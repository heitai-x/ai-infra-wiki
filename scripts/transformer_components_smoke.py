#!/usr/bin/env python3
"""Run small, CPU-friendly checks for the transformer component learning path.

The NumPy checks are deliberately independent of PyTorch so that the shape,
mask, cache and formula checks remain runnable on a machine whose PyTorch
installation cannot load its native DLLs.  When ``--source-root`` is given and
PyTorch imports successfully, the same invariants are also checked against the
six IDE source files recorded in the handoff document.
"""

from __future__ import annotations

import argparse
import ast
import importlib
import json
import platform
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np


EXPECTED_DEFINITIONS = {
    "softmax.py": {"safe_softmax"},
    "ReLu.py": {"relu", "ReLU"},
    "RMSNorm.py": {"RMSNorm"},
    "MHA.py": {"MultiheadAttention"},
    "GQA.py": {"GQA", "GroupedQueryAttention"},
    "kvcache.py": {"KVCache"},
}


@dataclass
class Check:
    name: str
    status: str
    detail: str


def check(name: str, condition: bool, detail: str) -> Check:
    return Check(name=name, status="passed" if condition else "failed", detail=detail)


def safe_softmax_np(x: np.ndarray, mask: np.ndarray | None = None, axis: int = -1) -> np.ndarray:
    """Reference implementation matching the handoff's safe_softmax contract."""

    values = np.asarray(x)
    if values.ndim == 0:
        raise ValueError("x must have at least one dimension")
    if not np.issubdtype(values.dtype, np.floating):
        raise TypeError("x must be a floating-point array")
    if mask is None:
        keep = np.ones(values.shape, dtype=bool)
    else:
        keep = np.broadcast_to(np.asarray(mask, dtype=bool), values.shape)
    masked = np.where(keep, values, -np.inf)
    row_max = np.max(masked, axis=axis, keepdims=True)
    safe_max = np.where(np.isfinite(row_max), row_max, 0)
    with np.errstate(over="ignore", under="ignore", invalid="ignore", divide="ignore"):
        exponent = np.exp(masked - safe_max)
    exponent = np.where(keep, exponent, 0)
    denom = np.sum(exponent, axis=axis, keepdims=True)
    safe_denom = np.where(denom > 0, denom, 1)
    return (exponent / safe_denom).astype(values.dtype, copy=False)


def rms_norm_np(x: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    values = np.asarray(x)
    compute = values.astype(np.float32 if values.dtype == np.float16 else values.dtype)
    mean_square = np.mean(np.square(compute), axis=-1, keepdims=True)
    output = compute * (1.0 / np.sqrt(mean_square + eps))
    return output.astype(values.dtype, copy=False)


def causal_mask(length: int) -> np.ndarray:
    return np.tril(np.ones((length, length), dtype=bool))


def attention_reference(
    x: np.ndarray,
    num_q_heads: int,
    num_kv_heads: int | None = None,
    mask: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Small self-attention reference used only for shape and mask checks."""

    batch, seq_len, d_model = x.shape
    if d_model % num_q_heads:
        raise ValueError("d_model must be divisible by num_q_heads")
    num_kv_heads = num_kv_heads or num_q_heads
    if num_q_heads % num_kv_heads:
        raise ValueError("num_q_heads must be divisible by num_kv_heads")
    head_dim = d_model // num_q_heads

    q = x.reshape(batch, seq_len, num_q_heads, head_dim).transpose(0, 2, 1, 3)
    kv_width = num_kv_heads * head_dim
    k = x[..., :kv_width].reshape(batch, seq_len, num_kv_heads, head_dim).transpose(0, 2, 1, 3)
    v = (x[..., :kv_width] + 0.25).reshape(batch, seq_len, num_kv_heads, head_dim).transpose(0, 2, 1, 3)
    if num_kv_heads != num_q_heads:
        groups = num_q_heads // num_kv_heads
        k = np.repeat(k, groups, axis=1)
        v = np.repeat(v, groups, axis=1)
    scores = np.matmul(q, np.swapaxes(k, -1, -2)) / np.sqrt(head_dim)
    weights = safe_softmax_np(scores, mask=mask, axis=-1)
    values = np.matmul(weights, v)
    output = values.transpose(0, 2, 1, 3).reshape(batch, seq_len, d_model)
    return output, weights


class NumpyKVCache:
    """Contiguous single-length cache mirroring the IDE KVCache layout."""

    def __init__(self, batch_size: int, num_kv_heads: int, max_seq_len: int, head_dim: int, dtype: Any = np.float32) -> None:
        self.k = np.empty((batch_size, num_kv_heads, max_seq_len, head_dim), dtype=dtype)
        self.v = np.empty_like(self.k)
        self.length = 0

    @property
    def remaining_length(self) -> int:
        return self.k.shape[2] - self.length

    @property
    def is_full(self) -> bool:
        return self.length >= self.k.shape[2]

    def append(self, new_k: np.ndarray, new_v: np.ndarray) -> None:
        if new_k.shape != new_v.shape or new_k.ndim != 4:
            raise ValueError("new_k and new_v must have shape [B, Hkv, Tnew, Dh]")
        end = self.length + new_k.shape[2]
        if end > self.k.shape[2]:
            raise RuntimeError("KV cache overflow")
        self.k[:, :, self.length:end, :] = new_k
        self.v[:, :, self.length:end, :] = new_v
        self.length = end

    def get(self) -> tuple[np.ndarray, np.ndarray]:
        return self.k[:, :, : self.length, :], self.v[:, :, : self.length, :]

    def reset(self) -> None:
        self.length = 0


def run_numpy_checks() -> list[Check]:
    checks: list[Check] = []

    values = np.array([[1.0, 2.0, 3.0], [1.0, 2.0, 3.0]], dtype=np.float32)
    mask = np.array([[True, True, False], [False, False, False]])
    result = safe_softmax_np(values, mask=mask)
    checks.append(check(
        "safe_softmax_mask_and_full_row",
        bool(np.isfinite(result).all() and np.allclose(result[0].sum(), 1.0) and result[0, 2] == 0 and np.all(result[1] == 0)),
        f"result={result.tolist()}",
    ))

    dtype_details: list[str] = []
    dtype_ok = True
    for dtype in (np.float32, np.float16):
        typed = safe_softmax_np(values.astype(dtype), mask=mask)
        dtype_ok = dtype_ok and bool(np.isfinite(typed).all() and np.all(typed[1] == 0))
        dtype_details.append(f"{np.dtype(dtype).name}:finite={bool(np.isfinite(typed).all())}")
    checks.append(check("safe_softmax_float_dtypes", dtype_ok, "; ".join(dtype_details)))

    relu_input = np.array([[-2.0, 0.0, 3.0]], dtype=np.float32)
    relu_output = np.maximum(relu_input, 0)
    checks.append(check("relu_forward", bool(np.array_equal(relu_output, [[0.0, 0.0, 3.0]])), f"output={relu_output.tolist()}"))

    norm_input = np.array([[3.0, 4.0]], dtype=np.float16)
    norm_output = rms_norm_np(norm_input)
    rms = np.sqrt(np.mean(norm_output.astype(np.float32) ** 2, axis=-1))
    checks.append(check("rmsnorm_unit_rms", bool(np.allclose(rms, 1.0, atol=2e-3)), f"output={norm_output.tolist()}, rms={rms.tolist()}"))

    x = np.arange(1, 1 + 2 * 4 * 8, dtype=np.float32).reshape(2, 4, 8) / 10
    causal = causal_mask(4)[None, None, :, :]
    mha_output, mha_weights = attention_reference(x, num_q_heads=4, mask=causal)
    gqa_output, gqa_weights = attention_reference(x, num_q_heads=4, num_kv_heads=2, mask=causal)
    future_mass = np.triu(mha_weights[0], k=1).max()
    checks.append(check(
        "mha_shape_and_causal_mask",
        bool(mha_output.shape == (2, 4, 8) and mha_weights.shape == (2, 4, 4, 4) and future_mass == 0),
        f"output_shape={list(mha_output.shape)}, weights_shape={list(mha_weights.shape)}, future_max={float(future_mass)}",
    ))
    checks.append(check(
        "gqa_shape_and_kv_ratio",
        bool(gqa_output.shape == (2, 4, 8) and gqa_weights.shape == (2, 4, 4, 4)),
        f"output_shape={list(gqa_output.shape)}, weights_shape={list(gqa_weights.shape)}, kv_heads=2, q_heads=4",
    ))

    cache = NumpyKVCache(batch_size=2, num_kv_heads=2, max_seq_len=5, head_dim=2, dtype=np.float32)
    first_k = np.ones((2, 2, 3, 2), dtype=np.float32)
    first_v = np.full_like(first_k, 2)
    next_k = np.full((2, 2, 1, 2), 3, dtype=np.float32)
    next_v = np.full_like(next_k, 4)
    cache.append(first_k, first_v)
    cache.append(next_k, next_v)
    got_k, got_v = cache.get()
    cache_ok = cache.length == 4 and got_k.shape == (2, 2, 4, 2) and got_v[:, :, -1, :].tolist() == [
        [[4.0, 4.0], [4.0, 4.0]],
        [[4.0, 4.0], [4.0, 4.0]],
    ]
    checks.append(check("kv_cache_prefill_decode_append", bool(cache_ok), f"length={cache.length}, shape={list(got_k.shape)}"))
    cache.reset()
    checks.append(check("kv_cache_reset", bool(cache.length == 0 and cache.remaining_length == 5), f"length={cache.length}, remaining={cache.remaining_length}"))

    return checks


def run_source_inventory(source_root: Path | None) -> tuple[list[Check], dict[str, Any]]:
    if source_root is None:
        return [check("source_inventory", False, "source root was not supplied")], {"status": "not_run"}
    checks: list[Check] = []
    inventory: dict[str, Any] = {"root": str(source_root), "files": {}}
    all_ok = True
    for filename, expected in EXPECTED_DEFINITIONS.items():
        path = source_root / filename
        if not path.exists():
            checks.append(check(f"source_exists:{filename}", False, "missing"))
            all_ok = False
            inventory["files"][filename] = {"status": "missing"}
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            definitions = {
                node.name
                for node in ast.walk(tree)
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            }
            for node in tree.body:
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            definitions.add(target.id)
            missing = sorted(expected - definitions)
            ok = not missing
            checks.append(check(f"source_definitions:{filename}", ok, f"found={sorted(definitions & expected)}, missing={missing}"))
            all_ok = all_ok and ok
            inventory["files"][filename] = {"status": "passed" if ok else "failed", "definitions": sorted(definitions)}
        except (OSError, SyntaxError) as exc:
            checks.append(check(f"source_parse:{filename}", False, f"{type(exc).__name__}: {exc}"))
            all_ok = False
            inventory["files"][filename] = {"status": "failed", "error": f"{type(exc).__name__}: {exc}"}
    checks.append(check("source_inventory", all_ok, f"root={source_root}"))
    inventory["status"] = "passed" if all_ok else "failed"
    return checks, inventory


def run_pytorch_checks(source_root: Path | None) -> tuple[list[Check], dict[str, Any]]:
    if source_root is None:
        return [], {"status": "not_run", "reason": "source root was not supplied"}
    try:
        import torch  # type: ignore
    except BaseException as exc:  # native DLL errors are not always Exception subclasses
        return [], {"status": "unavailable", "error_type": type(exc).__name__, "error": str(exc)}

    sys.path.insert(0, str(source_root))
    checks: list[Check] = []
    try:
        softmax_module = importlib.import_module("softmax")
        relu_module = importlib.import_module("ReLu")
        rms_module = importlib.import_module("RMSNorm")
        mha_module = importlib.import_module("MHA")
        gqa_module = importlib.import_module("GQA")
        cache_module = importlib.import_module("kvcache")

        values = torch.tensor([[1.0, 2.0, 3.0], [1.0, 2.0, 3.0]], dtype=torch.float32)
        mask = torch.tensor([[True, True, False], [False, False, False]])
        result = softmax_module.safe_softmax(values, mask=mask)
        checks.append(check("torch_safe_softmax", bool(torch.isfinite(result).all() and torch.all(result[1] == 0)), f"result={result.tolist()}"))

        relu_result = relu_module.relu(torch.tensor([-1.0, 0.0, 2.0]))
        checks.append(check("torch_relu", bool(torch.equal(relu_result, torch.tensor([0.0, 0.0, 2.0]))), f"output={relu_result.tolist()}"))

        norm = rms_module.RMSNorm(4)
        norm_result = norm(torch.ones(2, 3, 4, dtype=torch.float32))
        checks.append(check("torch_rmsnorm_shape", tuple(norm_result.shape) == (2, 3, 4), f"shape={list(norm_result.shape)}"))

        x = torch.randn(2, 4, 8)
        mha = mha_module.MultiheadAttention(input_dim=8, d_model=8, num_heads=4)
        mha_result = mha(x, is_causal=True)
        checks.append(check("torch_mha_shape", tuple(mha_result.shape) == (2, 4, 8), f"shape={list(mha_result.shape)}"))

        gqa = gqa_module.GQA(input_dim=8, d_model=8, num_q_heads=4, num_kv_heads=2)
        gqa_result = gqa(x, is_causal=True)
        checks.append(check("torch_gqa_shape", tuple(gqa_result.shape) == (2, 4, 8), f"shape={list(gqa_result.shape)}"))

        cache = cache_module.KVCache(2, 2, 5, 2, dtype=torch.float32)
        new_k = torch.ones(2, 2, 3, 2)
        new_v = torch.ones_like(new_k)
        cache.append(new_k, new_v)
        got_k, got_v = cache.get()
        checks.append(check("torch_kv_cache_append", tuple(got_k.shape) == (2, 2, 3, 2) and cache.length == 3, f"shape={list(got_k.shape)}, length={cache.length}"))
    except BaseException as exc:
        checks.append(check("torch_source_checks", False, f"{type(exc).__name__}: {exc}"))
    finally:
        try:
            sys.path.remove(str(source_root))
        except ValueError:
            pass
    return checks, {"status": "available", "version": torch.__version__}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, help="Directory containing softmax.py, ReLu.py, RMSNorm.py, MHA.py, GQA.py and kvcache.py")
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    args = parser.parse_args()

    source_root = args.source_root
    if source_root is not None:
        source_root = source_root.expanduser().resolve()

    numpy_checks = run_numpy_checks()
    inventory_checks, inventory = run_source_inventory(source_root)
    torch_checks, torch_status = run_pytorch_checks(source_root)
    all_checks = numpy_checks + inventory_checks + torch_checks
    result = {
        "experiment": "transformer_components_smoke",
        "collected_at": "2026-09-23",
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "source_root": str(source_root) if source_root else None,
        },
        "source_inventory": inventory,
        "pytorch": torch_status,
        "checks": [check.__dict__ for check in all_checks],
        "passed": all(item.status == "passed" for item in all_checks if not item.name.startswith("torch_") or torch_status.get("status") == "available"),
        "note": "NumPy checks are reference invariants. PyTorch checks are skipped when the local native installation cannot be imported.",
    }
    # A missing optional PyTorch runtime is an environment boundary, not a failed
    # NumPy invariant. Any attempted PyTorch check that fails remains a failure.
    if torch_status.get("status") != "available":
        result["passed"] = all(item.status == "passed" for item in numpy_checks + inventory_checks)

    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    print(rendered)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
