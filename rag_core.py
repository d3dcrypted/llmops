"""Dependency-free RAG building blocks for an inspectable baseline."""
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Chunk:
    source: str
    index: int
    text: str

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
