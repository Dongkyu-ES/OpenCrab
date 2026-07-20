"""
Seed script: load the Ontology-Playground learn corpus into the OpenCrab stores.

Ingests seeds/ontology-playground/ as a foundational knowledge corpus:

  - vector store (ChromaDB): every article, chunked by ## section
  - graph: Document per track (resource), TextUnit per article (evidence),
    concept backbone from backbone.json (design patterns, core concepts,
    anti-patterns) with mentions/exemplifies/contains edges

Every write is an upsert keyed on stable IDs, so the script is idempotent —
re-run it after updating the corpus to refresh the stores.

Run with:
    python scripts/seed_ontology_playground.py [--dry-run] [--skip-vectors]
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.WARNING)

SEED_DIR = Path(__file__).parent.parent / "seeds" / "ontology-playground"
CORPUS_DIR = SEED_DIR / "corpus"
DISTILLED = SEED_DIR / "distilled" / "knowledge.md"
BACKBONE = SEED_DIR / "backbone.json"

SITE_URL = "https://microsoft.github.io/Ontology-Playground/#/learn"

_QUIZ_RE = re.compile(r"```quiz.*?```", re.DOTALL)
_EMBED_RE = re.compile(r"<ontology-embed[^>]*>\s*(</ontology-embed>)?")


def parse_article(path: Path) -> tuple[dict, str]:
    """Split a learn article into (frontmatter dict, cleaned body)."""
    raw = path.read_text(encoding="utf-8")
    meta: dict[str, str] = {}
    body = raw
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) == 3:
            for line in parts[1].splitlines():
                if ":" in line:
                    key, _, value = line.partition(":")
                    meta[key.strip()] = value.strip()
            body = parts[2]
    body = _QUIZ_RE.sub("", body)
    body = _EMBED_RE.sub("", body)
    return meta, body.strip()


def chunk_by_section(body: str) -> list[tuple[str, str]]:
    """Split article body into (section_title, text) chunks on ## headings."""
    chunks: list[tuple[str, str]] = []
    current_title = "intro"
    current: list[str] = []
    for line in body.splitlines():
        if line.startswith("## "):
            if "".join(current).strip():
                chunks.append((current_title, "\n".join(current).strip()))
            current_title = line[3:].strip()
            current = []
        else:
            current.append(line)
    if "".join(current).strip():
        chunks.append((current_title, "\n".join(current).strip()))
    return chunks


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "section"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="print planned writes, touch nothing")
    parser.add_argument("--skip-vectors", action="store_true", help="only build graph nodes/edges")
    args = parser.parse_args()

    backbone = json.loads(BACKBONE.read_text(encoding="utf-8"))
    tracks = backbone["tracks"]

    stats = {"chunks": 0, "nodes": 0, "edges": 0, "errors": 0}
    planned: list[str] = []

    if args.dry_run:
        builder = hybrid = None
    else:
        from opencrab.config import get_settings
        from opencrab.ontology.builder import OntologyBuilder
        from opencrab.ontology.query import HybridQuery
        from opencrab.stores.factory import (
            make_doc_store,
            make_graph_store,
            make_sql_store,
            make_vector_store,
        )

        cfg = get_settings()
        builder = OntologyBuilder(make_graph_store(cfg), make_doc_store(cfg), make_sql_store(cfg))
        hybrid = HybridQuery(make_vector_store(cfg), make_graph_store(cfg))

    def add_node(space: str, node_type: str, node_id: str, props: dict) -> None:
        if args.dry_run:
            planned.append(f"node  {space}/{node_type}  {node_id}")
            stats["nodes"] += 1
            return
        try:
            builder.add_node(space=space, node_type=node_type, node_id=node_id, properties=props)
            stats["nodes"] += 1
        except Exception as exc:
            stats["errors"] += 1
            print(f"  ! node {node_id}: {exc}")

    def add_edge(fs: str, fid: str, rel: str, ts: str, tid: str, props: dict | None = None) -> None:
        if args.dry_run:
            planned.append(f"edge  {fid} -{rel}-> {tid}")
            stats["edges"] += 1
            return
        try:
            builder.add_edge(from_space=fs, from_id=fid, relation=rel, to_space=ts, to_id=tid, properties=props or {})
            stats["edges"] += 1
        except Exception as exc:
            stats["errors"] += 1
            print(f"  ! edge {fid}-{rel}->{tid}: {exc}")

    def ingest(text: str, source_id: str, meta: dict) -> None:
        if args.dry_run or args.skip_vectors:
            stats["chunks"] += 1
            return
        result = hybrid.ingest(text=text, source_id=source_id, metadata=meta)
        status = result["stores"].get("chromadb", "?")
        if str(status).startswith("ok"):
            stats["chunks"] += 1
        else:
            stats["errors"] += 1
            print(f"  ! ingest {source_id}: {status}")

    # ------------------------------------------------------------------
    # 1. Concept backbone (topics, concepts, concept-concept edges)
    # ------------------------------------------------------------------
    print("[1/4] concept backbone")
    for topic in backbone["topics"]:
        add_node("concept", "Topic", topic["id"], {"name": topic["name"], "description": topic["description"]})

    concepts = {c["id"]: c for c in backbone["concepts"]}
    for con in backbone["concepts"]:
        add_node(
            "concept",
            "Concept",
            con["id"],
            {"name": con["name"], "kind": con["kind"], "description": con["description"], "corpus": backbone["corpus"]},
        )
    for edge in backbone["concept_edges"]:
        add_edge("concept", edge["from"], edge["relation"], "concept", edge["to"])

    # ------------------------------------------------------------------
    # 2. Corpus tracks: Document + TextUnit nodes, vector chunks
    # ------------------------------------------------------------------
    print("[2/4] corpus tracks")
    alias_index = [
        (con_id, [a.lower() for a in con.get("aliases", [])] + [con["name"].lower()])
        for con_id, con in concepts.items()
    ]

    for track_dir in sorted(p for p in CORPUS_DIR.iterdir() if p.is_dir()):
        track = track_dir.name
        meta_file = track_dir / "_meta.md"
        track_meta, _ = parse_article(meta_file) if meta_file.exists() else ({}, "")
        doc_id = f"doc-oplay-{track}"
        articles = sorted(p for p in track_dir.glob("*.md") if p.name != "_meta.md")
        add_node(
            "resource",
            "Document",
            doc_id,
            {
                "title": track_meta.get("title", track),
                "description": track_meta.get("description", ""),
                "corpus": backbone["corpus"],
                "track": track,
                "kind": track_meta.get("type", "path"),
                "articles": len(articles),
                "source_url": SITE_URL,
                "format": "markdown",
            },
        )

        track_concepts = tracks.get(track, {}).get("concepts", [])
        for article in articles:
            fm, body = parse_article(article)
            slug = fm.get("slug", article.stem)
            order = int(fm.get("order", 0) or 0)
            tu_id = f"tu-oplay-{track}-{slug}"
            url = f"{SITE_URL}/{slug}"
            add_node(
                "evidence",
                "TextUnit",
                tu_id,
                {
                    "text": fm.get("description", fm.get("title", slug)),
                    "title": fm.get("title", slug),
                    "corpus": backbone["corpus"],
                    "track": track,
                    "article": slug,
                    "order": order,
                    "source": url,
                },
            )
            add_edge("resource", doc_id, "contains", "evidence", tu_id)

            lowered = body.lower()
            mentioned = [cid for cid, aliases in alias_index if any(a in lowered for a in aliases)]
            for cid in mentioned:
                add_edge("evidence", tu_id, "mentions", "concept", cid)
            if order == 1:
                for cid in track_concepts:
                    add_edge("evidence", tu_id, "exemplifies", "concept", cid, {"reason": "track teaches this pattern"})

            for i, (section, text) in enumerate(chunk_by_section(body)):
                ingest(
                    text=f"# {fm.get('title', slug)} — {section}\n\n{text}",
                    source_id=f"oplay/{track}/{slug}#{i:02d}-{slugify(section)}",
                    meta={
                        "corpus": backbone["corpus"],
                        "track": track,
                        "article": slug,
                        "order": order,
                        "section": section,
                        "textunit_id": tu_id,
                        "url": url,
                    },
                )

    # ------------------------------------------------------------------
    # 3. Distilled knowledge document
    # ------------------------------------------------------------------
    print("[3/4] distilled digest")
    doc_id = "doc-oplay-distilled"
    tu_id = "tu-oplay-distilled"
    add_node(
        "resource",
        "Document",
        doc_id,
        {
            "title": "Ontology-Playground distilled knowledge",
            "description": "Structured digest: full learn tree, 12-pattern catalogue, per-track entity/relationship tables.",
            "corpus": backbone["corpus"],
            "kind": "digest",
            "format": "markdown",
        },
    )
    add_node(
        "evidence",
        "TextUnit",
        tu_id,
        {
            "text": "Distilled digest of the Ontology-Playground learn corpus (patterns, anti-patterns, per-track models).",
            "corpus": backbone["corpus"],
            "kind": "digest",
        },
    )
    add_edge("resource", doc_id, "contains", "evidence", tu_id)
    for cid in concepts:
        add_edge("evidence", tu_id, "describes", "concept", cid)

    distilled_body = DISTILLED.read_text(encoding="utf-8")
    for i, (section, text) in enumerate(chunk_by_section(distilled_body)):
        ingest(
            text=f"# Ontology design digest — {section}\n\n{text}",
            source_id=f"oplay/distilled#{i:02d}-{slugify(section)}",
            meta={"corpus": backbone["corpus"], "kind": "digest", "section": section, "textunit_id": tu_id},
        )

    # ------------------------------------------------------------------
    # 4. Summary
    # ------------------------------------------------------------------
    print("[4/4] done")
    mode = "dry-run" if args.dry_run else "applied"
    print(f"  {mode}: {stats['nodes']} nodes, {stats['edges']} edges, {stats['chunks']} chunks, {stats['errors']} errors")
    if args.dry_run:
        print("\n".join(f"  {p}" for p in planned[:20]))
        if len(planned) > 20:
            print(f"  ... and {len(planned) - 20} more")


if __name__ == "__main__":
    main()
