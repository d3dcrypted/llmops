"""Dependency-free RAG building blocks for an inspectable baseline."""
from dataclasses import dataclass
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
    candidate = (root / relative_path).resolve()
    base = root.resolve()
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

def lexical_retrieve(query: str, chunks: list[Chunk], top_k: int = 3) -> list[Chunk]:
    terms = set(re.findall(r"\w+", query.lower()))
    scored = [(sum(t in c.text.lower().split() for t in terms), c) for c in chunks]
    return [c for score, c in sorted(scored, key=lambda x: (-x[0], x[1].index))[:top_k] if score]

def retrieve_with_citations(query: str, chunks: list[Chunk], top_k: int = 3) -> list[dict]:
    """Return retrieved text plus stable source coordinates for verification."""
    return [{"source": c.source, "chunk_index": c.index, "text": c.text}
            for c in lexical_retrieve(query, chunks, top_k)]
