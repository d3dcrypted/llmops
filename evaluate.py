from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Case:
    case_id: str
    expected: str
    actual: str

def token_overlap(expected: str, actual: str) -> float:
    e, a = set(re.findall(r"\w+", expected.lower())), set(re.findall(r"\w+", actual.lower()))
    return len(e & a) / len(e) if e else 1.0

def score(case: Case) -> dict:
    return {"case_id": case.case_id, "exact_match": case.expected.strip() == case.actual.strip(),
            "token_overlap": round(token_overlap(case.expected, case.actual), 4)}
