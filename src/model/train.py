"""
Training and Evaluation Script for TurkishTextClassifier:
1. Cross-validates baseline lightweight models
2. Trains the chosen architecture
3. Exports Scikit-Learn pipeline artifacts
4. Evaluates on test set and generates detailed metrics
"""

import json
import os
import time
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score
)
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.naive_bayes import ComplementNB
from sklearn.svm import LinearSVC

from pipeline import (
    build_sklearn_pipeline,
    preprocess_turkish_text
)

CLASSES = ["Soru", "Şikâyet", "Öneri"]
CLASS_TO_IDX = {c: i for i, c in enumerate(CLASSES)}
IDX_TO_CLASS = {i: c for i, c in enumerate(CLASSES)}

def run_training():
    print("=" * 60)
    print("   TURKISH TEXT CLASSIFIER - TRAINING & EVALUATION")
    print("=" * 60)
    
    # 1. Load data
    train_df = pd.read_csv("data/train.csv")
    test_df = pd.read_csv("data/test.csv")
    
    X_train = train_df["text"]
    y_train = train_df["label"]
    X_test = test_df["text"]
    y_test = test_df["label"]
    
    print(f"\nLoaded {len(train_df)} training samples and {len(test_df)} test samples.")
    
    # 2. Benchmark candidate lightweight architectures (5-fold CV)
    print("\n--- 1. Evaluating Lightweight Model Candidates (5-Fold CV) ---")
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    candidates = {
        "LogisticRegression (C=2.0)": build_sklearn_pipeline(c_param=2.0),
        "LinearSVC (C=1.0)": Pipeline([
            ("tfidf", build_sklearn_pipeline().named_steps["tfidf"]),
            ("clf", LinearSVC(C=1.0, random_state=42, class_weight="balanced"))
        ]),
        "ComplementNB": Pipeline([
            ("tfidf", build_sklearn_pipeline().named_steps["tfidf"]),
            ("clf", ComplementNB())
        ])
    }
    
    cv_results = {}
    for name, pipe in candidates.items():
        scores = cross_val_score(pipe, X_train, y_train, cv=skf, scoring="f1_macro")
        cv_results[name] = {"mean": float(scores.mean()), "std": float(scores.std())}
        print(f"  {name:<28}: Mean F1-Macro = {scores.mean():.4f} (+/- {scores.std():.4f})")
        
    # Choose LogisticRegression for well-calibrated probabilities and smooth PyTorch weight transfer
    chosen_pipeline = build_sklearn_pipeline(c_param=2.0, max_features=5000)
    
    # 3. Fit pipeline on full train set
    print("\n--- 2. Training Chosen Architecture on Full Training Set ---")
    t0 = time.time()
    chosen_pipeline.fit(X_train, y_train)
    train_duration = time.time() - t0
    print(f"Training completed in {train_duration:.3f} seconds.")
    
    # 4. Measure inference latency
    warmup_text = ["Kargo ne zaman teslim edilecek?"] * 50
    _ = chosen_pipeline.predict(warmup_text)
    
    t0 = time.time()
    n_runs = 500
    for _ in range(n_runs):
        _ = chosen_pipeline.predict(["Siparişim ne zaman kargoya verilir acaba?"])
    latency_ms = ((time.time() - t0) / n_runs) * 1000
    print(f"Single-sentence inference latency: {latency_ms:.3f} ms")
    
    # 5. Evaluate on held-out test set
    print("\n--- 3. Held-out Test Set Evaluation ---")
    y_pred = chosen_pipeline.predict(X_test)
    y_prob = chosen_pipeline.predict_proba(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    p_macro = precision_score(y_test, y_pred, average="macro", zero_division=0)
    r_macro = recall_score(y_test, y_pred, average="macro", zero_division=0)
    f1_macro = f1_score(y_test, y_pred, average="macro", zero_division=0)
    
    p_weighted = precision_score(y_test, y_pred, average="weighted", zero_division=0)
    r_weighted = recall_score(y_test, y_pred, average="weighted", zero_division=0)
    f1_weighted = f1_score(y_test, y_pred, average="weighted", zero_division=0)
    
    cm = confusion_matrix(y_test, y_pred, labels=CLASSES)
    clf_report = classification_report(y_test, y_pred, labels=CLASSES, output_dict=True)
    clf_report_text = classification_report(y_test, y_pred, labels=CLASSES)
    
    print("\nDetailed Test Set Classification Report:")
    print(clf_report_text)
    
    print("Confusion Matrix:")
    print(f"{'':<10} Pred: {CLASSES[0]:<10} Pred: {CLASSES[1]:<10} Pred: {CLASSES[2]:<10}")
    for idx, true_cls in enumerate(CLASSES):
        print(f"True: {true_cls:<6} {cm[idx][0]:<15} {cm[idx][1]:<15} {cm[idx][2]:<15}")
        
    # 6. Save all artifacts
    os.makedirs("artifacts/model", exist_ok=True)
    os.makedirs("artifacts/reports", exist_ok=True)
    
    vectorizer = chosen_pipeline.named_steps["tfidf"]
    clf = chosen_pipeline.named_steps["clf"]
    feature_count = len(vectorizer.vocabulary_)
    classes = list(clf.classes_)
    
    # Save scikit-learn pipeline & vectorizer
    joblib.dump(chosen_pipeline, "artifacts/model/turkish_text_classifier.joblib")
    joblib.dump(vectorizer, "artifacts/model/vectorizer.joblib")
    
    # Save vocabulary
    vocab = {k: int(v) for k, v in vectorizer.vocabulary_.items()}
    with open("artifacts/model/vocab.json", "w", encoding="utf-8") as f:
        json.dump(vocab, f, ensure_ascii=False, indent=2)
        
    # Save config.json
    config = {
        "model_name": "TurkishTextClassifier",
        "slug": "turkish-text-classifier",
        "version": "1.0.0",
        "modality": "NLP",
        "task": "text_classification",
        "framework": "scikit-learn",
        "supported_formats": ["joblib"],
        "num_classes": 3,
        "classes": classes,
        "input_dim": feature_count,
        "ngram_range": [1, 2],
        "sublinear_tf": True,
        "class_weight": "balanced",
        "c_param": 2.0,
        "latency_ms": round(latency_ms, 3)
    }
    with open("artifacts/model/config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
        
    # Save metadata.json
    model_metadata = {
        "name": "TurkishTextClassifier",
        "slug": "turkish-text-classifier",
        "architecture": "LinearTfidfClassifier",
        "modality": "NLP",
        "visibility": "PUBLIC",
        "stage": "PRODUCTION",
        "framework": "scikit-learn",
        "tags": ["turkish", "nlp", "text-classification", "intent", "sentiment", "customer-service"],
        "description": "Hafif ve yüksek performanslı Türkçe metin sınıflandırma modeli. Cümleleri Soru, Şikâyet ve Öneri olmak üzere 3 temel kategoriye ayırır.",
        "metrics": {
            "accuracy": round(acc, 4),
            "precision_macro": round(p_macro, 4),
            "recall_macro": round(r_macro, 4),
            "f1_macro": round(f1_macro, 4),
            "precision_weighted": round(p_weighted, 4),
            "recall_weighted": round(r_weighted, 4),
            "f1_weighted": round(f1_weighted, 4),
            "per_class": {
                cls_name: {
                    "precision": round(clf_report[cls_name]["precision"], 4),
                    "recall": round(clf_report[cls_name]["recall"], 4),
                    "f1_score": round(clf_report[cls_name]["f1-score"], 4),
                    "support": clf_report[cls_name]["support"]
                } for cls_name in classes
            }
        },
        "file_size_bytes": os.path.getsize("artifacts/model/turkish_text_classifier.joblib"),
        "license": "MIT",
        "demo_config": {
            "sample_inputs": [
                "Siparişim ne zaman kargoya verilir acaba?",
                "Kargo kutusu ezik ve yırtık geldi, iade talep ediyorum.",
                "Uygulamaya gece modu eklenirse göz yorgunluğu azalır."
            ]
        }
    }
    with open("artifacts/model/metadata.json", "w", encoding="utf-8") as f:
        json.dump(model_metadata, f, ensure_ascii=False, indent=2)
        
    # Save evaluation report
    report = {
        "summary": {
            "accuracy": float(acc),
            "macro_precision": float(p_macro),
            "macro_recall": float(r_macro),
            "macro_f1": float(f1_macro),
            "weighted_precision": float(p_weighted),
            "weighted_recall": float(r_weighted),
            "weighted_f1": float(f1_weighted),
            "training_duration_seconds": float(train_duration),
            "latency_ms_per_sample": float(latency_ms)
        },
        "cv_results": cv_results,
        "classification_report": clf_report,
        "confusion_matrix": cm.tolist(),
        "classes": CLASSES
    }
    with open("artifacts/reports/evaluation_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        
    with open("artifacts/reports/confusion_matrix.txt", "w", encoding="utf-8") as f:
        f.write(f"Classes: {CLASSES}\n\n")
        f.write(f"{'':<10} Pred: {CLASSES[0]:<10} Pred: {CLASSES[1]:<10} Pred: {CLASSES[2]:<10}\n")
        for idx, true_cls in enumerate(CLASSES):
            f.write(f"True: {true_cls:<6} {cm[idx][0]:<15} {cm[idx][1]:<15} {cm[idx][2]:<15}\n")
            
    print("\n[SUCCESS] Model training, export and evaluation completed successfully!")
    print(f"Artifacts saved in artifacts/model/ and artifacts/reports/")

if __name__ == "__main__":
    from sklearn.pipeline import Pipeline
    run_training()
