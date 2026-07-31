import unittest
from rag_core import chunk_text, lexical_retrieve

class RagCoreTests(unittest.TestCase):
    def test_chunks_keep_source_and_overlap(self):
        chunks = chunk_text("guide.md", "alpha beta gamma delta", size=3, overlap=1)
        self.assertEqual(chunks[0].source, "guide.md")
        self.assertIn("gamma", chunks[1].text)

    def test_retrieval_is_deterministic(self):
        chunks = chunk_text("a.md", "python deployment metrics", 10, 0)
        self.assertEqual(lexical_retrieve("metrics", chunks)[0].source, "a.md")

if __name__ == "__main__": unittest.main()
