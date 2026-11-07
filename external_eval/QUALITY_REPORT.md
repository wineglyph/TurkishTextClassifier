# Quality Report — TurkishTextClassifier Independent Synthetic Evaluation Dataset v1.0.0

## 1. Scope and project inspection

The supplied project archive was extracted into a separate inspection directory. The project files were inspected before data generation. The relevant inspected assets were:

| Project area | Files inspected | Findings |
|---|---|---|
| Complete data | `data/turkish_text_dataset.csv`, `data/turkish_text_dataset.jsonl` | 1,922 examples; columns are `text`, `label`, `domain` |
| Training / test | `data/train.csv`, `data/test.csv` | 1,537 training rows; 385 test rows |
| Manual tests | `test_samples_20.json`, `artifacts/reports/manual_test_results.json` | 25 manual examples in each representation; report mirrors the manual test texts |
| Dataset generation / validation | `src/dataset/generate_dataset.py`, `src/dataset/validate_dataset.py` | Domain vocabulary, templates, 45 curated edge cases, and original QA logic inspected |
| Preprocessing / model | `src/model/pipeline.py`, `src/model/predict.py`, `src/model/train.py`, `src/model/evaluate_manual.py` | Turkish normalizer, TF-IDF feature pipeline, Logistic Regression classifier, and prediction paths inspected |
| Documentation | `README.md`, `docs/MODEL_CARD.md` | Intended use, categories, original data description, training/evaluation notes inspected |
| Existing artifacts | `artifacts/model/config.json`, `metadata.json`, `vocab.json`, weights, and `artifacts/reports/*` | Class names and model configuration inspected; no weights or model objects were loaded for prediction |
| Release archives | `artifacts/dist/turkish_text_classifier_v1.0.0.tar.gz`, `.zip` | Contain model/package artifacts; no additional evaluation data corpus |

### Actual label definitions and pipeline behavior

The expected labels are exactly `Soru`, `Şikâyet`, and `Öneri`.

- **Soru:** information-seeking, clarification, procedure, status, or eligibility inquiry.
- **Şikâyet:** dissatisfaction about an existing problem, failure, negative experience, or unresolved service issue.
- **Öneri:** a proposed improvement, feature, change, or new idea.

The project normalizer applies Turkish-aware lowercase mapping (`I` → `ı`, `İ` → `i`), Unicode NFKC normalization, repeated punctuation condensation, filtering of non-word/noise characters while preserving basic punctuation cues, and whitespace collapse. The documented feature pipeline uses word unigrams/bigrams with sublinear TF-IDF and a balanced Logistic Regression classifier; the prediction service can use the scikit-learn pipeline or the exported PyTorch linear layer.

This task did **not** load the model, call its prediction functions or API, run model evaluation, train, fine-tune, or change any model artifacts.

### Original source inventory used for contamination checks

| Source | Text entries |
|---|---:|
| `data/turkish_text_dataset.csv` | 1,922 |
| `data/train.csv` | 1,537 |
| `data/test.csv` | 385 |
| `data/turkish_text_dataset.jsonl` | 1,922 |
| `test_samples_20.json` | 25 |
| `artifacts/reports/manual_test_results.json` | 25 |
| `src/dataset/generate_dataset.py` — `CURATED_EXAMPLES` | 45 |
| `README.md` — extractable quoted text | 5 |
| `docs/MODEL_CARD.md` — extractable quoted text | 7 |
| `src/model/train.py` — extractable quoted text | 41 |
| `src/model/predict.py` — extractable quoted text | 15 |
| `artifacts/model/metadata.json` — extractable quoted text | 4 |
| **Total reference entries (representations overlap)** | **5,933** |

The full CSV, split files, and JSONL mirror contain overlapping representations, so the entry counts above are not additive counts of independent original samples. The extended reference inventory contained **2,003 unique texts after project-style normalization**.

## 2. Final dataset composition

- Total records: **450**
- Total class count: **150 per class**
- Domains: **10**, each with 45 records (15 per class)
- Writing-style groups: **5**, each with 90 records (3 per class/domain cell)

### Class distribution

| Class | Count |
|---|---:|
| Soru | 150 |
| Şikâyet | 150 |
| Öneri | 150 |
| **Total** | **450** |

### Domain distribution

| Domain | Soru | Şikâyet | Öneri | Total |
|---|---:|---:|---:|---:|
| E-ticaret | 15 | 15 | 15 | 45 |
| Bankacılık ve finans | 15 | 15 | 15 | 45 |
| Telekomünikasyon | 15 | 15 | 15 | 45 |
| Yazılım ve mobil uygulamalar | 15 | 15 | 15 | 45 |
| Ulaşım | 15 | 15 | 15 | 45 |
| Sağlık hizmetleri | 15 | 15 | 15 | 45 |
| Belediye hizmetleri | 15 | 15 | 15 | 45 |
| Eğitim | 15 | 15 | 15 | 45 |
| Kargo ve lojistik | 15 | 15 | 15 | 45 |
| Restoran ve konaklama | 15 | 15 | 15 | 45 |
| **Total** | **150** | **150** | **150** | **450** |

### Writing-style distribution

| Writing style | Count |
|---|---:|
| Resmî / kurumsal | 90 |
| Günlük konuşma | 90 |
| Kısa ve doğrudan | 90 |
| Ayrıntılı anlatım | 90 |
| Yazım varyasyonlu | 90 |
| **Total** | **450** |

## 3. Exact duplicate checks

Project-style normalized matching used Turkish-aware lowercase conversion, NFKC, punctuation cleanup, and whitespace collapse. A second key removed basic punctuation and collapsed whitespace, so punctuation-only or spacing-only variants would still match.

| Check | Result |
|---|---:|
| Duplicate records within the new CSV after project-style normalization | **0** |
| Duplicate records within the new CSV after punctuation/whitespace normalization | **0** |
| New-to-original exact normalized overlaps | **0** |
| New-to-original punctuation-insensitive overlaps | **0** |

The checks covered the full corpus and its JSONL mirror, train/test split files, the manual test JSON and stored manual-results report, curated generator examples, and supplemental quoted examples extracted from documentation and source files.

## 4. Near-duplicate analysis

### Methods and thresholds

1. **Character n-gram similarity:** TF-IDF with character 3–5-grams and sublinear term frequency. Cosine similarity was computed for every new-to-original pair and for every within-new-set pair.
2. **Edit-style similarity:** `difflib.SequenceMatcher` ratio on the five nearest character-similarity neighbors for each new example. This limits expensive edit comparisons to the most plausible lexical neighbors.
3. **Review thresholds:** cross-corpus pairs would be flagged at character cosine ≥ **0.67** or edit ratio ≥ **0.78**; within-dataset pairs would be flagged at cosine ≥ **0.70** or edit ratio ≥ **0.82**.

### Measured results on the final CSV

| Metric | Highest measured value | Flag threshold | Flagged pairs |
|---|---:|---:|---:|
| Cross-corpus character cosine | **0.3746** | 0.67 | 0 |
| Cross-corpus edit ratio among top-five character neighbors | **0.6279** | 0.78 | 0 |
| Within-dataset character cosine | **0.3134** | 0.70 | 0 |
| Within-dataset edit ratio among top-five character neighbors | **0.6531** | 0.82 | 0 |

No pair met the near-duplicate thresholds. The strongest cross-corpus lexical neighbor was a short inquiry about how long an additional internet package remains valid compared with an original inquiry about when that package becomes active. Their subject vocabulary overlaps, but the information requested is different; the pair was reviewed. The strongest within-dataset edit neighbor was between two short suggestions about adding amenities in different service contexts; it is not a paraphrase.

During preliminary review of the nearest pairs, two sentences that were too close in wording/intent to existing examples were rewritten (banking password recovery; cargo branch-pickup identity verification). A further banking question was reworded to widen its distance from nearby source language. Five complaint statements were also strengthened because the initial phrasing described a state too neutrally. These nine targeted rewrites were completed before the final text-only label audit and all checks were rerun afterward.

**Limitations:** Character n-grams and edit ratios are lexical methods. They cannot establish semantic independence and can miss paraphrases that use different words or overstate similarity for common domain terms. No local embedding model was available for this task, and none was downloaded. No classifier or model inference was used as a substitute for similarity review.

## 5. Original dataset contamination analysis

- All accessible complete, split, JSONL, and manually curated dataset references were included.
- The original train and test CSVs are subsets of the complete dataset; the JSONL file is a second representation of that corpus.
- The manual JSON and persisted evaluation report both contain 25 examples and were both checked.
- The generator's hand-curated examples were parsed from source as data; the source file was not executed.
- Additional extractable quoted examples from README/model docs/training/prediction source/model metadata were added to the extended near-similarity inventory.
- Final exact and punctuation-insensitive new-to-original overlap counts are both **0**.

### Missing or unavailable source files

- No separate validation CSV/split was found in the supplied project.
- `data/raw/` exists but is empty; no raw source corpus files were available there.
- No separate manually authored test file beyond `test_samples_20.json` and its persisted evaluation report was found.
- No external dataset was retrieved or used, and no check against unprovided source files can be claimed.

## 6. Second-pass label audit — evidence limitation

The earlier working notes and an aggregate scratch summary report that 450 examples were reviewed in a text-only pass and that the reported agreement was 450/450. However, the workspace does **not** preserve the 450 per-example review decisions or a reviewer decision log. Inspection of the temporary dataset-builder script also shows that its final `adjudicated` mapping assigns each example its existing `gold_label`; that code therefore cannot independently substantiate a 450/450 second-pass agreement result.

| Audit evidence | Status |
|---|---|
| Aggregate summary reports 450 reviewed / 450 agreement | Reported in a temporary workspace summary; not retained as a project audit artifact |
| Per-example blind review category assignments | Not available |
| Reproducible independent agreement calculation | **Not verifiable from retained files** |
| Unresolved cases | The aggregate summary reports 0, but there is no per-example record to verify this |

Accordingly, this package does **not** claim a verified 450/450 independent label-audit result. The gold labels remain the authored dataset labels and have not been changed in this consolidation. A future human or independently logged label review should preserve one reviewed label per ID before an agreement rate is stated as verified. This is an internal documentation correction; it does not change any dataset row or model evaluation prediction.

## 7. Final data-quality and safety checks

| Check | Result |
|---|---|
| CSV data rows excluding header | **450 — PASS** |
| Required columns and order | **PASS** (`id`, `text`, `gold_label`, `domain`, `writing_style`, `synthetic`) |
| Exact class balance | **PASS** — 150 each |
| Domain coverage / balance | **PASS** — all ten domains, 45 each, all classes represented |
| Writing-style coverage / balance | **PASS** — all five styles, 90 each |
| Empty text fields | **0 — PASS** |
| Empty IDs / duplicate IDs | **0 — PASS** |
| Unexpected label values | **0 — PASS** |
| Exact duplicates within dataset | **0 — PASS** |
| Exact source overlaps | **0 — PASS** |
| Punctuation-insensitive source overlaps | **0 — PASS** |
| UTF-8 decoding and CSV parsing | **PASS** |
| Email pattern matches | **0** |
| Turkish phone-number pattern matches | **0** |
| Long numeric identifier pattern matches | **0** |
| IBAN pattern matches | **0** |
| Synthetic marker | **450 / 450 marked `true`** |

The personal-data scan is pattern-based and is not a universal privacy guarantee. No personal phone numbers, financial identifiers, or real street addresses were intentionally authored; examples refer to generic service contexts and non-identifying locations such as a neighborhood or branch.

The reusable `validate_dataset.py` script was run against the final CSV with the extracted project root. It completed successfully and independently rechecked row count, labels, domains, writing styles, empty fields, duplicates, UTF-8/CSV parsing, pattern-based personal-data indicators, and exact overlap with accessible source datasets/manual files.

## 8. Project integrity and prohibited actions

- All newly created deliverables are confined to `external_eval/` inside the extracted project directory.
- Original project files, datasets, preprocessing code, training scripts, model weights, and prediction pipeline were not edited.
- No model inference, model evaluation, training, fine-tuning, or retraining was performed.
- No unnecessary dependency was installed; existing local Python/scikit-learn tooling was used for tabular parsing and lexical similarity analysis.
- No project files were uploaded to an external service.

## 9. Risks and limitations

1. Synthetic text is not a substitute for a naturally sampled, independently annotated user-message corpus.
2. Class and domain balance are intentionally artificial and do not represent real incoming-message prevalence.
3. Lexical similarity checks cannot prove semantic independence; paraphrase-level contamination from unavailable sources remains possible.
4. The earlier label-audit result is only an aggregate claim; per-example review decisions were not preserved, so independent agreement is not reproducible from this package.
5. The missing validation split and empty raw-data directory prevent inspection of those unavailable sources.
6. Some examples are intentionally short or informal; a later evaluator should report per-class and per-domain metrics rather than relying on aggregate accuracy alone.
