# Raw Sources Boundary

`raw-sources/` is the immutable source-of-truth layer for this AI Infra LLM Wiki.

Store here:

- official docs exported to Markdown or PDF
- papers, design docs, incident writeups, benchmark raw logs
- profiler traces, screenshots, and config snapshots

Rules:

1. Do not edit source content in place after ingestion. Add a new versioned file instead.
2. Keep filenames stable and append dates or versions when refreshing content.
3. Preserve raw benchmark outputs, trace artifacts, and deployment configs alongside summaries.
4. Let the wiki cite or summarize these files; do not treat generated wiki pages as the only evidence.
