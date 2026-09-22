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


def selected_items(bundle: dict[str, Any], stage: str, through: bool) -> list[str]:
    if not through:
        return stage_items(bundle, stage)
    stages = bundle.get("stages")
    if not isinstance(stages, dict):
        raise SystemExit("Bundle must contain a stages mapping")
    names = list(stages)
    if stage not in names:
        available = ", ".join(str(name) for name in names)
        raise SystemExit(f"Unknown stage {stage!r}; available: {available}")
    paths: list[str] = []
    for name in names[: names.index(stage) + 1]:
        for path in stage_items(bundle, name):
            if path not in paths:
                paths.append(path)
    return paths


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


def print_text(bundle: dict[str, Any], stage: str, files: list[dict[str, str]], through: bool) -> None:
    print(f"bundle={bundle.get('bundle_id', '-')}")
    print(f"title={bundle.get('title', '-')}")
    print(f"{'through' if through else 'stage'}={stage}")
    print(f"files={len(files)}")
    for file in files:
        print(f"\n===== {file['path']} =====")
        print(file["content"].rstrip())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", help="Bundle YAML path")
    stage_group = parser.add_mutually_exclusive_group()
    stage_group.add_argument("--stage", help="Load one stage")
    stage_group.add_argument("--through", help="Load all stages through this stage")
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
    selected_stage = args.stage or args.through
    if not selected_stage:
        raise SystemExit("Provide --stage, --through or use --list-stages")

    through = bool(args.through)
    files = load_files(selected_items(bundle, selected_stage, through), REPO_ROOT)
    if args.format == "json":
        print(json.dumps({"bundle": bundle, "stage": selected_stage, "through": through, "files": files}, ensure_ascii=False, indent=2))
    else:
        print_text(bundle, selected_stage, files, through)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
