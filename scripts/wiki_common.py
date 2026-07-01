#!/usr/bin/env python3
"""Shared helpers for AI Infra wiki maintenance scripts."""
from __future__ import annotations

import fnmatch
from pathlib import Path
from typing import Any

import yaml

DEFAULT_IGNORE_GLOBS = [
    ".ipynb_checkpoints/**",
    "**/.ipynb_checkpoints/**",
    ".obsidian/**",
    "**/.obsidian/**",
    "__pycache__/**",
    "**/__pycache__/**",
]


def load_wiki_config(wiki_root: Path) -> dict[str, Any]:
    config_path = wiki_root / ".ai-wiki.yml"
    if not config_path.exists():
        return {}
    data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{config_path}: expected a YAML mapping")
    return data


def ignore_globs(config: dict[str, Any]) -> list[str]:
    raw = config.get("ignore_globs", [])
    if not isinstance(raw, list):
        return list(DEFAULT_IGNORE_GLOBS)
    return [*DEFAULT_IGNORE_GLOBS, *(str(item) for item in raw)]


def should_ignore(path: Path, root: Path, config: dict[str, Any]) -> bool:
    rel = str(path.relative_to(root)).replace("\\", "/")
    parts = path.relative_to(root).parts
    if any(part in {".ipynb_checkpoints", ".obsidian", "__pycache__"} for part in parts):
        return True
    for pattern in ignore_globs(config):
        if fnmatch.fnmatch(rel, pattern):
            return True
    return False


def iter_markdown_files(root: Path, config: dict[str, Any]) -> list[Path]:
    files: list[Path] = []
    for path in sorted(root.rglob("*.md")):
        if should_ignore(path, root, config):
            continue
        files.append(path)
    return files


def parse_front_matter(text: str, rel_path: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        raise ValueError(f"{rel_path}: missing front matter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError(f"{rel_path}: missing closing front matter")
    raw = text[4:end]
    body = text[end + len("\n---\n"):].lstrip("\n")
    data = yaml.safe_load(raw) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{rel_path}: front matter must be a YAML mapping")
    return data, body


def front_matter_scalar(front_matter: dict[str, Any], key: str) -> str:
    value = front_matter.get(key, "")
    if value is None:
        return ""
    if isinstance(value, (list, dict)):
        return ""
    return str(value).strip()


def front_matter_text(front_matter: dict[str, Any], key: str) -> str:
    value = front_matter.get(key, "")
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    if isinstance(value, dict):
        return yaml.safe_dump(value, allow_unicode=True, sort_keys=True).strip()
    return str(value).strip()


def json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_safe(item) for item in value]
    if isinstance(value, tuple):
        return [json_safe(item) for item in value]
    if hasattr(value, "isoformat"):
        try:
            return value.isoformat()
        except TypeError:
            return str(value)
    return value
