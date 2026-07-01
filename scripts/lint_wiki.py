#!/usr/bin/env python3
"""Lint the AI Infra LLM Wiki.

Checks:
- every Markdown page starts with YAML front matter
- required fields, enum fields, and date fields are valid
- source pages have source_type/source_url/last_checked
- Obsidian-style wikilinks resolve to existing pages
- non-index pages are reachable through at least one inbound wikilink unless allowlisted
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

from wiki_common import front_matter_scalar, iter_markdown_files, load_wiki_config, parse_front_matter

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")

DEFAULT_REQUIRED_FIELDS = {
    "title",
    "type",
    "topic",
    "level",
    "status",
    "last_updated",
    "owner",
    "reliability",
}


def as_string_set(value: Any) -> set[str]:
    if not isinstance(value, list):
        return set()
    return {str(item).strip() for item in value}


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("ai-infra-wiki")
    root = root.resolve()
    config = load_wiki_config(root)
    required = as_string_set(config.get("required_front_matter")) or DEFAULT_REQUIRED_FIELDS
    allowed_types = as_string_set(config.get("allowed_types"))
    allowed_levels = as_string_set(config.get("allowed_levels"))
    allowed_statuses = as_string_set(config.get("allowed_statuses"))
    allowed_reliability = as_string_set(config.get("allowed_reliability"))
    allowed_source_types = as_string_set(config.get("allowed_source_types"))
    source_required = as_string_set(config.get("source_required_front_matter"))
    allowed_orphans = as_string_set(config.get("allowed_orphan_pages"))

    files = iter_markdown_files(root, config)
    existing = set()
    for path in files:
        existing.add(str(path.relative_to(root).with_suffix("")))
        existing.add(path.stem)

    errors: list[str] = []
    inbound: dict[str, int] = {str(path.relative_to(root)): 0 for path in files}
    stem_to_rel = {path.stem: str(path.relative_to(root)) for path in files}
    no_ext_to_rel = {str(path.relative_to(root).with_suffix("")): str(path.relative_to(root)) for path in files}

    for path in files:
        rel = str(path.relative_to(root))
        text = path.read_text(encoding="utf-8")
        try:
            fm, _ = parse_front_matter(text, rel)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        missing = sorted(required - set(fm))
        if missing:
            errors.append(f"{rel}: missing required fields: {', '.join(missing)}")

        page_type = front_matter_scalar(fm, "type")
        if allowed_types and page_type not in allowed_types:
            errors.append(f"{rel}: invalid type {page_type!r}")
        level = front_matter_scalar(fm, "level")
        if allowed_levels and level not in allowed_levels:
            errors.append(f"{rel}: invalid level {level!r}")
        status = front_matter_scalar(fm, "status")
        if allowed_statuses and status not in allowed_statuses:
            errors.append(f"{rel}: invalid status {status!r}")
        reliability = front_matter_scalar(fm, "reliability")
        if allowed_reliability and reliability not in allowed_reliability:
            errors.append(f"{rel}: invalid reliability {reliability!r}")
        last_updated = front_matter_scalar(fm, "last_updated")
        if not DATE_RE.match(last_updated):
            errors.append(f"{rel}: invalid last_updated {last_updated!r}; expected YYYY-MM-DD")
        if page_type == "source":
            missing_source = sorted(source_required - set(fm))
            if missing_source:
                errors.append(f"{rel}: source page missing fields: {', '.join(missing_source)}")
            source_type = front_matter_scalar(fm, "source_type")
            if allowed_source_types and source_type not in allowed_source_types:
                errors.append(f"{rel}: invalid source_type {source_type!r}")
            if "last_checked" in fm:
                last_checked = front_matter_scalar(fm, "last_checked")
                if not DATE_RE.match(last_checked):
                    errors.append(f"{rel}: invalid last_checked {last_checked!r}; expected YYYY-MM-DD")

        for match in LINK_RE.finditer(text):
            target = match.group(1).strip()
            if target.endswith(".md"):
                target = target[:-3]
            if target not in existing and Path(target).name not in existing:
                errors.append(f"{rel}: broken wikilink -> {target}")
                continue
            resolved = no_ext_to_rel.get(target) or stem_to_rel.get(Path(target).name)
            if resolved and resolved != rel:
                inbound[resolved] = inbound.get(resolved, 0) + 1

    for rel, count in sorted(inbound.items()):
        if count == 0 and rel not in allowed_orphans and not rel.startswith("00-index/"):
            errors.append(f"{rel}: orphan page has no inbound wikilink")

    if errors:
        print(f"wiki_lint=failed files={len(files)} errors={len(errors)}")
        for err in errors:
            print(err)
        return 1
    print(f"wiki_lint=ok files={len(files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
