"""
CLI and Python programmatic prediction module for TurkishTextClassifier.
Supports single sentences, batch inference, and JSON output.
"""

import argparse
import json
import sys
import time
import joblib
import numpy as np

class TurkishTextClassifierService:
    def __init__(self, model_dir: str = "artifacts/model"):
        self.model_dir = model_dir
        
        # Load config
        with open(f"{model_dir}/config.json", "r", encoding="utf-8") as f:
            self.config = json.load(f)
            
        # Load scikit-learn pipeline
        self.pipeline = joblib.load(f"{model_dir}/turkish_text_classifier.joblib")
        self.classes = list(self.pipeline.named_steps["clf"].classes_)
        self.vectorizer = self.pipeline.named_steps["tfidf"]

    def predict(self, text: str) -> dict:
        t0 = time.time()
        probs = self.pipeline.predict_proba([text])[0]
        pred_idx = int(np.argmax(probs))
        pred_class = self.classes[pred_idx]
        confidence = float(probs[pred_idx])
        latency_ms = (time.time() - t0) * 1000
        
        prob_dict = {cls: round(float(p), 4) for cls, p in zip(self.classes, probs)}
        
        return {
            "text": text,
            "prediction": pred_class,
            "confidence": round(confidence, 4),
            "probabilities": prob_dict,
            "latency_ms": round(latency_ms, 3)
        }

    def predict_batch(self, texts: list) -> list:
        return [self.predict(t) for t in texts]

def main():
    parser = argparse.ArgumentParser(description="TurkishTextClassifier CLI Inference Tool")
    parser.add_argument("--text", "-t", type=str, help="Turkish text to classify")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    
    args = parser.parse_args()
    
    service = TurkishTextClassifierService()
    
    if args.text:
        res = service.predict(args.text)
        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            print("\n--- TAHMİN SONUCU ---")
            print(f"Girdi Metin  : {res['text']}")
            print(f"Sınıf        : {res['prediction']} (Güven: %{res['confidence']*100:.1f})")
            print(f"Olasılıklar  : {res['probabilities']}")
            print(f"Gecikme      : {res['latency_ms']} ms")
    else:
        # Interactive mode
        print("TurkishTextClassifier Interactive Mode (Çıkmak için 'q' yazın):")
        while True:
            try:
                line = input("\nMetin girin > ").strip()
                if not line or line.lower() == 'q':
                    break
                res = service.predict(line)
                print(f"-> Sınıf: {res['prediction']} (%{res['confidence']*100:.1f}) | {res['probabilities']} [{res['latency_ms']} ms]")
            except (KeyboardInterrupt, EOFError):
                break

if __name__ == "__main__":
    main()
