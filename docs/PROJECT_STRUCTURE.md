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
│   ├── model/                 # Original sklearn model artifacts
│   └── reports/               # Training and manual test reports
├── data/
│   ├── raw/                   # Empty source-data staging directory
│   ├── turkish_text_dataset.csv
│   ├── turkish_text_dataset.jsonl
│   ├── train.csv
│   └── test.csv
├── docs/
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

The original `src/` and `artifacts/model/` locations are retained so legacy import and relative artifact paths continue to work. `models/`, `src/preprocessing/`, and `src/utils/` were not invented because the existing project does not use those locations. There is no separate validation split in the supplied source archive.

The two pre-existing `artifacts/dist/` archives were excluded from the repository. Python `__pycache__` bytecode was excluded as local generated noise.
```
