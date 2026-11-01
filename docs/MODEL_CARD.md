# Model Card: TurkishTextClassifier (v1.0.0)

## 1. Model Details
- **Model Name:** TurkishTextClassifier
- **Version:** 1.0.0
- **Model Type:** Lightweight Turkish Text Intent Classifier
- **Architecture:** Sublinear TF-IDF (1-2 n-grams, 5000 max features) + Balanced Linear/Logistic Classifier (with PyTorch `.pt` neural projection)
- **Frameworks:** The original card records PyTorch 2.15.0 and scikit-learn 1.9.1. The consolidation smoke-tested the PyTorch backend runtime with PyTorch 2.10.0+cpu; the sklearn artifact emitted a version warning under scikit-learn 1.8.0 (see Section 8).
- **Target Ecosystem:** EVREN AI (`ssyz.org.tr`)
- **Modality:** NLP (Text)
- **License metadata:** `MIT` is recorded in `artifacts/model/metadata.json`; however, no repository `LICENSE` file or independent rights-holder authorization was supplied. Treat redistribution rights as unverified until confirmed.
- **Author/Maintainer metadata:** EVREN AI NLP Project (as recorded in the original model card; ownership was not independently verified).

---

## 2. Intended Use
- **Primary Use Case:** Real-time customer service request routing, feedback triage, and automated inbox classification for Turkish text inputs.
- **Target Categories (3-Class):**
  1. **Soru (Question):** Inquiries, informational questions, procedural lookups, and account status requests.
  2. **Şikâyet (Complaint):** Negative experiences, defective items, delays, unresolved issues, and service dissatisfaction.
  3. **Öneri (Suggestion):** Constructive feedback, new feature requests, UX enhancements, and procedural improvement proposals.
- **Out-of-Scope Uses:** Long document summarization, sentiment polarity quantification beyond the three designated intent categories, multilingual classification without Turkish preprocessing.

---

## 3. Dataset Information
- **Total Dataset Size:** 1,922 unique, deduplicated Turkish sentences.
- **Label Distribution:**
  - **Soru:** 756 samples (39.3%)
  - **Şikâyet:** 632 samples (32.9%)
  - **Öneri:** 534 samples (27.8%)
- **Domain Coverage (10 Representative Sectors):**
  - E-ticaret / Alışveriş (order status, returns, packaging, product inquiries)
  - Bankacılık & Finans (credit card, EFT, interest, ATM issues, limits)
  - Telekomünikasyon / İnternet (bills, speed, fiber, connectivity, roaming)
  - Yazılım, Mobil Uygulama & Web (bugs, dark mode, syncing, crashes)
  - Ulaşım & Seyahat (flights, delays, baggage, bus routes, seat selection)
  - Sağlık & Randevu (hospital appointments, blood tests, prescriptions)
  - Belediye & Kamu Hizmetleri (road repairs, waste, street lights, bus schedules)
  - Kargo & Lojistik (live tracking, damaged packages, delayed courier)
  - Eğitim & Üniversite (course registrations, transcripts, exams, library)
  - Restoran & Yeme-İçme (delivery temperature, allergen notes, portion size)
- **Train / Test Split:**
  - **Training Set:** 1,537 samples (80.0%, stratified)
  - **Test Set:** 385 samples (20.0%, stratified)
  - **Data Leakage:** Verified 0 overlapping instances between train and test splits.

---

## 4. Training Methodology
- **Preprocessing Pipeline:**
  - Proper Turkish character lowercasing (preserving dotted `İ` -> `i` and dotless `I` -> `ı`).
  - Unicode NFKC normalization.
  - Punctuation condensation and clean whitespace normalization.
- **Feature Engineering:**
  - Sublinear term frequency scaling (`sublinear_tf=True`).
  - Word and sub-phrase n-grams: range `(1, 2)`.
  - Token pattern: `(?u)\b\w+\b|[!?]` to retain question and exclamation cues.
  - Vocabulary dimension: 5,000 features.
- **Candidate Benchmark (5-Fold Stratified Cross-Validation on Train Set):**
  - Logistic Regression (C=2.0, balanced): **F1-Macro = 0.9958 (+/- 0.0050)**
  - LinearSVC (C=1.0, balanced): **F1-Macro = 0.9958 (+/- 0.0050)**
  - ComplementNB: **F1-Macro = 0.9958 (+/- 0.0050)**
- **PyTorch Parity Transfer:**
  - Linear layer weights and biases transferred directly to PyTorch `LightweightTurkishClassifierNN`.
  - Maximum numerical probability divergence between Scikit-learn and PyTorch: **0.00000002** (exact parity).

---

## 5. Evaluation Metrics
Evaluated on the held-out test set (385 samples):

| Metric | Score |
| :--- | :--- |
| **Accuracy** | **99.74%** (384 / 385 correct) |
| **Macro Precision** | **99.74%** |
| **Macro Recall** | **99.69%** |
| **Macro F1-Score** | **99.71%** |
| **Weighted F1-Score** | **99.74%** |
| **Single-Sample Inference Latency** | **~1.16 ms** |

### Per-Class Detailed Performance:
| Category | Precision | Recall | F1-Score | Support |
| :--- | :---: | :---: | :---: | :---: |
| **Soru (Question)** | 1.0000 | 1.0000 | **1.0000** | 151 |
| **Şikâyet (Complaint)** | 0.9922 | 1.0000 | **0.9961** | 127 |
| **Öneri (Suggestion)** | 1.0000 | 0.9907 | **0.9953** | 107 |

### Confusion Matrix (Test Set):
```
            Pred: Soru   Pred: Şikâyet   Pred: Öneri
True: Soru       151           0              0
True: Şikâyet      0         127              0
True: Öneri        0           1            106
```

### Manual Validation (25 Real-World Unseen Sentences):
- **Accuracy:** **96.00%** (24 / 25 correct)
- Tested across colloquial phrasing, typo variations, and formal customer complaints.

---

## 6. Limitations
1. **Short Ambiguous Inputs:** Very short sentences consisting of 1-2 words without punctuation or context (e.g., *"Yardım"* or *"Destek"*) may exhibit lower prediction certainty.
2. **Compound Sarcasm & Dual Intents:** Sentences containing both a complaint and a question (e.g., *"İki haftadır kargom gelmedi, bu nasıl rezillik?"*) will predominantly classify into the dominant lexical feature (Complaint in this instance).
3. **EVREN Platform Modality Constraints:** EVREN AI's online portal (`https://evren.ssyz.org.tr`) currently supports dataset management and automated HPC training exclusively for VISION and MEDICAL modalities. Self-service text model training is not yet exposed via the public web UI. The model is packaged for PyTorch `.pt` local/microservice inference.

---

## 7. Example Inputs and Outputs

| Girdi Cümlesi (Input) | Tahmin (Prediction) | Güven (Confidence) | Baskın Kategori Gerekçesi |
| :--- | :---: | :---: | :--- |
| *"Siparişim kargoya verildiğinde SMS ile bilgilendirme yapılacak mı?"* | **Soru** | %98.4 | Soru eki `mı`, sorgulama yüklemi |
| *"Ürünün kutusu paramparça geldi ve içindeki cam parça kırılmış, rezillik resmen!"* | **Şikâyet** | %84.7 | Olumsuz deneyim, hasar ifadesi (`rezillik`, `kırılmış`) |
| *"Mobil uygulamaya gece modu seçeneği eklenirse karanlıkta gözü yormaz, çok iyi olur."* | **Öneri** | %93.6 | Şart kipi (`eklenirse`) ve tavsiye (`çok iyi olur`) |
| *"Hesabımdan haberim olmadan iki defa para çekilmiş, acilen iadesini talep ediyorum."* | **Şikâyet** | %80.4 | Mağduriyet ve yetkisiz işlem bildirimi |
| *"Otobüs duraklarına akıllı dijital ekranlar konulmasını tavsiye ederim."* | **Öneri** | %81.6 | Doğrudan tavsiye fiili (`tavsiye ederim`) |
| *"Yurtdışı kullanımında roaming ücreti günlük mü yoksa aylık mı yansıtılıyor?"* | **Soru** | %94.8 | Karşılaştırmalı soru yapısı (`günlük mü yoksa aylık mı`) |


## 8. Packaging and Evaluation Caveats

- The production inference service defaults to the serialized scikit-learn pipeline (`artifacts/model/turkish_text_classifier.joblib`). It also initializes the optional PyTorch state-dictionary backend.
- The independent synthetic evaluation used the default scikit-learn backend for 450 examples and measured 81.56% accuracy (367/450) and 81.07% macro F1. See `external_eval/results/EVALUATION_REPORT.md`. This synthetic benchmark is not a real-world production accuracy estimate.
- During the recorded evaluation, the persisted scikit-learn estimators reported version 1.9.1, while the runtime was 1.8.0; an `InconsistentVersionWarning` was emitted. The pipeline loaded and predicted, but strict reproducibility should use the artifact-matching version.
- The supplied repository contains no `LICENSE` file. The MIT value in model metadata does not independently establish redistribution rights for all bundled source, weights, and data.
