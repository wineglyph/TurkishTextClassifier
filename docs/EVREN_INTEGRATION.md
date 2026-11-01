# EVREN AI Platform Integration & Ecosystem Report

## 1. Executive Summary
This document outlines the findings of the architectural and API investigation into the **EVREN AI Platform** (`https://evren.ssyz.org.tr`, API `https://api.ssyz.org.tr/api/v1`, LLM Gateway `https://evren-llmapi.ssyz.org.tr/v1`), details the model packaging workflow, documents the live verification results, and provides operational instructions for deploying and running **TurkishTextClassifier**.

---

## 2. Platform Architecture & Publishing Workflow Analysis

### 2.1 Ecosystem Overview
The EVREN AI ecosystem operated by SSB (Savunma Sanayii Başkanlığı) comprises three primary layers:
1. **EVREN Platform Web & API (`api.ssyz.org.tr`):** High-Performance Computing (HPC) orchestration, dataset repository, Slurm-based GPU training cluster, and model registry.
2. **EVREN LLM Gateway (`evren-llmapi.ssyz.org.tr/v1`):** OpenAI-compatible inference gateway serving foundation models (e.g., `deepseek-v4.1-flash`, `qwen3.8-flash-next`, `glm-5.3`, `mimo-v2.6-pro`).
3. **EVREN Universe / Keşif Merkezi:** Public repository of shared models and datasets.

### 2.2 Model Registration & Training Lifecycle
Inspection of EVREN's frontend modules (`UserGuidePage`, `useModels`, `useTraining`, `ModelDetailPage`) revealed the canonical platform workflow:
- **Dataset Creation:** A dataset is created and items/annotations are uploaded.
- **Dataset Freezing:** A version must be created and frozen (`GET /datasets/{id}/versions`).
- **Automated HPC Training Job:** A training job is queued (`POST /training/jobs`) targeting cluster partitions.
- **Automatic Model Registration:** When training completes, EVREN automatically creates the model entry in the registry.
- **Manual Upload Limitation:** The platform documentation explicitly states:
  > *"Eğitim tamamlandığında model otomatik olarak oluşturulur — manuel model oluşturma desteklenmez."*
  *(When training completes, the model is automatically created — manual model creation is not supported).*

### 2.3 Modality Restrictions on EVREN Web Platform
The official EVREN platform user guide explicitly documents the current dataset modality constraints:
> *"İlk adımda veri tipini seçin: Görsel (görüntü/video) veya Medikal (DICOM). Metin, Ses ve Çoklu veri tipleri şu an kullanıma açık değildir."*
*(Select the data type: Vision or Medical. Text, Audio, and Multimodal data types are currently not open for use).*

---

## 3. Live Ecosystem API Verification Probe

A probe script (`src/evren/evren_api_check.py`) was executed to verify live platform endpoints and credentials:

| Endpoint | Method | Result / Status Code | Behavior & Response Summary |
| :--- | :---: | :---: | :--- |
| `/universe/search` | `GET` | **200 OK** | Public universe API accessible unauthenticated. |
| `/models` | `GET` | **401 Unauthorized** | Returns `Token veya API anahtari eksik` when unauthenticated. |
| `/models` | `POST` | **401 Unauthorized** | Manual creation blocked; requires authenticated user session. |
| `/models` (with key) | `GET` | **401 Unauthorized** | Platform API key requires platform scope; LLM Gateway key is dedicated to LLM endpoints. |
| `evren-llmapi/v1/models` | `GET` | **200 OK** | Successfully authenticated with `evren.key`. 16 LLM models accessible. |

### Conclusion on Publication:
In compliance with the project rules (*"Do not claim publication unless it has been verified"* and *"If an EVREN feature is unavailable, document the limitation and complete everything possible locally"*):
- The model is **not** falsely claimed to be published to `api.ssyz.org.tr`'s remote cloud database due to the platform's architectural restriction disallowing manual model uploads outside of its HPC vision training pipeline.
- Instead, the model is fully packaged according to EVREN's official configuration standards and delivered with a local EVREN-compatible microservice and CLI.

---

## 4. Packaging Specification for EVREN AI

The trained model is bundled in `artifacts/dist/turkish_text_classifier_v1.0.0.tar.gz` (and `.zip`) following EVREN specifications:

```
turkish_text_classifier/
├── config.json                        # Model architecture, hyperparams, class definitions
├── metadata.json                      # EVREN ecosystem metadata (modality=NLP, metrics, license)
├── turkish_text_classifier.pt         # PyTorch weights for EVREN PyTorch engine
├── turkish_text_classifier_full.pt    # Self-contained PyTorch Module
├── turkish_text_classifier.joblib     # Scikit-learn CPU inference pipeline
├── vectorizer.joblib                  # TF-IDF sublinear n-gram feature extractor
└── vocab.json                         # Serialized vocabulary index mapping
```

### EVREN Metadata Schema Compliance (`metadata.json`):
```json
{
  "name": "TurkishTextClassifier",
  "slug": "turkish-text-classifier",
  "architecture": "LinearTfidfClassifier",
  "modality": "NLP",
  "visibility": "PUBLIC",
  "stage": "PRODUCTION",
  "framework": "pytorch",
  "tags": ["turkish", "nlp", "text-classification", "intent", "sentiment"],
  "metrics": {
    "accuracy": 0.9974,
    "f1_macro": 0.9971,
    "precision_macro": 0.9974,
    "recall_macro": 0.9969
  },
  "file_size_bytes": 51621,
  "license": "MIT"
}
```

---

## 5. Inference Service & API Verification

An EVREN-compatible inference microservice is implemented in `src/evren/serve.py`.

### 5.1 Starting the Server
```bash
python3 src/evren/serve.py 8080
```

### 5.2 Health Check Endpoint
```bash
curl http://localhost:8080/health
```
**Response:**
```json
{
  "success": true,
  "status": "healthy",
  "model": "TurkishTextClassifier",
  "version": "1.0.0",
  "ecosystem": "EVREN AI"
}
```

### 5.3 Prediction Endpoint (`POST /inference/predict`)
```bash
curl -X POST http://localhost:8080/inference/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Siparişim kargoya verildiğinde SMS ile bilgilendirme yapılacak mı?"}'
```
**Response:**
```json
{
  "success": true,
  "data": {
    "model": "TurkishTextClassifier",
    "version": "1.0.0",
    "predictions": [
      {
        "class_name": "Soru",
        "confidence": 0.8915,
        "probabilities": {
          "Soru": 0.8915,
          "Öneri": 0.0419,
          "Şikâyet": 0.0666
        },
        "text": "Siparişim kargoya verildiğinde SMS ile bilgilendirme yapılacak mı?"
      }
    ],
    "backend": "sklearn",
    "latency_ms": 1.25
  }
}
```


---

## 6. Consolidation Status Note

This document and `artifacts/reports/evren_ecosystem_verification.json` are retained from the supplied project. The API observations are historical records from the earlier probe and were not freshly re-verified during project consolidation. The consolidated project includes local EVREN-compatible inference and packaging scripts, but **no model upload, registration, or public EVREN publication is claimed**.
