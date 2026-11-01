"""
Dataset Validator and Quality Assurance
Verifies integrity, label distributions, vocabulary statistics, and splits.
"""

import pandas as pd
import numpy as np

def validate():
    df_all = pd.read_csv("data/turkish_text_dataset.csv")
    df_train = pd.read_csv("data/train.csv")
    df_test = pd.read_csv("data/test.csv")
    
    # 1. Null check
    assert df_all["text"].isnull().sum() == 0, "Null texts found in full dataset"
    assert df_all["label"].isnull().sum() == 0, "Null labels found in full dataset"
    assert df_train["text"].isnull().sum() == 0, "Null texts found in train dataset"
    assert df_test["text"].isnull().sum() == 0, "Null texts found in test dataset"
    
    # 2. Split sum check
    assert len(df_train) + len(df_test) == len(df_all), "Train + Test != Total"
    
    # 3. Leakage check
    train_set = set(df_train["text"].str.strip().str.lower())
    test_set = set(df_test["text"].str.strip().str.lower())
    overlap = train_set.intersection(test_set)
    assert len(overlap) == 0, f"Detected {len(overlap)} overlapping samples!"
    
    # 4. Length stats
    word_counts = df_all["text"].apply(lambda x: len(x.split()))
    char_counts = df_all["text"].apply(len)
    
    print("=== DATASET VALIDATION REPORT ===")
    print(f"Total Samples: {len(df_all)}")
    print(f"Train Samples: {len(df_train)} ({len(df_train)/len(df_all):.1%})")
    print(f"Test Samples:  {len(df_test)} ({len(df_test)/len(df_all):.1%})")
    print("\nLength Statistics:")
    print(f"Word Count -> Mean: {word_counts.mean():.1f}, Min: {word_counts.min()}, Max: {word_counts.max()}")
    print(f"Char Count -> Mean: {char_counts.mean():.1f}, Min: {char_counts.min()}, Max: {char_counts.max()}")
    print("\nLabel Balance (% in train vs test):")
    for lbl in ["Soru", "Şikâyet", "Öneri"]:
        tr_pct = (df_train["label"] == lbl).mean() * 100
        te_pct = (df_test["label"] == lbl).mean() * 100
        print(f"  {lbl:<10}: Train {tr_pct:.2f}% | Test {te_pct:.2f}%")
    print("\n[PASSED] All dataset validation and QA checks passed!")

if __name__ == "__main__":
    validate()
