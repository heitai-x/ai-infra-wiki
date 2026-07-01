#!/usr/bin/env python3
"""Search the local AI Infra LLM Wiki SQLite FTS5 index."""
from __future__ import annotations

import argparse
import re
import sqlite3
from pathlib import Path

TOKEN_RE = re.compile(r"[\w\-./:+]+|[\u4e00-\u9fff]{1,}")
FILTER_COLUMNS = {"type", "topic", "component", "level", "status", "reliability", "source_type"}


def make_fts_query(query: str) -> str:
    terms = TOKEN_RE.findall(query)
    if not terms:
        return query
    return " OR ".join(f'"{term}"' for term in terms)


def parse_filters(values: list[str]) -> tuple[str, list[str]]:
    clauses: list[str] = []
    params: list[str] = []
    for value in values:
        if "=" not in value:
            raise SystemExit(f"Invalid filter {value!r}; expected key=value")
        key, raw = value.split("=", 1)
        key = key.strip()
        if key not in FILTER_COLUMNS:
            raise SystemExit(f"Invalid filter column {key!r}; allowed: {', '.join(sorted(FILTER_COLUMNS))}")
        clauses.append(f"{key} = ?")
        params.append(raw.strip())
    if not clauses:
        return "", []
    return " AND " + " AND ".join(clauses), params


def search(conn: sqlite3.Connection, query: str, filters: list[str], limit: int) -> list[sqlite3.Row]:
    where_sql, filter_params = parse_filters(filters)
    fts_query = make_fts_query(query)
    sql = f"""
        SELECT
            rel_path,
            title,
            heading_path,
            type,
            topic,
            component,
            level,
            reliability,
            source_type,
            source_url,
            last_checked,
            bm25(chunks_fts) AS score,
            snippet(chunks_fts, 5, '[', ']', ' ... ', 24) AS snippet
        FROM chunks_fts
        WHERE chunks_fts MATCH ?{where_sql}
        ORDER BY score
        LIMIT ?
    """
    try:
        return conn.execute(sql, [fts_query, *filter_params, limit]).fetchall()
    except sqlite3.OperationalError:
        like_sql = f"""
            SELECT
                rel_path,
                title,
                heading_path,
                type,
                topic,
                component,
                level,
                reliability,
                source_type,
                source_url,
                last_checked,
                0.0 AS score,
                substr(content, 1, 240) AS snippet
            FROM chunks
            WHERE content LIKE ?{where_sql}
            LIMIT ?
        """
        return conn.execute(like_sql, [f"%{query}%", *filter_params, limit]).fetchall()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="Search query")
    parser.add_argument("--db", default="wiki-index/ai_infra_wiki.sqlite", help="SQLite index path")
    parser.add_argument("--filter", action="append", default=[], help="Metadata filter, e.g. topic=training")
    parser.add_argument("--limit", type=int, default=8, help="Max results")
    args = parser.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        raise SystemExit(f"Index not found: {db_path}. Run scripts/build_wiki_index.py first.")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = search(conn, args.query, args.filter, args.limit)
    conn.close()

    print(f"results={len(rows)} query={args.query!r}")
    for i, row in enumerate(rows, 1):
        component = row["component"] or "-"
        source_type = row["source_type"] or "-"
        source_url = row["source_url"] or "-"
        last_checked = row["last_checked"] or "-"
        print(f"\n{i}. {row['title']} :: {row['heading_path']}")
        print(
            f"   path={row['rel_path']} type={row['type']} topic={row['topic']} "
            f"component={component} level={row['level']} reliability={row['reliability']} "
            f"source_type={source_type} last_checked={last_checked} score={row['score']:.4f}"
        )
        print(f"   source_url={source_url}")
        print(f"   {row['snippet'].replace(chr(10), ' ')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
