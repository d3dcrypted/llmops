"""Dependency-free RAG building blocks for an inspectable baseline."""
from dataclasses import dataclass
import math
from pathlib import Path
import re

@dataclass(frozen=True)
class Chunk:
    source: str
    index: int
    text: str

def ingest_file(root: Path, relative_path: str, max_bytes: int = 1_000_000) -> str:
    """Read one explicitly selected UTF-8 file below root, with safe bounds."""
    if max_bytes <= 0 or Path(relative_path).is_absolute():
        raise ValueError("relative path and positive max_bytes required")
    base = root.resolve()
    selected = root / relative_path
    if selected.is_symlink():
        raise ValueError("symlink input is not allowed")
    candidate = selected.resolve()
    if candidate != base and base not in candidate.parents:
        raise ValueError("path escapes root")
    if candidate.is_symlink() or not candidate.is_file():
        raise ValueError("regular file required")
    if candidate.stat().st_size > max_bytes:
        raise ValueError("input exceeds max_bytes")
    return candidate.read_text(encoding="utf-8")

def chunk_text(source: str, text: str, size: int = 500, overlap: int = 50) -> list[Chunk]:
    if size <= 0 or overlap < 0 or overlap >= size:
        raise ValueError("require size > overlap >= 0")
    words = re.findall(r"\S+", text)
    step = size - overlap
    return [Chunk(source, i // step, " ".join(words[i:i + size]))
            for i in range(0, len(words), step) if words[i:i + size]]

def _tokens(text: str) -> list[str]:
    """One tokenizer for queries and chunks, so trailing punctuation cannot break a match."""
    return re.findall(r"\w+", text.lower())

def lexical_retrieve(query: str, chunks: list[Chunk], top_k: int = 3) -> list[Chunk]:
    """Rank chunks by inverse-document-frequency weighted term match.

    Weighting is the point: an unweighted count makes a word that appears in every
    chunk worth as much as the term the query is actually about.
    """
    if top_k <= 0:
        raise ValueError("top_k must be positive")
    terms = set(_tokens(query))
    if not terms:
        return []
    document_terms = [set(_tokens(chunk.text)) for chunk in chunks]
    total = len(chunks)
    scored = []
    for chunk, words in zip(chunks, document_terms):
        matched = terms & words
        if not matched:
            continue
        score = sum(math.log(1 + total / sum(term in other for other in document_terms))
                    for term in matched)
        scored.append((-score, chunk.source, chunk.index, chunk))
    scored.sort(key=lambda row: row[:3])
    return [row[3] for row in scored[:top_k]]

def retrieve_with_citations(query: str, chunks: list[Chunk], top_k: int = 3) -> list[dict]:
    """Return retrieved text plus stable source coordinates for verification."""
    return [{"schema_version": 1, "source": c.source, "chunk_index": c.index, "text": c.text}
            for c in lexical_retrieve(query, chunks, top_k)]
