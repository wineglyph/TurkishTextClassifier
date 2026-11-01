"""
Pipeline definitions for TurkishTextClassifier:
1. Turkish text preprocessing and tokenization
2. Feature extraction (TF-IDF with sublinear scaling & n-grams)
3. Model training & inference pipeline
4. Lightweight PyTorch Neural Network mapping for EVREN .pt export
"""

import re
import unicodedata
import numpy as np
import torch
import torch.nn as nn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Turkish character mapping for lowercasing
TURKISH_LOWER_MAP = {
    ord("I"): "ı",
    ord("İ"): "i",
}

def turkish_lower(text: str) -> str:
    """Properly lowercases Turkish text preserving dotted and dotless I."""
    if not isinstance(text, str):
        return ""
    text = text.translate(TURKISH_LOWER_MAP)
    return text.lower()

def preprocess_turkish_text(text: str) -> str:
    """Normalizes Turkish text: lowers, cleans noise, preserves punctuation hints."""
    text = turkish_lower(text)
    # Normalize unicode
    text = unicodedata.normalize("NFKC", text)
    # Remove repeated punctuation
    text = re.sub(r'([!?.,])\1+', r'\1', text)
    # Keep Turkish letters, digits, and basic punctuation
    text = re.sub(r'[^\w\s!?.,]', ' ', text)
    # Collapse multiple whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def build_sklearn_pipeline(c_param: float = 2.0, max_features: int = 5000):
    """Builds a scikit-learn TF-IDF + Logistic Regression pipeline."""
    vectorizer = TfidfVectorizer(
        preprocessor=preprocess_turkish_text,
        ngram_range=(1, 2),
        sublinear_tf=True,
        max_features=max_features,
        token_pattern=r'(?u)\b\w+\b|[!?]'
    )
    
    classifier = LogisticRegression(
        C=c_param,
        max_iter=1000,
        class_weight="balanced",
        random_state=42,
        solver="lbfgs"
    )
    
    pipe = Pipeline([
        ("tfidf", vectorizer),
        ("clf", classifier)
    ])
    return pipe

class LightweightTurkishClassifierNN(nn.Module):
    """
    Lightweight Neural Network classifier operating over sparse/dense TF-IDF features.
    Ideal for packaging into PyTorch weights (.pt) for EVREN AI platform.
    """
    def __init__(self, input_dim: int = 5000, num_classes: int = 3):
        super().__init__()
        self.fc = nn.Linear(input_dim, num_classes)
        self.softmax = nn.Softmax(dim=1)
        
    def forward(self, x):
        logits = self.fc(x)
        return logits
        
    def predict_proba(self, x):
        logits = self.fc(x)
        return self.softmax(logits)
