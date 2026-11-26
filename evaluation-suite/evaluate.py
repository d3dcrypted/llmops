from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Case:
    case_id: str
    expected: str
    actual: str

def token_scores(expected: str, actual: str) -> dict:
    """Precision, recall and F1 over token sets.

    Recall alone gives a wrong but chatty answer full marks, because the expected
    word is usually somewhere in the text. Precision is the half that notices the
    noise, so both are reported and F1 is the headline number.
    """
    expected_tokens = set(re.findall(r"\w+", expected.lower()))
    actual_tokens = set(re.findall(r"\w+", actual.lower()))
    overlap = len(expected_tokens & actual_tokens)
    precision = overlap / len(actual_tokens) if actual_tokens else float(not expected_tokens)
    recall = overlap / len(expected_tokens) if expected_tokens else 1.0
    total = precision + recall
    return {"precision": round(precision, 4), "recall": round(recall, 4),
            "f1": round(2 * precision * recall / total, 4) if total else 0.0}

def score(case: Case) -> dict:
    scores = token_scores(case.expected, case.actual)
    return {"case_id": case.case_id, "exact_match": case.expected.strip() == case.actual.strip(),
            "token_precision": scores["precision"], "token_recall": scores["recall"],
            "token_f1": scores["f1"]}

def evaluate_cases(cases: list[Case]) -> dict:
    results = [score(case) for case in cases]
    count = len(results)
    if not count:
        raise ValueError("at least one case is required")
    return {
        "schema_version": 2,
        "case_count": count,
        "exact_match_rate": round(sum(r["exact_match"] for r in results) / count, 4),
        "mean_token_f1": round(sum(r["token_f1"] for r in results) / count, 4),
        "mean_token_precision": round(sum(r["token_precision"] for r in results) / count, 4),
        "mean_token_recall": round(sum(r["token_recall"] for r in results) / count, 4),
        "cases": results,
    }

def regression_passes(results: dict, min_exact_match_rate: float = 1.0,
                      min_token_f1: float = 1.0) -> bool:
    return (results["exact_match_rate"] >= min_exact_match_rate and
            results["mean_token_f1"] >= min_token_f1)
