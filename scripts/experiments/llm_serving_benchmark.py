#!/usr/bin/env python3
"""Small OpenAI-compatible LLM serving benchmark harness.

The script intentionally uses only the Python standard library so it can run on
bare servers. It records raw JSONL artifacts that the wiki can ingest later.
"""
from __future__ import annotations

import argparse
import concurrent.futures as futures
import json
import statistics
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class RequestMetric:
    request_id: int
    ok: bool
    latency_ms: float
    prompt_chars: int
    output_tokens: int
    error: str = ""


def read_prompts(path: Path) -> list[str]:
    prompts: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        prompts.append(obj.get("prompt") or obj.get("messages", [{}])[-1].get("content", ""))
    return prompts


def post_json(url: str, payload: dict, timeout: float) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def run_one(request_id: int, prompt: str, args: argparse.Namespace) -> RequestMetric:
    payload = {
        "model": args.model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": args.max_tokens,
        "temperature": args.temperature,
        "stream": False,
    }
    start = time.perf_counter()
    try:
        response = post_json(args.url, payload, args.timeout)
        elapsed_ms = (time.perf_counter() - start) * 1000
        usage = response.get("usage", {})
        output_tokens = int(usage.get("completion_tokens") or 0)
        if not output_tokens:
            text = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            output_tokens = max(1, len(text.split())) if text else 0
        return RequestMetric(request_id=request_id, ok=True, latency_ms=elapsed_ms, prompt_chars=len(prompt), output_tokens=output_tokens)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError) as exc:
        elapsed_ms = (time.perf_counter() - start) * 1000
        return RequestMetric(request_id=request_id, ok=False, latency_ms=elapsed_ms, prompt_chars=len(prompt), output_tokens=0, error=repr(exc))


def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    idx = min(len(values) - 1, int(round((p / 100) * (len(values) - 1))))
    return values[idx]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8000/v1/chat/completions")
    parser.add_argument("--model", required=True)
    parser.add_argument("--prompts", default="artifacts/sample-workloads/llm_prompts.jsonl")
    parser.add_argument("--concurrency", type=int, default=4)
    parser.add_argument("--requests", type=int, default=16)
    parser.add_argument("--max-tokens", type=int, default=64)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument("--output", default="artifacts/llm_serving_benchmark.jsonl")
    args = parser.parse_args()

    prompts = read_prompts(Path(args.prompts))
    if not prompts:
        raise SystemExit(f"No prompts found in {args.prompts}")
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    request_prompts = [prompts[i % len(prompts)] for i in range(args.requests)]
    start = time.perf_counter()
    metrics: list[RequestMetric] = []
    with futures.ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        future_map = {pool.submit(run_one, i, prompt, args): i for i, prompt in enumerate(request_prompts)}
        for future in futures.as_completed(future_map):
            metric = future.result()
            metrics.append(metric)
            with output.open("a", encoding="utf-8") as f:
                f.write(json.dumps(asdict(metric), ensure_ascii=False) + "\n")
    wall = time.perf_counter() - start
    ok = [m for m in metrics if m.ok]
    latencies = [m.latency_ms for m in ok]
    generated_tokens = sum(m.output_tokens for m in ok)
    summary = {
        "requests": len(metrics),
        "ok": len(ok),
        "errors": len(metrics) - len(ok),
        "concurrency": args.concurrency,
        "wall_time_s": wall,
        "request_throughput_rps": len(ok) / wall if wall else 0.0,
        "generation_tokens_per_s": generated_tokens / wall if wall else 0.0,
        "latency_ms_avg": statistics.mean(latencies) if latencies else 0.0,
        "latency_ms_p50": percentile(latencies, 50),
        "latency_ms_p95": percentile(latencies, 95),
        "latency_ms_p99": percentile(latencies, 99),
        "raw_output": str(output),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if len(ok) == len(metrics) else 2


if __name__ == "__main__":
    raise SystemExit(main())
