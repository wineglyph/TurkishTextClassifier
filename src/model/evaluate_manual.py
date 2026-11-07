"""
Evaluator for manually selected Turkish test sentences.
Tests the Scikit-learn pipeline on real-world sentences.
"""

import json
import os
from pathlib import Path
import joblib
import numpy as np

def run_manual_evaluation():
    print("=" * 65)
    print("   MANUAL EVALUATION ON REAL-WORLD TURKISH SENTENCES")
    print("=" * 65)
    
    # 1. Load manual test samples
    samples_path = Path("data/manual_samples.json")
    with samples_path.open("r", encoding="utf-8") as f:
        samples = json.load(f)
        
    # 2. Load model & vectorizer
    pipeline = joblib.load("artifacts/model/turkish_text_classifier.joblib")
    classes = list(pipeline.named_steps["clf"].classes_)
    
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
