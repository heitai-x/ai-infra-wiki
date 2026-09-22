#!/usr/bin/env python3
"""Summarize a learning checklist and an optional study checkpoint."""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import Any

import yaml


def read_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise SystemExit(f"{path}: expected a YAML mapping")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checklist", required=True, help="Checklist YAML path")
    parser.add_argument("--checkpoint", help="Optional study checkpoint YAML path")
    args = parser.parse_args()

    checklist_path = Path(args.checklist)
    checklist = read_yaml(checklist_path)
    items = checklist.get("items") or []
    if not isinstance(items, list):
        raise SystemExit("Checklist items must be a list")
    statuses = Counter(str(item.get("status", "todo")) for item in items if isinstance(item, dict))
    total = len(items)
    done = statuses.get("done", 0)
    print(f"checklist={checklist.get('checklist_id', checklist_path)}")
    print(f"progress={done}/{total} done")
    print("statuses=" + ", ".join(f"{key}:{value}" for key, value in sorted(statuses.items())))

    if args.checkpoint:
        checkpoint = read_yaml(Path(args.checkpoint))
        progress = checkpoint.get("progress") or {}
        completed = progress.get("completed") or []
        next_step = checkpoint.get("next") or {}
        print(f"checkpoint={checkpoint.get('checkpoint_id', args.checkpoint)}")
        print(f"checkpoint_status={checkpoint.get('status', '-')}")
        print(f"completed_items={len(completed)}")
        print(f"next_stage={next_step.get('stage', '-')}")
        print(f"next_action={next_step.get('action', '-')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
