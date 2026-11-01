# Generation Notes

- All 450 examples were authored synthetically for this independent evaluation set. No external datasets, paid APIs, or model-generated predictions were used.
- Construction grid: 10 domains × 3 intent classes × 15 sentences = 450 records.
- Every domain/class cell contains three examples from each of five writing-style groups, yielding 90 examples per style.
- The sentences cover information-seeking questions, existing service failures/dissatisfaction, and improvement proposals. Formal, conversational, concise, detailed, emphatic, and intentionally imperfect Turkish appear across the set; the style labels track the five balanced editorial groups.
- Records are deterministically interleaved in the CSV rather than grouped by class or domain.
- Project-consistent Turkish normalization was used for exact overlap detection. Punctuation-insensitive matching, character 3–5-gram TF-IDF cosine similarity, and edit similarity on nearest lexical neighbors were also used. These are lexical screens, not proof of semantic independence.
- A separate internal review read the final shuffled text-only records without seeing their labels, assigned the dominant intent, and then compared those decisions with the restored gold labels. This was an internal editorial pass, not independent human annotation.
- No model weights, vectorizer, prediction API, training script, or model inference path was used to generate, label, or score examples.


## Label-review evidence note (consolidation)

An earlier working summary reported a 450-item text-only second pass with 450/450 agreement. The project workspace did not retain per-example review labels or a decision log. The temporary builder script's final adjudication map copies the existing gold labels and therefore cannot independently prove that agreement. For this reason, `QUALITY_REPORT.md` now marks the aggregate audit claim as **not independently verifiable** rather than presenting it as a validated result. This correction does not change the dataset labels or the already-recorded model evaluation outputs.
