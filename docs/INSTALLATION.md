# Installation and Usage

## Requirements

- Python 3.11 or newer is recommended.
- Install the dependencies in `requirements.txt`.
- The bundled scikit-learn estimator was serialized under scikit-learn 1.9.1. Use that version for reproducible `joblib` loading.

## Create an environment

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Windows PowerShell:

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## CLI inference

Run commands from the repository root so the existing relative artifact paths resolve correctly:

```bash
python src/model/predict.py --text "Siparişim ne zaman kargoya verilir acaba?"
python src/model/predict.py --text "Ürünün kutusu hasarlı geldi." --json
```

The prediction service loads the serialized scikit-learn pipeline.

## Python API

The module uses a top-level `pipeline` import. This supported import example adds its directory to `sys.path` without editing project source:

```python
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src" / "model"))

from predict import TurkishTextClassifierService

classifier = TurkishTextClassifierService(
    model_dir=str(PROJECT_ROOT / "artifacts" / "model")
)
result = classifier.predict("Faturam neden beklediğimden yüksek geldi?")
print(result["prediction"], result["confidence"])
```

For a script saved outside this repository, set `PROJECT_ROOT` to the extracted repository directory.

## Local HTTP API

Start the standard-library HTTP server:

```bash
python src/serve.py 8080
```

Health check:

```bash
curl http://127.0.0.1:8080/health
```

Single prediction:

```bash
curl -X POST http://127.0.0.1:8080/inference/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"Kargom üç gündür dağıtıma çıkmadı."}'
```

Batch prediction:

```bash
curl -X POST http://127.0.0.1:8080/inference/predict \
  -H "Content-Type: application/json" \
  -d '{"texts":["Siparişim nerede?","Hizmetten hiç memnun kalmadım."]}'
```

The server binds to `0.0.0.0` and does not implement authentication. Use only in a trusted development environment; do not expose it directly to an untrusted network without adding an appropriate security layer.

## Demo, validation, and smoke checks

```bash
python run_demo.py
python external_eval/validate_dataset.py --project-root .
python scripts/verify_project.py
python -m unittest discover -s tests -v
```

## Training (not required for inference)

The original training entry point is:

```bash
python src/model/train.py
```

It reads `data/train.csv` and `data/test.csv` and writes model/report artifacts. Running it can overwrite model outputs. Do not run it when the intention is to preserve the supplied trained model. No training is needed for inference or for validating the packaged evaluation results.
