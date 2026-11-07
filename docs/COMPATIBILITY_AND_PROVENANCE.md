# Compatibility, Provenance, and Publication Notes

## Serialized model compatibility

The independent evaluation loaded `artifacts/model/turkish_text_classifier.joblib` and obtained predictions for all 450 synthetic examples. The runtime emitted scikit-learn `InconsistentVersionWarning`: the serialized estimators report version **1.9.1**, while the evaluation runtime was **1.8.0**. The pipeline loaded, but cross-version pickle/joblib compatibility is not guaranteed. `requirements.txt` pins scikit-learn 1.9.1 to match the artifact metadata observed in the warning. A clean rerun under that exact version was not performed during consolidation.

The evaluation environment used Python 3.13.5, scikit-learn 1.8.0, joblib 1.5.3, pandas 2.2.3, and NumPy 2.3.5. These are recorded evaluation-environment versions, not a formal complete build lock.

## Model files

The model directory contains:

- `turkish_text_classifier.joblib` — fitted scikit-learn pipeline and the default production inference artifact.
- `vectorizer.joblib` — separate fitted vectorizer artifact.
- `vocab.json`, `config.json`, and `metadata.json` — vocabulary and model metadata/configuration.

## Data provenance and licensing

The supplied repository contains generation code and locally stored corpora. The code is released under the MIT License. Confirm ownership and redistribution permissions for downstream uses.

## Removed derived files

The pre-existing distribution archives under `artifacts/dist/` and `__pycache__` bytecode files were omitted as machine-specific/derived files.
