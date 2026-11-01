# TurkishTextClassifier — Final Consolidation Manifest

**Package:** `TurkishTextClassifier/`  
**Consolidation date:** 2026-11-01  
**Model version:** 1.0.0 (original artifacts retained)  
**Dataset/evaluation additions:** independent synthetic evaluation v1.0.0 and recorded results

## Delivery summary

The consolidated folder contains **53 regular files** (including this manifest and `SHA256SUMS.txt`). It is organized as one root directory named `TurkishTextClassifier/` and preserves the original project import/artifact paths.

The original uploaded archive contained 33 regular files. Of these, 29 are represented in this consolidation: 26 were retained byte-for-byte and the root `README.md`, `docs/MODEL_CARD.md`, and `docs/EVREN_INTEGRATION.md` were deliberately updated with expanded instructions and accuracy/licensing/compatibility caveats. Four derived/cache files were omitted: two old model-only distribution bundles under `artifacts/dist/` and two Python `__pycache__` bytecode files. The original package-builder source remains at `src/evren/package_model.py`.

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

All seven files under `artifacts/model/` are included:

- `config.json`
- `metadata.json`
- `turkish_text_classifier.joblib` — fitted scikit-learn pipeline and default production inference artifact
- `turkish_text_classifier.pt` — PyTorch state dictionary
- `turkish_text_classifier_full.pt` — full serialized PyTorch module
- `vectorizer.joblib`
- `vocab.json`

Original model artifacts were hash-checked against the evaluation integrity record and the uploaded archive. No weight files were edited, retrained, or replaced. The existing source paths remain intact.

## Original reports and integration

- `artifacts/reports/evaluation_report.json`
- `artifacts/reports/confusion_matrix.txt`
- `artifacts/reports/manual_test_results.json`
- `artifacts/reports/evren_ecosystem_verification.json`
- `src/evren/evren_api_check.py`
- `src/evren/package_model.py`
- `src/evren/serve.py`
- `docs/EVREN_INTEGRATION.md`

The EVREN report is historical. This consolidation did not publish or register the model with EVREN.

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
│   ├── EVREN_INTEGRATION.md
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
│   ├── evren/
│   └── model/
├── tests/
│   └── test_project_smoke.py
├── run_demo.py
└── test_samples_20.json
```

## Verification results

- Synthetic dataset validator: **PASS** — 450 UTF-8 rows; class/domain/style balance correct; no empty text; no within-set exact duplicates; no exact or punctuation-normalized overlap against accessible project source texts.
- Project verification script: **PASS** — required files, CSVs, stored predictions/metrics, model loading, text-only inference smoke, and model-artifact hashes.
- Standard-library tests: **4/4 PASS**.
- CLI inference: **PASS** for default scikit-learn and optional PyTorch backends.
- Local HTTP API: **PASS** for `/health` and `/inference/predict`.
- Internal Markdown relative links: verified during final packaging.
- Confusion-matrix PNG: valid PNG, 1213 × 1062 pixels.
- Secret-pattern scan: no API keys, passwords, private keys, email addresses, Turkish phone-number patterns, or IBAN patterns found in the checked source/data files. Pattern scans are not a universal security guarantee.
- Largest individual file: below 1 MB; no file requires Git LFS under GitHub's ordinary 100 MB single-file limit.
- Model and original data: original hashes match; no model weights or original datasets modified.

### Known warnings and exclusions

1. No `LICENSE` file was present. The model metadata contains an MIT label, but no complete legal license or data-rights authorization was supplied. A `LICENSE` file has intentionally **not** been invented. Confirm rights before public GitHub release.
2. The separate validation split is missing; `data/raw/` is empty.
3. Scikit-learn emitted `InconsistentVersionWarning` because the artifact reports 1.9.1 and the available runtime is 1.8.0. The model loaded and inference worked, but compatibility is not fully certified. The pin in `requirements.txt` matches the artifact warning; a clean 1.9.1 install/rerun was not performed.
4. The two model-only bundles formerly under `artifacts/dist/` are not duplicated in this package. They can be recreated using the retained `src/evren/package_model.py`. Python bytecode caches are also excluded.
5. The temporary workspace-only files `build_external_eval.py`, `blind_review_map.json`, and `blind_review_audit_summary.json` are not packaged. The builder uses a non-portable absolute workspace path and has an adjudication block that copies gold labels; the blind map duplicates text already in the CSV, while the summary contains only aggregate counts and no per-example decisions. The finalized dataset, validation script, quality report, and evaluation outputs are included instead.
6. The independent benchmark is synthetic and does not establish real-world production accuracy.

## GitHub readiness

The project is organized for a local Git initialization and review. No GitHub repository was created and no push was performed. Before a public push, obtain a rights-holder-approved license/attribution statement for source, model, and datasets; review any third-party rights; and decide whether the historical EVREN verification report should remain public. No bundled individual file exceeds 100 MB, so Git LFS is not currently required by file size.

## Checksums

`SHA256SUMS.txt` contains SHA-256 hashes for every regular file in this directory except itself. Verify from this directory with:

```bash
sha256sum -c SHA256SUMS.txt
```
