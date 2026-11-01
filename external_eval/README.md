# TurkishTextClassifier — Independent Synthetic Evaluation Dataset v1.0.0

## Purpose

This dataset is a standalone synthetic holdout set for a future evaluation of the existing TurkishTextClassifier. It must remain separate from model training, validation, model selection, threshold tuning, vocabulary fitting, and fine-tuning. **All 450 examples were authored synthetically for this evaluation task.** No Hugging Face, Trendyol, Şikayetvar, or other external datasets were downloaded or used. No model inference or evaluation was performed.

## Labels

The label names and spelling match the supplied project:

- **Soru** — the primary intent is to obtain information, an explanation, a status update, or clarification.
- **Şikâyet** — the primary intent is to report an existing failure, negative experience, or dissatisfaction.
- **Öneri** — the primary intent is to propose an improvement, feature, change, or new idea.

These are intent labels, not punctuation or sentiment labels. A question mark alone does not make a message `Soru`; negative vocabulary alone does not make it `Şikâyet`; and a polite request is not automatically `Öneri`. The dominant communicative intent determines the label.

## Composition

Total: **450** examples, with 150 per class. Each of the ten domains contributes 45 examples (15 per class). Each of the five writing styles contributes 90 examples.

### Class distribution

| Class | Examples |
|---|---:|
| Soru | 150 |
| Şikâyet | 150 |
| Öneri | 150 |

### Domain distribution

| Domain | Examples |
|---|---:|
| E-ticaret | 45 |
| Bankacılık ve finans | 45 |
| Telekomünikasyon | 45 |
| Yazılım ve mobil uygulamalar | 45 |
| Ulaşım | 45 |
| Sağlık hizmetleri | 45 |
| Belediye hizmetleri | 45 |
| Eğitim | 45 |
| Kargo ve lojistik | 45 |
| Restoran ve konaklama | 45 |

### Writing-style distribution

| Writing style | Examples |
|---|---:|
| Resmî / kurumsal | 90 |
| Ayrıntılı anlatım | 90 |
| Günlük konuşma | 90 |
| Yazım varyasyonlu | 90 |
| Kısa ve doğrudan | 90 |


Writing styles cover formal/organizational wording, everyday conversation, short direct messages, detailed contextual narration, and realistic spelling/diacritic variation. The last group includes missing Turkish characters such as `ş`, `ğ`, `ı`, `ç`, `ö`, and `ü`, along with minor typing errors. Strong emotions and emphatic expressions also appear naturally, especially in complaints. Style is an editorial descriptor, not a linguistic diagnosis.

## Generation methodology

Examples were authored specifically for this dataset with a balanced 10-domain × 3-class design (15 sentences per domain/class cell). Sentences vary in length, register, syntax, vocabulary, punctuation, and the way intent is expressed. Examples include both explicit and indirect informational requests, concrete reports of service failures, and clearly framed improvement proposals. A deterministic interleaving step prevents the CSV from being grouped by class or domain.

The five writing-style groups are balanced within every domain/class cell (three examples per style).

## Leakage and similarity checks

The original complete corpus, its JSONL mirror, train/test CSVs, manual sample JSON, stored manual-evaluation report, and the generator's curated examples were checked as references. Supplemental quoted example strings in project documentation and code were also included in the extended similarity inventory. Normalization follows the project's Turkish-aware lowercasing (`I` → `ı`, `İ` → `i`), Unicode NFKC, punctuation cleanup, and whitespace collapse. Exact and punctuation-insensitive overlaps were checked. Near-duplicate screening used character 3–5-gram TF-IDF cosine similarity and `difflib.SequenceMatcher` on the five nearest character-similarity neighbors for each record. Thresholds and measured maxima are documented in `QUALITY_REPORT.md`. These lexical methods cannot prove semantic independence.

## Intended later evaluation use

Use `synthetic_test.csv` as a fixed external evaluation set. Keep it separate from training, vocabulary fitting, tuning, prompt/rule development, and model selection. Expose only `text` to the prediction process; retain `gold_label` for scoring after predictions are produced. Record the model version and evaluation code version used in that later evaluation.

## Known limitations

- Synthetic sentences cannot fully represent naturally sampled customer messages, production slang, rare intents, or the true frequency of each class/domain.
- The set is deliberately balanced; its class distribution is not a deployment-prevalence estimate.
- Lexical similarity screening cannot guarantee semantic independence and may miss paraphrases or flag common domain vocabulary. No embedding model or external semantic service was used.
- The second label review was an internal, text-only editorial review, not independent human annotation; no inter-annotator agreement is claimed.
- Checks could cover only files present in the supplied archive. No separate validation split file or raw data files were present; `data/raw/` was empty.

## Files

- `synthetic_test.csv` — 450 labeled synthetic examples.
- `QUALITY_REPORT.md` — inspection, measured duplicate/similarity results, audit results, validation, and limitations.
- `dataset_metadata.json` — machine-readable metadata and validation summary.
- `validate_dataset.py` — reusable, non-destructive validation script.
- `GENERATION_NOTES.md` — concise description of dataset construction and checks.


## Label-review evidence limitation

An earlier aggregate note reports 450/450 agreement in a text-only second pass, but the per-example review labels were not preserved in the project workspace. The temporary builder's adjudication step copies the original labels, so that code does not substantiate independent agreement. See the corrected evidence assessment in `QUALITY_REPORT.md`; do not treat the 450/450 figure as a reproducibly verified audit result.
