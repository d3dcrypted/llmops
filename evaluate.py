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

def evaluate_cases(cases: list[Case]) -> dict:
    results = [score(case) for case in cases]
    count = len(results)
    if not count:
        raise ValueError("at least one case is required")
    return {
        "schema_version": 1,
        "case_count": count,
        "exact_match_rate": round(sum(r["exact_match"] for r in results) / count, 4),
        "mean_token_overlap": round(sum(r["token_overlap"] for r in results) / count, 4),
        "cases": results,
    }

def regression_passes(results: dict, min_exact_match_rate: float = 1.0,
                      min_token_overlap: float = 1.0) -> bool:
    return (results["exact_match_rate"] >= min_exact_match_rate and
            results["mean_token_overlap"] >= min_token_overlap)
