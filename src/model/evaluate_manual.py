"""
Evaluator for manually selected Turkish test sentences.
Tests both the Scikit-learn pipeline and PyTorch model on 25 real-world sentences.
"""

import json
import joblib
import numpy as np
import torch
from pipeline import LightweightTurkishClassifierNN, preprocess_turkish_text

def run_manual_evaluation():
    print("=" * 65)
    print("   MANUAL EVALUATION ON 25 REAL-WORLD TURKISH SENTENCES")
    print("=" * 65)
    
    # 1. Load manual test samples
    with open("test_samples_20.json", "r", encoding="utf-8") as f:
        samples = json.load(f)
        
    # 2. Load model & vectorizer
    pipeline = joblib.load("artifacts/model/turkish_text_classifier.joblib")
    classes = list(pipeline.named_steps["clf"].classes_)
    
    # 3. Load PyTorch model
    with open("artifacts/model/vocab.json", "r", encoding="utf-8") as f:
        vocab = json.load(f)
    vectorizer = pipeline.named_steps["tfidf"]
    
    pytorch_model = LightweightTurkishClassifierNN(input_dim=len(vocab), num_classes=len(classes))
    pytorch_model.load_state_dict(torch.load("artifacts/model/turkish_text_classifier.pt"))
    pytorch_model.eval()
    
    results = []
    correct_count = 0
    
    print(f"\nEvaluating {len(samples)} manually curated samples:\n")
    print(f"{'ID':<3} | {'Beklenen':<8} | {'Tahmin':<8} | {'Güven':<7} | {'Metin':<50}")
    print("-" * 85)
    
    for s in samples:
        text = s["text"]
        expected = s["expected_label"]
        
        # Scikit-learn prediction
        prob = pipeline.predict_proba([text])[0]
        pred_idx = np.argmax(prob)
        predicted = classes[pred_idx]
        conf = float(prob[pred_idx])
        
        # PyTorch prediction
        feat = vectorizer.transform([text]).toarray()
        with torch.no_grad():
            torch_prob = pytorch_model.predict_proba(torch.tensor(feat, dtype=torch.float32)).numpy()[0]
        torch_pred = classes[np.argmax(torch_prob)]
        
        # Parity check
        assert predicted == torch_pred, f"Prediction mismatch between sklearn and PyTorch on: '{text}'"
        
        is_correct = (predicted == expected)
        if is_correct:
            correct_count += 1
            status = "✓"
        else:
            status = "✗"
            
        short_text = text if len(text) <= 47 else text[:44] + "..."
        print(f"{s['id']:<3} | {expected:<8} | {predicted:<8} | {conf*100:>5.1f}% | {short_text:<50} {status}")
        
        results.append({
            "id": s["id"],
            "text": text,
            "expected_label": expected,
            "predicted_label": predicted,
            "confidence": conf,
            "probabilities": {cls: round(float(p), 4) for cls, p in zip(classes, prob)},
            "correct": is_correct,
            "category_description": s["category_description"]
        })
        
    accuracy = correct_count / len(samples)
    print("\n" + "=" * 85)
    print(f"Results: {correct_count}/{len(samples)} correct. Manual Test Accuracy: {accuracy*100:.2f}%")
    print("=" * 85)
    
    # Save results
    report = {
        "total_samples": len(samples),
        "correct_predictions": correct_count,
        "accuracy": accuracy,
        "sample_evaluations": results
    }
    with open("artifacts/reports/manual_test_results.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        
    print("\nDetailed manual evaluation report saved to artifacts/reports/manual_test_results.json")

if __name__ == "__main__":
    run_manual_evaluation()
