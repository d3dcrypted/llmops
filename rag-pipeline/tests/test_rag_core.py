import tempfile
import unittest
from pathlib import Path
from rag_core import chunk_text, ingest_file, lexical_retrieve, retrieve_with_citations

class RagCoreTests(unittest.TestCase):
    def test_chunks_keep_source_and_overlap(self):
        chunks = chunk_text("guide.md", "alpha beta gamma delta", size=3, overlap=1)
        self.assertEqual(chunks[0].source, "guide.md")
        self.assertIn("gamma", chunks[1].text)

    def test_retrieval_is_deterministic(self):
        chunks = chunk_text("a.md", "python deployment metrics", 10, 0)
        self.assertEqual(lexical_retrieve("metrics", chunks)[0].source, "a.md")

    def test_retrieval_ignores_trailing_punctuation(self):
        chunks = chunk_text("guide.md", "python deployment metrics.", 10, 0)
        self.assertEqual([c.text for c in lexical_retrieve("metrics", chunks)],
                         ["python deployment metrics."])

    def test_common_terms_do_not_outrank_the_query_subject(self):
        chunks = (chunk_text("a.md", "the the the", 10, 0)
                  + chunk_text("b.md", "deployment guide", 10, 0)
                  + chunk_text("c.md", "the handbook", 10, 0))
        self.assertEqual(lexical_retrieve("the deployment", chunks)[0].source, "b.md")

    def test_ingestion_accepts_explicit_relative_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "guide.md").write_text("alpha beta", encoding="utf-8")
            self.assertEqual(ingest_file(root, "guide.md").strip(), "alpha beta")

    def test_ingestion_rejects_traversal_and_oversized_input(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "large.md").write_text("0123456789", encoding="utf-8")
            with self.assertRaises(ValueError): ingest_file(root, "../outside.md")
            with self.assertRaises(ValueError): ingest_file(root, "large.md", max_bytes=5)

    def test_ingestion_rejects_symlink(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "target.md").write_text("safe", encoding="utf-8")
            (root / "link.md").symlink_to(root / "target.md")
            with self.assertRaises(ValueError): ingest_file(root, "link.md")

    def test_citations_are_source_and_chunk_verifiable(self):
        chunks = chunk_text("guide.md", "python deployment metrics", 10, 0)
        citations = retrieve_with_citations("metrics", chunks)
        self.assertEqual(citations[0]["source"], "guide.md")
        self.assertEqual(citations[0]["chunk_index"], 0)
        self.assertEqual(citations[0]["text"], chunks[0].text)

if __name__ == "__main__": unittest.main()
