import unittest
from pathlib import Path
from experiment import (DatasetRecord, LoraPlan, adapter_parameters, load_manifest, load_plan,
                        plan_summary, validate)

class ExperimentTests(unittest.TestCase):
    def test_manifest_contract(self):
        validate(DatasetRecord("synthetic-demo", "MIT", "a" * 64, 2))
    def test_rejects_missing_checksum(self):
        with self.assertRaises(ValueError): validate(DatasetRecord("x", "MIT", "bad", 1))
    def test_rejects_64_characters_that_are_not_hexadecimal(self):
        with self.assertRaises(ValueError): validate(DatasetRecord("x", "MIT", "z" * 64, 1))
    def test_rejects_non_spdx_license_and_uppercase_slug(self):
        with self.assertRaises(ValueError): validate(DatasetRecord("x", "not a licence", "a" * 64, 1))
        with self.assertRaises(ValueError): validate(DatasetRecord("X", "MIT", "a" * 64, 1))

    def test_adapter_parameters_follow_rank_and_layer_shape(self):
        plan = LoraPlan("synthetic-base", rank=16, target_modules=("q_proj",))
        layers = (("q_proj", 4096, 4096), ("embed_tokens", 32000, 4096))
        self.assertEqual(adapter_parameters(plan, layers), 16 * (4096 + 4096))
        summary = plan_summary(plan, layers)
        self.assertEqual(summary["base_parameters"], 4096 * 4096 + 32000 * 4096)
        self.assertEqual(summary["scaling"], 2.0)
        self.assertLess(summary["adapter_share"], 0.01)

    def test_rejects_a_plan_that_would_train_everything(self):
        with self.assertRaises(ValueError): LoraPlan("m", rank=0).validate()
        with self.assertRaises(ValueError): LoraPlan("m", target_modules=()).validate()
        with self.assertRaises(ValueError): LoraPlan("m", rank=1.5).validate()
        with self.assertRaises(ValueError):
            adapter_parameters(LoraPlan("m", rank=64, target_modules=("q_proj",)), (("q_proj", 8, 8),))

    def test_example_configuration_files_are_valid(self):
        root = Path(__file__).parents[1]
        self.assertEqual(load_plan(root / "experiment.example.json").rank, 16)
        self.assertEqual(load_manifest(root / "manifest.example.json").examples, 2)

if __name__ == "__main__": unittest.main()
