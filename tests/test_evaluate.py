import unittest
from evaluate import Case, evaluate_cases, regression_passes, score

class EvaluationTests(unittest.TestCase):
    def test_exact_match(self):
        self.assertTrue(score(Case("x", "A", "A"))["exact_match"])
    def test_overlap(self):
        self.assertEqual(score(Case("x", "blue sky", "blue ocean"))["token_overlap"], 0.5)

    def test_evaluate_cases_returns_aggregate_metrics(self):
        results = evaluate_cases([Case("a", "yes", "yes"), Case("b", "blue sky", "blue ocean")])
        self.assertEqual(results["case_count"], 2)
        self.assertEqual(results["exact_match_rate"], 0.5)
        self.assertEqual(results["mean_token_overlap"], 0.75)

    def test_regression_gate_is_explicit(self):
        results = evaluate_cases([Case("a", "yes", "yes")])
        self.assertTrue(regression_passes(results, min_exact_match_rate=1.0, min_token_overlap=1.0))
        self.assertFalse(regression_passes(results, min_exact_match_rate=1.1, min_token_overlap=1.0))

if __name__ == "__main__": unittest.main()
