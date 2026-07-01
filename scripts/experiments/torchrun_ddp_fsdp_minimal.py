#!/usr/bin/env python3
"""Minimal torchrun DDP/FSDP experiment for the AI Infra Wiki.

Examples:
  torchrun --standalone --nproc_per_node=2 scripts/experiments/torchrun_ddp_fsdp_minimal.py --strategy ddp
  torchrun --standalone --nproc_per_node=2 scripts/experiments/torchrun_ddp_fsdp_minimal.py --strategy fsdp --activation-checkpoint
"""
from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import asdict, dataclass

import torch
import torch.distributed as dist
import torch.nn as nn
from torch.distributed.fsdp import FullyShardedDataParallel as FSDP
from torch.nn.parallel import DistributedDataParallel as DDP

try:
    from torch.distributed.algorithms._checkpoint.checkpoint_wrapper import checkpoint_wrapper
except Exception:  # pragma: no cover - optional across PyTorch versions
    checkpoint_wrapper = None


@dataclass
class StepMetric:
    step: int
    loss: float
    step_time_ms: float
    max_memory_allocated_mb: float
    max_memory_reserved_mb: float


class TinyTransformer(nn.Module):
    def __init__(self, vocab_size: int, hidden: int, layers: int, heads: int, seq_len: int) -> None:
        super().__init__()
        self.token = nn.Embedding(vocab_size, hidden)
        block = nn.TransformerEncoderLayer(
            d_model=hidden,
            nhead=heads,
            dim_feedforward=hidden * 4,
            batch_first=True,
            activation="gelu",
        )
        self.blocks = nn.ModuleList([block if i == 0 else type(block)(
            d_model=hidden,
            nhead=heads,
            dim_feedforward=hidden * 4,
            batch_first=True,
            activation="gelu",
        ) for i in range(layers)])
        self.norm = nn.LayerNorm(hidden)
        self.lm_head = nn.Linear(hidden, vocab_size, bias=False)
        self.seq_len = seq_len

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        x = self.token(input_ids)
        for block in self.blocks:
            x = block(x)
        x = self.norm(x)
        return self.lm_head(x)


def setup_distributed() -> tuple[int, int, int, torch.device]:
    rank = int(os.environ.get("RANK", "0"))
    local_rank = int(os.environ.get("LOCAL_RANK", "0"))
    world_size = int(os.environ.get("WORLD_SIZE", "1"))
    if world_size > 1 and not dist.is_initialized():
        backend = "nccl" if torch.cuda.is_available() else "gloo"
        dist.init_process_group(backend=backend)
    if torch.cuda.is_available():
        torch.cuda.set_device(local_rank)
        device = torch.device("cuda", local_rank)
    else:
        device = torch.device("cpu")
    return rank, local_rank, world_size, device


def maybe_wrap_blocks(model: TinyTransformer, enabled: bool) -> TinyTransformer:
    if not enabled or checkpoint_wrapper is None:
        return model
    model.blocks = nn.ModuleList([checkpoint_wrapper(block) for block in model.blocks])
    return model


def build_model(args: argparse.Namespace, device: torch.device) -> nn.Module:
    model = TinyTransformer(args.vocab_size, args.hidden, args.layers, args.heads, args.seq_len)
    model = maybe_wrap_blocks(model, args.activation_checkpoint)
    model.to(device)
    if args.strategy == "ddp" and dist.is_initialized():
        model = DDP(model, device_ids=[device.index] if device.type == "cuda" else None)
    elif args.strategy == "fsdp" and dist.is_initialized():
        model = FSDP(model)
    return model


def sync() -> None:
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    if dist.is_initialized():
        dist.barrier()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strategy", choices=["single", "ddp", "fsdp"], default="ddp")
    parser.add_argument("--steps", type=int, default=20)
    parser.add_argument("--warmup", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--seq-len", type=int, default=128)
    parser.add_argument("--vocab-size", type=int, default=4096)
    parser.add_argument("--hidden", type=int, default=512)
    parser.add_argument("--layers", type=int, default=4)
    parser.add_argument("--heads", type=int, default=8)
    parser.add_argument("--activation-checkpoint", action="store_true")
    parser.add_argument("--output", default="artifacts/torchrun_ddp_fsdp_metrics.jsonl")
    args = parser.parse_args()

    rank, local_rank, world_size, device = setup_distributed()
    torch.manual_seed(1234 + rank)
    model = build_model(args, device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    loss_fn = nn.CrossEntropyLoss()

    if rank == 0:
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        open(args.output, "w", encoding="utf-8").close()

    metrics: list[StepMetric] = []
    total_steps = args.warmup + args.steps
    for step in range(total_steps):
        if torch.cuda.is_available():
            torch.cuda.reset_peak_memory_stats(device)
        input_ids = torch.randint(0, args.vocab_size, (args.batch_size, args.seq_len), device=device)
        labels = torch.roll(input_ids, shifts=-1, dims=1)
        sync()
        start = time.perf_counter()
        logits = model(input_ids)
        loss = loss_fn(logits.reshape(-1, args.vocab_size), labels.reshape(-1))
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
        sync()
        elapsed_ms = (time.perf_counter() - start) * 1000
        if step >= args.warmup:
            allocated = torch.cuda.max_memory_allocated(device) / 2**20 if torch.cuda.is_available() else 0.0
            reserved = torch.cuda.max_memory_reserved(device) / 2**20 if torch.cuda.is_available() else 0.0
            metric = StepMetric(step=step - args.warmup, loss=float(loss.detach().cpu()), step_time_ms=elapsed_ms, max_memory_allocated_mb=allocated, max_memory_reserved_mb=reserved)
            metrics.append(metric)
            if rank == 0:
                with open(args.output, "a", encoding="utf-8") as f:
                    f.write(json.dumps(asdict(metric), ensure_ascii=False) + "\n")

    if rank == 0 and metrics:
        avg_ms = sum(m.step_time_ms for m in metrics) / len(metrics)
        max_mem = max(m.max_memory_allocated_mb for m in metrics)
        print(json.dumps({
            "strategy": args.strategy,
            "world_size": world_size,
            "steps": len(metrics),
            "avg_step_time_ms": avg_ms,
            "max_memory_allocated_mb": max_mem,
            "output": args.output,
        }, ensure_ascii=False, indent=2))
    if dist.is_initialized():
        dist.destroy_process_group()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
