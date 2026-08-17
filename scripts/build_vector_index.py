#!/usr/bin/env python3
"""
Bharat Legal AI — Vector Index Builder
Loads legal knowledge entries, chunks documents, computes embeddings, and stores them in ChromaDB.

Run:
    python scripts/build_vector_index.py
"""

import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple
from dotenv import load_dotenv

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

from api.legal_knowledge import get_all_legal_entries
from api.embeddings import get_embedding_service
from api.vector_store import get_vector_store


def parse_legal_identifiers(entry: Dict[str, Any]) -> Tuple[str, str, str]:
    """
    Extract act, article, and section strings from legal knowledge entry metadata.
    """
    title = entry.get("title", "")
    category = entry.get("category", "")
    subcategory = entry.get("subcategory", "")
    entry_id = entry.get("id", "")

    act = ""
    article = ""
    section = ""

    # Check for Article
    art_match = re.search(r"Article\s+(\d+[A-Za-z]*)", title, re.IGNORECASE)
    if art_match:
        article = art_match.group(1)
        act = "Constitution of India"

    # Check for Section
    sec_match = re.search(r"Section\s+(\d+[A-Za-z]*)", title, re.IGNORECASE)
    if sec_match:
        section = sec_match.group(1)
        if subcategory == "ipc" or "ipc" in entry_id:
            act = "Indian Penal Code, 1860"
        elif subcategory == "crpc" or "crpc" in entry_id:
            act = "Code of Criminal Procedure, 1973"
        elif "cpc" in entry_id:
            act = "Code of Civil Procedure, 1908"

    # Infer Act by category if not set
    if not act:
        if category == "constitution":
            act = "Constitution of India"
        elif "domestic-violence" in entry_id:
            act = "Protection of Women from Domestic Violence Act, 2005"
        elif "hindu-marriage" in entry_id:
            act = "Hindu Marriage Act, 1955"
        elif "contract-law" in entry_id:
            act = "Indian Contract Act, 1872"
        elif "consumer" in entry_id:
            act = "Consumer Protection Act, 2019"
        elif "it-act" in entry_id or category == "cyber":
            act = "Information Technology Act, 2000"
        elif "rti" in entry_id or category == "rights":
            act = "Right to Information Act, 2005"
        elif "minimum-wages" in entry_id:
            act = "Code on Wages, 2019 / Minimum Wages Act, 1948"
        elif "epf-esi" in entry_id:
            act = "Employees' Provident Funds Act, 1952 / ESI Act, 1948"
        elif "workplace-harassment" in entry_id:
            act = "POSH Act, 2013 (Sexual Harassment at Workplace)"
        else:
            act = f"Indian Legal Code ({category.title()})"

    return act, article, section


def split_text_into_chunks(text: str, chunk_size: int = 500, chunk_overlap: int = 100) -> List[str]:
    """
    Split a document text into overlapping chunks, respecting sentence/paragraph boundaries when possible.
    """
    text = text.strip()
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = start + chunk_size

        if end >= text_len:
            chunks.append(text[start:].strip())
            break

        # Look for sentence boundary near the end (., \n, ?)
        split_point = -1
        lookback_zone = text[start + chunk_size // 2 : end]

        for punct in ["\n\n", "\n", ". ", "? ", "; "]:
            pos = lookback_zone.rfind(punct)
            if pos != -1:
                split_point = (start + chunk_size // 2) + pos + len(punct)
                break

        if split_point == -1 or split_point <= start:
            # Fall back to word boundary
            space_pos = text.rfind(" ", start, end)
            if space_pos > start:
                split_point = space_pos + 1
            else:
                split_point = end

        chunk = text[start:split_point].strip()
        if chunk:
            chunks.append(chunk)

        # Advance with overlap
        start = max(split_point - chunk_overlap, start + 1)

    return chunks


def build_index():
    print("=" * 65)
    print("      BHARAT LEGAL AI — VECTOR INDEX INGESTION PIPELINE")
    print("=" * 65)

    chunk_size = int(os.getenv("CHUNK_SIZE", "500"))
    chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "100"))

    print(f"\n[1/5] Loading legal knowledge base...")
    entries = get_all_legal_entries()
    print(f"      Loaded {len(entries)} legal entries.")

    print(f"\n[2/5] Creating documents and semantic chunks (size={chunk_size}, overlap={chunk_overlap})...")
    all_chunks: List[str] = []
    all_ids: List[str] = []
    all_metadatas: List[Dict[str, Any]] = []

    for entry in entries:
        entry_id = entry.get("id", "entry")
        title = entry.get("title", "")
        category = entry.get("category", "")
        subcategory = entry.get("subcategory", "")
        content = entry.get("content", "")
        explanation = entry.get("explanation", "")
        guidance = entry.get("guidance", [])
        steps = entry.get("steps", [])
        keywords = entry.get("keywords", [])

        act, article, section = parse_legal_identifiers(entry)

        # Build comprehensive document text
        doc_parts = [
            f"Title: {title}",
            f"Statutory Act / Source: {act}",
        ]
        if article:
            doc_parts.append(f"Article: {article}")
        if section:
            doc_parts.append(f"Section: {section}")

        doc_parts.append(f"Legal Content: {content}")
        doc_parts.append(f"Legal Explanation: {explanation}")

        if guidance:
            doc_parts.append("Practical Guidance:\n" + "\n".join(f"- {g}" for g in guidance))
        if steps:
            doc_parts.append("Procedural Steps:\n" + "\n".join(f"{i+1}. {s}" for i, s in enumerate(steps)))
        if keywords:
            doc_parts.append("Keywords: " + ", ".join(keywords))

        full_doc_text = "\n\n".join(doc_parts)

        # Chunk the document
        chunks = split_text_into_chunks(full_doc_text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

        for i, chunk_text in enumerate(chunks):
            chunk_id = f"{entry_id}#chunk_{i}"
            meta = {
                "entry_id": entry_id,
                "title": title,
                "category": category,
                "subcategory": subcategory,
                "act": act,
                "article": article,
                "section": section,
                "source": act or title,
                "chunk_index": i,
                "total_chunks": len(chunks),
                "language": "en",
            }
            all_ids.append(chunk_id)
            all_chunks.append(chunk_text)
            all_metadatas.append(meta)

    print(f"      Total Documents: {len(entries)}")
    print(f"      Total Chunks:    {len(all_chunks)}")
    avg_len = sum(len(c) for c in all_chunks) // len(all_chunks) if all_chunks else 0
    print(f"      Average Chunk Size: {avg_len} characters")

    print(f"\n[3/5] Loading Multilingual Embedding Model...")
    embedding_service = get_embedding_service()
    model_info = embedding_service.get_model_info()
    print(f"      Model: {model_info['model_name']}")

    print(f"\n[4/5] Generating Vector Embeddings for {len(all_chunks)} chunks...")
    embeddings = embedding_service.embed_texts(all_chunks, batch_size=32)
    dim = len(embeddings[0]) if embeddings else 0
    print(f"      Generated {len(embeddings)} embeddings (dimension={dim}).")

    print(f"\n[5/5] Indexing into Persistent ChromaDB Vector Store...")
    vector_store = get_vector_store()
    vector_store.clear_collection()
    vector_store.add_documents(
        ids=all_ids,
        texts=all_chunks,
        embeddings=embeddings,
        metadatas=all_metadatas,
    )

    stats = vector_store.get_collection_stats()
    print("\n" + "=" * 65)
    print("      INDEXING SUMMARY")
    print("=" * 65)
    print(f"  • Collection Name:     {stats['collection_name']}")
    print(f"  • Storage Path:        {stats['persist_directory']}")
    print(f"  • Indexed Vectors:     {stats['total_chunks']}")
    print(f"  • Embedding Model:     {model_info['model_name']} ({dim}D)")
    print(f"  • Status:              READY FOR RAG RETRIEVAL")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    build_index()
