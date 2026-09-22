#!/usr/bin/env python3
"""Create or update a human-readable study checkpoint."""
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


def resolve_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or path.exists():
        return path
    return REPO_ROOT / path


def read_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise SystemExit(f"{path}: expected a YAML mapping")
    return data


def append_unique(mapping: dict[str, Any], key: str, values: list[str]) -> None:
    current = mapping.setdefault(key, [])
    if not isinstance(current, list):
        current = []
        mapping[key] = current
    for value in values:
        if value and value not in current:
            current.append(value)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="Checkpoint YAML path")
    parser.add_argument("--template", default="checkpoints/template.yml", help="Template YAML path")
    parser.add_argument("--checkpoint-id")
    parser.add_argument("--bundle")
    parser.add_argument("--status", choices=("in_progress", "complete", "blocked"))
    parser.add_argument("--stage")
    parser.add_argument("--action")
    parser.add_argument("--loaded-page", action="append", default=[])
    parser.add_argument("--completed", action="append", default=[])
    parser.add_argument("--in-progress", dest="in_progress", action="append", default=[])
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--open-question", action="append", default=[])
    args = parser.parse_args()

    output_path = resolve_path(args.output)
    if output_path.exists() and output_path.stat().st_size > 0:
        checkpoint = read_yaml(output_path)
    else:
        checkpoint = read_yaml(resolve_path(args.template))

    today = date.today().isoformat()
    checkpoint.setdefault("schema_version", 1)
    checkpoint.setdefault("created_at", today)
    checkpoint["updated_at"] = today
    if args.checkpoint_id:
        checkpoint["checkpoint_id"] = args.checkpoint_id
    elif not checkpoint.get("checkpoint_id"):
        checkpoint["checkpoint_id"] = output_path.stem
    if args.status:
        checkpoint["status"] = args.status

    goal = checkpoint.setdefault("goal", {})
    if args.bundle:
        goal["bundle"] = args.bundle

    context = checkpoint.setdefault("context", {})
    if args.stage:
        append_unique(context, "loaded_stages", [args.stage])
    append_unique(context, "loaded_pages", args.loaded_page)

    progress = checkpoint.setdefault("progress", {})
    append_unique(progress, "completed", args.completed)
    append_unique(progress, "in_progress", args.in_progress)

    evidence = checkpoint.setdefault("evidence", {})
    append_unique(evidence, "artifacts", args.evidence)
    append_unique(checkpoint, "open_questions", args.open_question)

    next_step = checkpoint.setdefault("next", {})
    if args.stage:
        next_step["stage"] = args.stage
    if args.action:
        next_step["action"] = args.action

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        yaml.safe_dump(checkpoint, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print(f"checkpoint_written={output_path}")
    print(f"checkpoint_id={checkpoint['checkpoint_id']}")
    print(f"updated_at={checkpoint['updated_at']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
