# Changelog

All notable project packaging and evaluation changes are recorded here.

## 1.1.0 — Removed EVREN integration

- Removed EVREN integration scripts, platform probes, and EVREN documentation.
- Moved HTTP inference microservice to `src/serve.py`.
- Removed PyTorch export layer and runtime dependency (`torch`), standardizing on scikit-learn.
- Updated documentation and verification tools.

## 1.0.0 — Initial release

- Bundled TurkishTextClassifier source code, training and preprocessing pipeline.
- Included complete corpus, train/test splits, and manually prepared examples.
- Included fitted scikit-learn pipeline, vocabulary, model config, and evaluation reports.
- Added independent 450-example synthetic evaluation benchmark with recorded predictions and error analysis.
- Added reusable integrity/smoke-check utilities and tests.
