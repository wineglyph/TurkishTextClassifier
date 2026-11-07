# Dataset Card — TurkishTextClassifier

## Summary

The repository contains the original project corpus and a separate synthetic evaluation set. They have different roles and must not be conflated.

## Original corpus

| File | Rows | Role |
|---|---:|---|
| `data/turkish_text_dataset.csv` | 1,922 | Complete project corpus |
| `data/turkish_text_dataset.jsonl` | 1,922 | JSON Lines representation of the corpus |
| `data/train.csv` | 1,537 | Training split |
| `data/test.csv` | 385 | Held-out internal test split |
| `data/manual_samples.json` | 25 | Manually prepared examples |
| `artifacts/reports/manual_test_results.json` | 25 results | Previously recorded manual evaluation output |

The corpus schema is `text`, `label`, and `domain`. Its labels are `Soru`, `Şikâyet`, and `Öneri`. The full corpus label distribution is 756 / 632 / 534 respectively. The train/test split is stratified according to the original model card.

The bundled `src/dataset/generate_dataset.py` describes a locally generated, template/vocabulary-based corpus covering ten service domains. The repository does not include a formal data-provenance ledger, a third-party dataset attribution list, or rights-holder authorization. Therefore, this packaging makes no independent legal determination about redistribution rights. Review the original creator's rights and any applicable terms before public release.

## Independent synthetic evaluation set

`external_eval/synthetic_test.csv` is a separate, fully synthetic test candidate created for independent evaluation. It contains 450 unique examples, balanced at 150 per label, across ten domains (45 each) and five writing styles (90 each). All examples are marked synthetic in the `synthetic` column. The set is not training data and must not be added to training or tuning without changing the evaluation design.

Its accompanying `README.md`, `QUALITY_REPORT.md`, `GENERATION_NOTES.md`, and `dataset_metadata.json` describe generation, distributions, duplicate/similarity checks, and an internal second-pass label audit. The `results/` directory contains predictions and evaluation outputs from the separate evaluation task.

## Intended use

- The original train split is used by the existing training script.
- The original test split records the project's internal hold-out benchmark.
- The manual sample file records a small manually prepared check.
- The synthetic set is intended for a separate, independent generalization check and error analysis.

## Labels

- **Soru:** primary intent is to obtain information, explanation, or clarification.
- **Şikâyet:** primary intent is dissatisfaction about an existing problem or failed experience.
- **Öneri:** primary intent is to propose an improvement, feature, change, or new idea.

## Known limitations

- The synthetic set cannot represent the full distribution of real user/customer traffic.
- Synthetic fluency, label decisions, and domain balance may differ from naturally collected messages.
- A separate internal editorial label review is not independent human annotation.
- Similarity checks do not prove semantic independence.
## Licensing and attribution

The codebase is released under the **MIT License** (Copyright (c) 2026 wineglyph). The dataset provenance is locally generated based on domain templates and vocabulary, as described in `src/dataset/generate_dataset.py`.
