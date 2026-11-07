"""Standard-library structural tests; no model training or dataset mutation."""
import csv
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ProjectSmokeTests(unittest.TestCase):
    def test_required_model_artifacts_exist(self):
        for rel in (
            "artifacts/model/turkish_text_classifier.joblib",
            "artifacts/model/vectorizer.joblib",
            "artifacts/model/vocab.json",
            "artifacts/model/config.json",
            "artifacts/model/metadata.json",
        ):
            with self.subTest(path=rel):
                self.assertTrue((ROOT / rel).is_file())

    def test_original_data_counts(self):
        expectations = {
            "data/turkish_text_dataset.csv": 1922,
            "data/train.csv": 1537,
            "data/test.csv": 385,
        }
        for rel, expected in expectations.items():
            with self.subTest(path=rel):
                with (ROOT / rel).open(encoding="utf-8-sig", newline="") as f:
                    self.assertEqual(len(list(csv.DictReader(f))), expected)

    def test_synthetic_test_is_balanced(self):
        path = ROOT / "external_eval/synthetic_test.csv"
        with path.open(encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 450)
        labels = {label: sum(r["gold_label"] == label for r in rows) for label in ("Soru", "Şikâyet", "Öneri")}
        self.assertEqual(labels, {"Soru": 150, "Şikâyet": 150, "Öneri": 150})

    def test_evaluation_predictions_and_metrics(self):
        with (ROOT / "external_eval/results/predictions.csv").open(encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
        metrics = json.loads((ROOT / "external_eval/results/evaluation_metrics.json").read_text(encoding="utf-8"))
        self.assertEqual(len(rows), 450)
        self.assertEqual(sum(r["correct"].lower() == "true" for r in rows), 367)
        self.assertEqual(metrics["incorrect_predictions"], 83)


if __name__ == "__main__":
    unittest.main()
