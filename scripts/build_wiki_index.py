#!/usr/bin/env python3
"""Build a local SQLite FTS5 index for the AI Infra LLM Wiki."""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from wiki_common import (
    front_matter_scalar,
    front_matter_text,
    iter_markdown_files,
    json_safe,
    load_wiki_config,
    parse_front_matter,
)

FM_REQUIRED = {"title", "type", "topic", "level", "status", "last_updated", "owner", "reliability"}
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]")
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
URL_RE = re.compile(r"https?://[^\s)]+")


@dataclass
class Page:
    path: Path
    rel_path: str
    front_matter: dict[str, Any]
    body: str


@dataclass
class Chunk:
    chunk_id: str
    rel_path: str
    title: str
    heading: str
    heading_path: str
    content: str
    front_matter: dict[str, Any]
    source_url: str


def validate_front_matter(front_matter: dict[str, Any], rel_path: str) -> None:
    missing = sorted(FM_REQUIRED - set(front_matter))
    if missing:
        raise ValueError(f"{rel_path}: missing required front matter fields: {', '.join(missing)}")


def normalize_markdown(text: str) -> str:
    text = WIKILINK_RE.sub(lambda m: m.group(2) or m.group(1), text)
    text = MD_LINK_RE.sub(lambda m: f"{m.group(1)} {m.group(2)}", text)
    return text


def read_pages(wiki_root: Path) -> list[Page]:
    config = load_wiki_config(wiki_root)
    pages: list[Page] = []
    for path in iter_markdown_files(wiki_root, config):
        rel_path = str(path.relative_to(wiki_root))
        text = path.read_text(encoding="utf-8")
        fm, body = parse_front_matter(text, rel_path)
        validate_front_matter(fm, rel_path)
        pages.append(Page(path=path, rel_path=rel_path, front_matter=fm, body=body))
    return pages


def chunk_source_url(page: Page, raw_chunk: str) -> str:
    urls = URL_RE.findall(raw_chunk)
    if urls:
        return urls[0].rstrip(".,")
    return front_matter_scalar(page.front_matter, "source_url")


def split_chunks(page: Page) -> list[Chunk]:
    title = front_matter_scalar(page.front_matter, "title") or page.path.stem
    chunks: list[Chunk] = []
    heading_stack: list[str] = [title]
    current_heading = title
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_lines
        raw = "\n".join(current_lines).strip()
        if not raw:
            current_lines = []
            return
        idx = len(chunks)
        heading_path = " > ".join(heading_stack)
        content = normalize_markdown(raw)
        chunks.append(
            Chunk(
                chunk_id=f"{page.rel_path}::chunk-{idx:04d}",
                rel_path=page.rel_path,
                title=title,
                heading=current_heading,
                heading_path=heading_path,
                content=content,
                front_matter=page.front_matter,
                source_url=chunk_source_url(page, raw),
            )
        )
        current_lines = []

    for line in page.body.splitlines():
        match = HEADING_RE.match(line)
        if match:
            level = len(match.group(1))
            heading_text = match.group(2).strip()
            if level <= 2:
                flush()
                while len(heading_stack) >= level:
                    heading_stack.pop()
                heading_stack.append(heading_text)
                current_heading = heading_text
        current_lines.append(line)
    flush()
    return chunks


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        DROP TABLE IF EXISTS pages;
        DROP TABLE IF EXISTS chunks;
        DROP TABLE IF EXISTS chunks_fts;
        CREATE TABLE pages (
            rel_path TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            type TEXT NOT NULL,
            topic TEXT NOT NULL,
            component TEXT,
            level TEXT NOT NULL,
            status TEXT NOT NULL,
            reliability TEXT NOT NULL,
            source_type TEXT,
            source_url TEXT,
            last_checked TEXT,
            last_updated TEXT NOT NULL,
            owner TEXT NOT NULL,
            tags TEXT,
            front_matter_json TEXT NOT NULL
        );
        CREATE TABLE chunks (
            chunk_id TEXT PRIMARY KEY,
            rel_path TEXT NOT NULL REFERENCES pages(rel_path),
            title TEXT NOT NULL,
            heading TEXT NOT NULL,
            heading_path TEXT NOT NULL,
            content TEXT NOT NULL,
            type TEXT NOT NULL,
            topic TEXT NOT NULL,
            component TEXT,
            level TEXT NOT NULL,
            status TEXT NOT NULL,
            reliability TEXT NOT NULL,
            source_type TEXT,
            source_url TEXT,
            last_checked TEXT
        );
        CREATE VIRTUAL TABLE chunks_fts USING fts5(
            chunk_id UNINDEXED,
            rel_path UNINDEXED,
            title,
            heading,
            heading_path,
            content,
            type UNINDEXED,
            topic UNINDEXED,
            component UNINDEXED,
            level UNINDEXED,
            status UNINDEXED,
            reliability UNINDEXED,
            source_type UNINDEXED,
            source_url UNINDEXED,
            last_checked UNINDEXED,
            tokenize='unicode61'
        );
        CREATE INDEX idx_chunks_rel_path ON chunks(rel_path);
        CREATE INDEX idx_chunks_topic ON chunks(topic);
        CREATE INDEX idx_chunks_type ON chunks(type);
        CREATE INDEX idx_chunks_component ON chunks(component);
        CREATE INDEX idx_chunks_reliability ON chunks(reliability);
        CREATE INDEX idx_chunks_source_type ON chunks(source_type);
        """
    )


def insert_page(conn: sqlite3.Connection, page: Page) -> None:
    fm = page.front_matter
    conn.execute(
        """
        INSERT INTO pages VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            page.rel_path,
            front_matter_text(fm, "title"),
            front_matter_text(fm, "type"),
            front_matter_text(fm, "topic"),
            front_matter_text(fm, "component"),
            front_matter_text(fm, "level"),
            front_matter_text(fm, "status"),
            front_matter_text(fm, "reliability"),
            front_matter_text(fm, "source_type"),
            front_matter_text(fm, "source_url"),
            front_matter_text(fm, "last_checked"),
            front_matter_text(fm, "last_updated"),
            front_matter_text(fm, "owner"),
            front_matter_text(fm, "tags"),
            json.dumps(json_safe(fm), ensure_ascii=False, sort_keys=True),
        ),
    )


def insert_chunk(conn: sqlite3.Connection, chunk: Chunk) -> None:
    fm = chunk.front_matter
    row = (
        chunk.chunk_id,
        chunk.rel_path,
        chunk.title,
        chunk.heading,
        chunk.heading_path,
        chunk.content,
        front_matter_text(fm, "type"),
        front_matter_text(fm, "topic"),
        front_matter_text(fm, "component"),
        front_matter_text(fm, "level"),
        front_matter_text(fm, "status"),
        front_matter_text(fm, "reliability"),
        front_matter_text(fm, "source_type"),
        chunk.source_url,
        front_matter_text(fm, "last_checked"),
    )
    conn.execute("INSERT INTO chunks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)
    conn.execute("INSERT INTO chunks_fts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)


def build_index(wiki_root: Path, db_path: Path) -> tuple[int, int]:
    pages = read_pages(wiki_root)
    conn = connect(db_path)
    with conn:
        init_schema(conn)
        chunk_count = 0
        for page in pages:
            insert_page(conn, page)
            for chunk in split_chunks(page):
                insert_chunk(conn, chunk)
                chunk_count += 1
    conn.close()
    return len(pages), chunk_count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wiki-root", default="ai-infra-wiki", help="Wiki root directory")
    parser.add_argument("--db", default="wiki-index/ai_infra_wiki.sqlite", help="Output SQLite database")
    args = parser.parse_args()

    wiki_root = Path(args.wiki_root).resolve()
    db_path = Path(args.db).resolve()
    pages, chunks = build_index(wiki_root, db_path)
    print(f"wiki_index_built db={db_path} pages={pages} chunks={chunks}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
