import unittest
from experiment import DatasetRecord, validate

class ExperimentTests(unittest.TestCase):
    def test_manifest_contract(self):
        validate(DatasetRecord("synthetic-demo", "MIT", "a" * 64, 2))
    def test_rejects_missing_checksum(self):
        with self.assertRaises(ValueError): validate(DatasetRecord("x", "MIT", "bad", 1))

if __name__ == "__main__": unittest.main()
