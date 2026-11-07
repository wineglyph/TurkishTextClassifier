"""Unit tests for preprocessing, inference validation, and server configuration."""

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

# Ensure src/model and src are available for import
import sys
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "src" / "model"))

from pipeline import preprocess_turkish_text
from predict import TurkishTextClassifierService
import serve


class TurkishPreprocessingUnitTests(unittest.TestCase):
    def test_turkish_dotted_and_dotless_i_lowercasing(self):
        # "İstanbul" -> "istanbul"
        self.assertEqual(preprocess_turkish_text("İstanbul"), "istanbul")
        # "ISIK" -> "ısık"
        self.assertEqual(preprocess_turkish_text("ISIK"), "ısık")

    def test_nfkc_and_whitespace_normalization(self):
        # Multiple spaces and tabs collapsed to single space, stripped
        raw = "   Bu   bir     deneme   metnidir.   "
        self.assertEqual(preprocess_turkish_text(raw), "bu bir deneme metnidir.")

        # Unicode NFKC normalization
        raw_unicode = "İSTANBUL\u00A0ve\u2002ANKARA"  # non-breaking spaces
        self.assertEqual(preprocess_turkish_text(raw_unicode), "istanbul ve ankara")


class InferenceValidationUnitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.service = TurkishTextClassifierService(model_dir=str(ROOT / "artifacts" / "model"))
        samples_path = ROOT / "data" / "manual_samples.json"
        with samples_path.open("r", encoding="utf-8") as f:
            cls.samples = json.load(f)

    def test_five_manual_samples_predictions_and_confidence(self):
        valid_labels = {"Soru", "Şikâyet", "Öneri"}
        test_samples = self.samples[:5]
        self.assertEqual(len(test_samples), 5)

        for sample in test_samples:
            text = sample["text"]
            res = self.service.predict(text)

            with self.subTest(sample_id=sample.get("id"), text=text):
                self.assertIn(res["prediction"], valid_labels)
                self.assertIsInstance(res["confidence"], float)
                self.assertGreaterEqual(res["confidence"], 0.0)
                self.assertLessEqual(res["confidence"], 1.0)
                self.assertIn("probabilities", res)
                self.assertEqual(set(res["probabilities"].keys()), valid_labels)


class ServerConfigurationUnitTests(unittest.TestCase):
    def test_default_host_is_localhost(self):
        self.assertEqual(serve.DEFAULT_HOST, "127.0.0.1")

    def test_parse_args_defaults(self):
        host, port = serve.parse_args([])
        self.assertEqual(host, "127.0.0.1")
        self.assertEqual(port, 8080)

    def test_parse_args_custom_host_and_port(self):
        host, port = serve.parse_args(["--host", "0.0.0.0", "--port", "9090"])
        self.assertEqual(host, "0.0.0.0")
        self.assertEqual(port, 9090)

    def test_parse_args_positional_port_compatibility(self):
        host, port = serve.parse_args(["8888"])
        self.assertEqual(host, "127.0.0.1")
        self.assertEqual(port, 8888)


if __name__ == "__main__":
    unittest.main()
