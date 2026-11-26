"""Deterministic input controls: classify, redact, record. No model call, no raw secrets."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re

# Each pattern is named, so a decision can say what it matched instead of "blocked".
INJECTION_PATTERNS: tuple[tuple[str, str], ...] = (
    ("instruction_override",
     r"\b(?:ignore|disregard|forget|override|bypass)\s+(?:all\s+|any\s+|the\s+)*"
     r"(?:previous|prior|earlier|above|system)\s+"
     r"(?:instruction|instructions|prompt|prompts|rule|rules|message|messages)\b"),
    ("instruction_override_it",
     r"\b(?:ignora|dimentica|tralascia|sovrascrivi|bypassa)\s+(?:\w+\s+){0,3}"
     r"(?:istruzioni|regole|indicazioni|comandi|prompt)\b"),
    ("prompt_exfiltration",
     r"\b(?:reveal|show|print|repeat|leak|dump)\s+(?:me\s+)?(?:your\s+|the\s+)?"
     r"(?:system\s+prompt|initial\s+prompt|hidden\s+rules|instructions)\b"),
    ("prompt_exfiltration_it",
     r"\b(?:rivela|mostra|ripeti|stampa)\s+(?:il\s+|le\s+|la\s+|i\s+)?"
     r"(?:prompt\s+di\s+sistema|istruzioni\s+di\s+sistema|tue\s+istruzioni|regole\s+interne)\b"),
    ("jailbreak_framing",
     r"\b(?:jailbreak|DAN\s+mode|developer\s+mode|no\s+restrictions|senza\s+restrizioni)\b"),
)
BLOCKING_REASONS = frozenset(name for name, _ in INJECTION_PATTERNS)

# Redaction errs towards over-redaction: a false positive costs a masked value,
# a false negative leaks one. Order matters, longer shapes first.
REDACTIONS: tuple[tuple[str, str, str], ...] = (
    ("email", r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b", "[REDACTED_EMAIL]"),
    ("iban", r"\b[A-Z]{2}\d{2}(?:\s?[A-Z0-9]{4}){2,7}(?:\s?[A-Z0-9]{1,3})?\b", "[REDACTED_IBAN]"),
    ("phone", r"(?:\+\d{1,3}[\s.-]?)?(?:3\d{2}|0\d{1,3})[\s.-]?\d{3,4}[\s.-]?\d{3,4}\b", "[REDACTED_PHONE]"),
    ("api_key", r"\b(?:sk|pk|ghp|gho|ghs|github_pat|xox[abprs])[-_][A-Za-z0-9_-]{16,}\b", "[REDACTED_API_KEY]"),
    ("aws_access_key", r"\bAKIA[0-9A-Z]{16}\b", "[REDACTED_API_KEY]"),
    ("jwt", r"\beyJ[\w-]{10,}\.[\w-]{10,}\.[\w-]{10,}\b", "[REDACTED_JWT]"),
)

@dataclass(frozen=True)
class Decision:
    allowed: bool
    redacted_text: str
    reasons: tuple[str, ...]

def inspect(text: str, audit: "AuditLog | None" = None) -> Decision:
    """Classify one input, return its redacted form, and optionally record the decision."""
    reasons: list[str] = []
    redacted = text
    for name, pattern, placeholder in REDACTIONS:
        redacted, hits = re.subn(pattern, placeholder, redacted)
        if hits:
            reasons.append(f"{name}_redacted")
    for name, pattern in INJECTION_PATTERNS:
        if re.search(pattern, text, re.I):
            reasons.append(name)
    decision = Decision(not (set(reasons) & BLOCKING_REASONS), redacted, tuple(reasons))
    if audit is not None:
        audit.record(text, decision)
    return decision

class AuditLog:
    """Append-only JSONL trail. It stores a hash of the input, never the input itself."""

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def record(self, text: str, decision: Decision) -> dict:
        row = {"schema_version": 1,
               "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
               "input_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
               "allowed": decision.allowed,
               "reasons": list(decision.reasons)}
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
        return row
