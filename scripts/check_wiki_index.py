#!/usr/bin/env python3
"""Validate the materialized AI Infra Wiki SQLite index."""
from __future__ import annotations

import argparse
import re
import sqlite3
from pathlib import Path

from wiki_common import iter_markdown_files, load_wiki_config

TOKEN_RE = re.compile(r"[\w\-./:+]+|[\u4e00-\u9fff]{1,}")
REQUIRED_TABLES = {"pages", "chunks", "chunks_fts"}
REQUIRED_CHUNK_COLUMNS = {
    "chunk_id",
    "rel_path",
    "title",
    "heading_path",
    "content",
    "type",
    "topic",
    "component",
    "level",
    "status",
    "reliability",
    "source_type",
    "source_url",
    "last_checked",
}
SAMPLE_QUERIES = [
    ("KV cache", "topic", "inference", "30-inference-systems/kv-cache-paged-attention.md"),
    ("FSDP ZeRO", "topic", "training", "20-training-systems/ddp-fsdp-zero.md"),
    ("NCCL hang", "component", "nccl", "80-playbooks/nccl-hang-triage.md"),
]


def make_fts_query(query: str) -> str:
    terms = TOKEN_RE.findall(query)
    return " OR ".join(f'"{term}"' for term in terms) if terms else query


def table_names(conn: sqlite3.Connection) -> set[str]:
    rows = conn.execute("SELECT name FROM sqlite_master WHERE type IN ('table', 'virtual table')").fetchall()
    return {row[0] for row in rows}


def columns(conn: sqlite3.Connection, table: str) -> set[str]:
    return {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}


def sample_search(conn: sqlite3.Connection, query: str, filter_key: str, filter_value: str) -> list[str]:
    sql = f"""
        SELECT DISTINCT rel_path
        FROM chunks_fts
        WHERE chunks_fts MATCH ? AND {filter_key} = ?
        ORDER BY bm25(chunks_fts)
        LIMIT 8
    """
    return [row[0] for row in conn.execute(sql, [make_fts_query(query), filter_value]).fetchall()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wiki-root", default="ai-infra-wiki")
    parser.add_argument("--db", default="wiki-index/ai_infra_wiki.sqlite")
    args = parser.parse_args()

    wiki_root = Path(args.wiki_root).resolve()
    db_path = Path(args.db).resolve()
    if not db_path.exists():
        print(f"wiki_index_check=failed missing_db={db_path}")
        return 1

    errors: list[str] = []
    conn = sqlite3.connect(db_path)
    tables = table_names(conn)
    missing_tables = REQUIRED_TABLES - tables
    if missing_tables:
        errors.append(f"missing tables: {', '.join(sorted(missing_tables))}")

    chunk_columns = columns(conn, "chunks") if "chunks" in tables else set()
    missing_columns = REQUIRED_CHUNK_COLUMNS - chunk_columns
    if missing_columns:
        errors.append(f"chunks missing columns: {', '.join(sorted(missing_columns))}")

    config = load_wiki_config(wiki_root)
    fs_pages = {str(path.relative_to(wiki_root)) for path in iter_markdown_files(wiki_root, config)}
    db_pages = {row[0] for row in conn.execute("SELECT rel_path FROM pages").fetchall()} if "pages" in tables else set()
    missing_in_db = sorted(fs_pages - db_pages)
    extra_in_db = sorted(db_pages - fs_pages)
    if missing_in_db:
        errors.append(f"pages missing in db: {missing_in_db[:10]}")
    if extra_in_db:
        errors.append(f"pages extra in db: {extra_in_db[:10]}")

    page_count = conn.execute("SELECT count(*) FROM pages").fetchone()[0] if "pages" in tables else 0
    chunk_count = conn.execute("SELECT count(*) FROM chunks").fetchone()[0] if "chunks" in tables else 0

    sample_results: list[str] = []
    if not missing_tables:
        for query, filter_key, filter_value, expected in SAMPLE_QUERIES:
            rel_paths = sample_search(conn, query, filter_key, filter_value)
            sample_results.append(f"{query} [{filter_key}={filter_value}] -> {rel_paths[:3]}")
            if expected not in rel_paths:
                errors.append(f"sample query {query!r} did not return expected {expected}; got {rel_paths[:8]}")

    source_rows = conn.execute(
        "SELECT count(*) FROM chunks WHERE type='source' AND source_type != '' AND source_url != '' AND last_checked != ''"
    ).fetchone()[0] if "chunks" in tables else 0
    if source_rows == 0:
        errors.append("no source chunks with source_type/source_url/last_checked")

    conn.close()

    if errors:
        print(f"wiki_index_check=failed pages={page_count} chunks={chunk_count} errors={len(errors)}")
        for error in errors:
            print(error)
        for result in sample_results:
            print(result)
        return 1

    print(f"wiki_index_check=ok pages={page_count} chunks={chunk_count} source_chunks={source_rows}")
    for result in sample_results:
        print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
