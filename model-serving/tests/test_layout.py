import re
import unittest
from pathlib import Path

CREDENTIAL = re.compile(r"^\s*[A-Z0-9_]*(?:PASSWORD|SECRET|TOKEN|API_KEY)[A-Z0-9_]*\s*[:=]\s*(\S*)\s*$")


class LayoutTests(unittest.TestCase):
    def test_runtime_files_exist(self):
        root = Path(__file__).parents[1]
        for name in ("docker-compose.yml", "prometheus.yml"):
            self.assertTrue((root / name).is_file())

    def test_no_committed_credential_values(self):
        """A credential line may name a variable or reference the environment, never hold a value."""
        root = Path(__file__).parents[1]
        for name in ("docker-compose.yml", ".env.example"):
            for number, line in enumerate((root / name).read_text(encoding="utf-8").splitlines(), 1):
                match = CREDENTIAL.match(line)
                if not match:
                    continue
                value = match.group(1)
                self.assertTrue(
                    value == "" or value.startswith("${"),
                    f"{name}:{number} holds a credential value instead of a variable reference",
                )

if __name__ == "__main__": unittest.main()
