import unittest
from evaluate import Case, evaluate_cases, regression_passes, score, token_scores

class EvaluationTests(unittest.TestCase):
    def test_exact_match(self):
        self.assertTrue(score(Case("x", "A", "A"))["exact_match"])
    def test_partial_overlap(self):
        scores = score(Case("x", "blue sky", "blue ocean"))
        self.assertEqual(scores["token_precision"], 0.5)
        self.assertEqual(scores["token_recall"], 0.5)
        self.assertEqual(scores["token_f1"], 0.5)

    def test_wrong_but_verbose_answer_does_not_score_full_marks(self):
        """The regression this metric has to catch: the expected word appears, the answer is wrong."""
        wrong = Case("x", "Paris", "No, it is not Paris, it is Lyon")
        self.assertEqual(score(wrong)["token_recall"], 1.0)
        self.assertLess(score(wrong)["token_f1"], 0.5)
        self.assertFalse(regression_passes(evaluate_cases([wrong])))

    def test_negation_is_not_detected(self):
        """Known limit of token overlap, kept executable: an answer that says the opposite scores high."""
        scores = token_scores("the backup is not encrypted", "the backup is encrypted")
        self.assertGreater(scores["f1"], 0.85)

    def test_evaluate_cases_returns_aggregate_metrics(self):
        results = evaluate_cases([Case("a", "yes", "yes"), Case("b", "blue sky", "blue ocean")])
        self.assertEqual(results["schema_version"], 2)
        self.assertEqual(results["case_count"], 2)
        self.assertEqual(results["exact_match_rate"], 0.5)
        self.assertEqual(results["mean_token_f1"], 0.75)

    def test_regression_gate_is_explicit(self):
        results = evaluate_cases([Case("a", "yes", "yes")])
        self.assertTrue(regression_passes(results, min_exact_match_rate=1.0, min_token_f1=1.0))
        self.assertFalse(regression_passes(results, min_exact_match_rate=1.1, min_token_f1=1.0))
        self.assertFalse(regression_passes(results, min_exact_match_rate=1.0, min_token_f1=1.1))

if __name__ == "__main__": unittest.main()
