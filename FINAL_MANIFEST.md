# TurkishTextClassifier — Final Consolidation Manifest

**Package:** `TurkishTextClassifier/`  
**Consolidation date:** 2026-11-01  
**Model version:** 1.0.0 (original artifacts retained)  
**Dataset/evaluation additions:** independent synthetic evaluation v1.0.0 and recorded results

## Delivery summary

The consolidated folder contains **53 regular files** (including this manifest and `SHA256SUMS.txt`). It is organized as one root directory named `TurkishTextClassifier/` and preserves the original project import/artifact paths.

The original uploaded archive contained 33 regular files. Of these, 29 are represented in this consolidation: 26 were retained byte-for-byte and the root `README.md` and `docs/MODEL_CARD.md` were updated with expanded instructions and accuracy/licensing/compatibility caveats. Four derived/cache files were omitted: two old model-only distribution bundles under `artifacts/dist/` and two Python `__pycache__` bytecode files.

## Original data inventory

| File | Rows/items | Status |
|---|---:|---|
| `data/turkish_text_dataset.csv` | 1,922 | Included; original bytes preserved |
| `data/turkish_text_dataset.jsonl` | 1,922 | Included; original bytes preserved |
| `data/train.csv` | 1,537 | Included; original bytes preserved |
| `data/test.csv` | 385 | Included; original bytes preserved |
| `test_samples_20.json` | 25 | Included; original bytes preserved (filename is historical and understates count) |
| `artifacts/reports/manual_test_results.json` | 25 results | Included; original bytes preserved |

The project has no separate validation split. `data/raw/` was empty in the source archive and is retained with `.gitkeep` only. Original corpus distribution: 756 `Soru`, 632 `Şikâyet`, and 534 `Öneri`.

## Model artifacts

All files under `artifacts/model/` are included:

- `config.json`
- `metadata.json`
- `turkish_text_classifier.joblib` — fitted scikit-learn pipeline and default production inference artifact
- `vectorizer.joblib`
- `vocab.json`

Original model artifacts were hash-checked against the evaluation integrity record and the uploaded archive. No weight files were edited, retrained, or replaced. The existing source paths remain intact.

## Original reports and integration

- `artifacts/reports/evaluation_report.json`
- `artifacts/reports/confusion_matrix.txt`
- `artifacts/reports/manual_test_results.json`
- `src/serve.py`

## Independent synthetic evaluation inventory

`external_eval/` is included in full:

- `synthetic_test.csv` — 450 examples, 150 per class
- `README.md`
- `QUALITY_REPORT.md`
- `GENERATION_NOTES.md`
- `dataset_metadata.json`
- `validate_dataset.py`
- `results/predictions.csv` — 450 model predictions
- `results/evaluation_metrics.json`
- `results/confusion_matrix.png`
- `results/ERROR_ANALYSIS.md` — all 83 recorded errors
- `results/EVALUATION_REPORT.md`

Recorded synthetic result: 367/450 correct (81.56% accuracy), 83 incorrect, 81.07% macro F1, and 81.07% weighted F1. The scikit-learn serialization warning (saved under 1.9.1; evaluation runtime 1.8.0) is documented. No successful clean rerun under 1.9.1 is claimed.

**Label-review caveat:** an earlier working summary reports 450/450 agreement in a text-only label review, but per-example review decisions were not preserved. The temporary builder's adjudication code copies the existing gold labels. Therefore, the claimed independent agreement cannot be independently verified from the retained evidence; `external_eval/QUALITY_REPORT.md` now states this limitation.

## Documentation and developer files

- `README.md` — complete project overview, installation, CLI, Python and API usage, evaluation summary, confusion matrix, and limitations
- `CHANGELOG.md`
- `requirements.txt` — pins scikit-learn 1.9.1 to match the serialization version reported by the stored pipeline
- `.gitignore`
- `.env.example` — contains no credential values
- `docs/MODEL_CARD.md`
- `docs/DATASET_CARD.md`
- `docs/INSTALLATION.md`
- `docs/PROJECT_STRUCTURE.md`
- `docs/COMPATIBILITY_AND_PROVENANCE.md`
- `scripts/verify_project.py`
- `tests/test_project_smoke.py`
- `SHA256SUMS.txt`

## Exact directory structure

```text
TurkishTextClassifier/
├── README.md
├── CHANGELOG.md
├── requirements.txt
├── .gitignore
├── .env.example
├── SHA256SUMS.txt
├── FINAL_MANIFEST.md
├── artifacts/
│   ├── model/
│   └── reports/
├── data/
│   ├── raw/
│   ├── turkish_text_dataset.csv
│   ├── turkish_text_dataset.jsonl
│   ├── train.csv
│   └── test.csv
├── docs/
│   ├── COMPATIBILITY_AND_PROVENANCE.md
│   ├── DATASET_CARD.md
│   ├── INSTALLATION.md
│   ├── MODEL_CARD.md
│   └── PROJECT_STRUCTURE.md
├── external_eval/
│   ├── synthetic_test.csv
│   ├── README.md
│   ├── QUALITY_REPORT.md
│   ├── GENERATION_NOTES.md
│   ├── dataset_metadata.json
│   ├── validate_dataset.py
│   └── results/
│       ├── predictions.csv
│       ├── evaluation_metrics.json
│       ├── confusion_matrix.png
│       ├── ERROR_ANALYSIS.md
│       └── EVALUATION_REPORT.md
├── scripts/
│   └── verify_project.py
├── src/
│   ├── dataset/
│   ├── model/
│   └── serve.py
├── tests/
│   └── test_project_smoke.py
├── run_demo.py
└── test_samples_20.json
```

## Verification results

- Synthetic dataset validator: **PASS** — 450 UTF-8 rows; class/domain/style balance correct; no empty text; no within-set exact duplicates; no exact or punctuation-normalized overlap against accessible project source texts.
- Project verification script: **PASS** — required files, CSVs, stored predictions/metrics, model loading, text-only inference smoke, and model-artifact hashes.
- Standard-library tests: **4/4 PASS**.
- CLI inference: **PASS** for scikit-learn backend.
- Local HTTP API: **PASS** for `/health` and `/inference/predict`.
- Internal Markdown relative links: verified during final packaging.
- Confusion-matrix PNG: valid PNG, 1213 × 1062 pixels.
- Secret-pattern scan: no API keys, passwords, private keys, email addresses, Turkish phone-number patterns, or IBAN patterns found in the checked source/data files. Pattern scans are not a universal security guarantee.
- Largest individual file: below 1 MB; no file requires Git LFS under GitHub's ordinary 100 MB single-file limit.
- Model and original data: original hashes match; no model weights or original datasets modified.

### Known warnings and exclusions

1. The separate validation split is missing; `data/raw/` is empty.
2. Scikit-learn emitted `InconsistentVersionWarning` because the artifact reports 1.9.1 and the available runtime is 1.8.0. The model loaded and inference worked, but compatibility is not fully certified. The pin in `requirements.txt` matches the artifact warning; a clean 1.9.1 install/rerun was not performed.
3. The two model-only bundles formerly under `artifacts/dist/` are not duplicated in this package. Python bytecode caches are also excluded.
4. The temporary workspace-only files `build_external_eval.py`, `blind_review_map.json`, and `blind_review_audit_summary.json` are not packaged. The builder uses a non-portable absolute workspace path and has an adjudication block that copies gold labels; the blind map duplicates text already in the CSV, while the summary contains only aggregate counts and no per-example decisions. The finalized dataset, validation script, quality report, and evaluation outputs are included instead.
5. The independent benchmark is synthetic and does not establish real-world production accuracy.

## GitHub readiness

The project is organized for GitHub release under the MIT License.

## Checksums

`SHA256SUMS.txt` contains SHA-256 hashes for every regular file in this directory except itself. Verify from this directory with:

```bash
sha256sum -c SHA256SUMS.txt
```
