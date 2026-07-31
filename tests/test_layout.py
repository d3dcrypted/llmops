import unittest
from pathlib import Path

class LayoutTests(unittest.TestCase):
    def test_runtime_files_exist(self):
        root = Path(__file__).parents[1]
        for name in ("docker-compose.yml", "prometheus.yml"):
            self.assertTrue((root / name).is_file())

if __name__ == "__main__": unittest.main()
