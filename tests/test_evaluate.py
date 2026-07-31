import unittest
from evaluate import Case, score

class EvaluationTests(unittest.TestCase):
    def test_exact_match(self):
        self.assertTrue(score(Case("x", "A", "A"))["exact_match"])
    def test_overlap(self):
        self.assertEqual(score(Case("x", "blue sky", "blue ocean"))["token_overlap"], 0.5)

if __name__ == "__main__": unittest.main()
