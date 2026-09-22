#!/usr/bin/env python3
"""Load one stage of a progressive context bundle."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


def resolve_path(value: str, base: Path = REPO_ROOT) -> Path:
    candidate = Path(value)
    if candidate.is_absolute():
        return candidate
    from_cwd = Path.cwd() / candidate
    if from_cwd.exists():
        return from_cwd
    return base / candidate


def read_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise SystemExit(f"{path}: expected a YAML mapping")
    return data


def item_path(item: Any) -> str:
    if isinstance(item, str):
        return item
    if isinstance(item, dict) and isinstance(item.get("path"), str):
        return item["path"]
    raise SystemExit(f"Invalid bundle item: {item!r}")


def stage_items(bundle: dict[str, Any], stage: str) -> list[str]:
    stages = bundle.get("stages")
    if not isinstance(stages, dict):
        raise SystemExit("Bundle must contain a stages mapping")
    if stage not in stages:
        available = ", ".join(str(key) for key in stages)
        raise SystemExit(f"Unknown stage {stage!r}; available: {available}")
    raw_items = stages[stage] or []
    if not isinstance(raw_items, list):
        raise SystemExit(f"Stage {stage!r} must contain a list")
    return [item_path(item) for item in raw_items]


def load_files(paths: list[str], repo_root: Path) -> list[dict[str, str]]:
    files: list[dict[str, str]] = []
    for raw_path in paths:
        path = resolve_path(raw_path, repo_root)
        if not path.exists():
            raise SystemExit(f"Bundle path not found: {raw_path}")
        files.append(
            {
                "path": raw_path,
                "content": path.read_text(encoding="utf-8"),
            }
        )
    return files


def print_text(bundle: dict[str, Any], stage: str, files: list[dict[str, str]]) -> None:
    print(f"bundle={bundle.get('bundle_id', '-')}")
    print(f"title={bundle.get('title', '-')}")
    print(f"stage={stage}")
    print(f"files={len(files)}")
    for file in files:
        print(f"\n===== {file['path']} =====")
        print(file["content"].rstrip())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", help="Bundle YAML path")
    parser.add_argument("--stage", help="Stage to load")
    parser.add_argument("--list-stages", action="store_true", help="List stages and exit")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    bundle_path = resolve_path(args.bundle)
    if not bundle_path.exists():
        raise SystemExit(f"Bundle not found: {args.bundle}")
    bundle = read_yaml(bundle_path)
    stages = bundle.get("stages")
    if not isinstance(stages, dict):
        raise SystemExit("Bundle must contain a stages mapping")

    if args.list_stages:
        for stage in stages:
            print(stage)
        return 0
    if not args.stage:
        raise SystemExit("Provide --stage or use --list-stages")

    files = load_files(stage_items(bundle, args.stage), REPO_ROOT)
    if args.format == "json":
        print(json.dumps({"bundle": bundle, "stage": args.stage, "files": files}, ensure_ascii=False, indent=2))
    else:
        print_text(bundle, args.stage, files)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
