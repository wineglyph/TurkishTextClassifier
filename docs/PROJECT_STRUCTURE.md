# Project Structure

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
│   ├── model/                 # Original sklearn + PyTorch model artifacts
│   └── reports/               # Original training/manual/EVREN reports
├── data/
│   ├── raw/                   # Empty source-data staging directory
│   ├── turkish_text_dataset.csv
│   ├── turkish_text_dataset.jsonl
│   ├── train.csv
│   └── test.csv
├── docs/
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

The original `src/` and `artifacts/model/` locations are retained so legacy import and relative artifact paths continue to work. `models/`, `src/preprocessing/`, and `src/utils/` were not invented because the existing project does not use those locations. There is no separate validation split in the supplied source archive.

The two pre-existing `artifacts/dist/` archives were excluded from the consolidated folder because they duplicate the model files already retained under `artifacts/model/`; `src/evren/package_model.py` remains available to rebuild EVREN distribution bundles when needed. Python `__pycache__` bytecode was excluded as local generated noise.
```
