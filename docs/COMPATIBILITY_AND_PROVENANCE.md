# Compatibility, Provenance, and Publication Notes

## Serialized model compatibility

The independent evaluation loaded `artifacts/model/turkish_text_classifier.joblib` and obtained predictions for all 450 synthetic examples. The runtime emitted scikit-learn `InconsistentVersionWarning`: the serialized estimators report version **1.9.1**, while the evaluation runtime was **1.8.0**. The pipeline loaded, but cross-version pickle/joblib compatibility is not guaranteed. `requirements.txt` pins scikit-learn 1.9.1 to match the artifact metadata observed in the warning. A clean rerun under that exact version was not performed during consolidation.

The evaluation environment used Python 3.13.5, scikit-learn 1.8.0, PyTorch 2.10.0+cpu, joblib 1.5.3, pandas 2.2.3, and NumPy 2.3.5. These are recorded evaluation-environment versions, not a formal complete build lock.

## Model files

The source archive contains all of the following, all retained byte-for-byte:

- `turkish_text_classifier.joblib` — fitted scikit-learn pipeline and the default production inference artifact.
- `turkish_text_classifier.pt` — PyTorch state dictionary used by the optional PyTorch inference backend.
- `turkish_text_classifier_full.pt` — full serialized PyTorch module.
- `vectorizer.joblib` — separate fitted vectorizer artifact.
- `vocab.json`, `config.json`, and `metadata.json` — vocabulary and model metadata/configuration.

## Data provenance and licensing

The supplied repository contains generation code and locally stored corpora, but no signed/explicit data-rights grant, attribution list for all source material, or repository `LICENSE` file. The model metadata says `MIT`; that field does not establish the licensing status of the source code, original corpus, or every bundled artifact. Confirm ownership and redistribution permissions before making the repository public. Do not add a license file until the relevant rights holder has authorized it.

## EVREN status

The repository contains EVREN compatibility scripts, model packaging metadata, a local HTTP service, and a prior API verification report. This consolidation did not register, publish, or upload the model to EVREN. The report is retained as historical project material and should not be interpreted as proof of current platform availability or successful publication.

## Removed derived files

The two pre-existing archives under `artifacts/dist/` were not copied into this consolidated repository because they are duplicate model-only bundles. The unbundled source model files and `src/evren/package_model.py` are retained. `__pycache__` files were omitted as machine-specific bytecode, not source materials.
