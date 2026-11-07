#!/usr/bin/env python3
"""Read-only packaging checks for TurkishTextClassifier.

This script does not train, fine-tune, edit datasets, or write model artifacts.
Run it from any working directory: python scripts/verify_project.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "artifacts/model/config.json",
    "artifacts/model/metadata.json",
    "artifacts/model/turkish_text_classifier.joblib",
    "artifacts/model/vectorizer.joblib",
    "artifacts/model/vocab.json",
    "data/turkish_text_dataset.csv",
    "data/turkish_text_dataset.jsonl",
    "data/train.csv",
    "data/test.csv",
    "data/manual_samples.json",
    "external_eval/synthetic_test.csv",
    "external_eval/results/predictions.csv",
    "external_eval/results/evaluation_metrics.json",
    "external_eval/results/confusion_matrix.png",
    "external_eval/results/ERROR_ANALYSIS.md",
    "external_eval/results/EVALUATION_REPORT.md",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def check_csv(path: Path) -> tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
        return True, f"{len(rows)} rows; UTF-8 CSV readable"
    except Exception as exc:  # report rather than conceal parse errors
        return False, f"{type(exc).__name__}: {exc}"


def main() -> int:
    failures: list[str] = []
    print(f"Project root: {ROOT}")

    for rel in sorted(EXPECTED):
        path = ROOT / rel
        if path.is_file():
            print(f"[PASS] required file: {rel} ({path.stat().st_size:,} bytes)")
        else:
            print(f"[FAIL] missing required file: {rel}")
            failures.append(f"missing: {rel}")

    for rel in (
        "data/turkish_text_dataset.csv",
        "data/train.csv",
        "data/test.csv",
        "external_eval/synthetic_test.csv",
        "external_eval/results/predictions.csv",
    ):
        path = ROOT / rel
        if not path.exists():
            continue
        ok, detail = check_csv(path)
        print(f"[{ 'PASS' if ok else 'FAIL' }] CSV {rel}: {detail}")
        if not ok:
            failures.append(f"invalid CSV: {rel}: {detail}")

    # Exercise the repository's own synthetic data validator.
    validator = ROOT / "external_eval/validate_dataset.py"
    if validator.is_file():
        proc = subprocess.run(
            [sys.executable, str(validator), "--project-root", str(ROOT)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        print("\n--- external_eval validator ---")
        print(proc.stdout.rstrip())
        if proc.stderr.strip():
            print(proc.stderr.rstrip(), file=sys.stderr)
        if proc.returncode:
            failures.append("external_eval/validate_dataset.py returned non-zero")

    # Validate the recorded predictions and aggregate metrics without rerunning inference.
    pred_path = ROOT / "external_eval/results/predictions.csv"
    metrics_path = ROOT / "external_eval/results/evaluation_metrics.json"
    if pred_path.is_file() and metrics_path.is_file():
        with pred_path.open("r", encoding="utf-8-sig", newline="") as f:
            pred_rows = list(csv.DictReader(f))
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        correct = sum(str(r.get("correct", "")).strip().lower() in {"true", "1"} for r in pred_rows)
        total = len(pred_rows)
        expected_correct = int(metrics.get("correct_predictions", -1))
        expected_total = int(metrics.get("total_examples", -1))
        ok = total == 450 and expected_total == total and correct == expected_correct
        print(f"[{ 'PASS' if ok else 'FAIL' }] stored evaluation results: {correct}/{total} correct; metrics say {expected_correct}/{expected_total}")
        if not ok:
            failures.append("stored predictions do not agree with evaluation_metrics.json")

    # Model load and one text-only smoke prediction. It is inference-only and read-only.
    if all((ROOT / p).is_file() for p in (
        "artifacts/model/config.json",
        "artifacts/model/turkish_text_classifier.joblib",
        "artifacts/model/vocab.json",
    )):
        before = {p: sha256(ROOT / p) for p in (
            "artifacts/model/config.json",
            "artifacts/model/metadata.json",
            "artifacts/model/turkish_text_classifier.joblib",
            "artifacts/model/vectorizer.joblib",
            "artifacts/model/vocab.json",
        ) if (ROOT / p).is_file()}
        try:
            sys.path.insert(0, str(ROOT / "src" / "model"))
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                from predict import TurkishTextClassifierService
                service = TurkishTextClassifierService(model_dir=str(ROOT / "artifacts" / "model"))
                smoke = service.predict("Siparişim ne zaman kargoya verilir?")
            print(f"[PASS] model load + text-only inference smoke: {smoke['prediction']} (confidence={smoke['confidence']})")
            for item in caught:
                if "InconsistentVersionWarning" in type(item.message).__name__:
                    print(f"[WARN] serialized sklearn/runtime version mismatch: {item.message}")
        except Exception as exc:
            failures.append(f"model load/inference smoke failed: {type(exc).__name__}: {exc}")
            print(f"[FAIL] model load/inference smoke: {type(exc).__name__}: {exc}")
        after = {p: sha256(ROOT / p) for p in before}
        unchanged = before == after
        print(f"[{ 'PASS' if unchanged else 'FAIL' }] model artifact SHA-256 unchanged by smoke check")
        if not unchanged:
            failures.append("model artifact hashes changed during smoke check")

    print("\n=== Verification summary ===")
    if failures:
        print(f"FAILED: {len(failures)} issue(s)")
        for item in failures:
            print(f" - {item}")
        return 1
    print("PASS: all required packaging checks completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
