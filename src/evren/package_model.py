"""
Model packaging script for EVREN AI Platform.
Packages model weights, configuration, metadata, and vocabulary into a standard EVREN release bundle.
"""

import json
import os
import shutil
import tarfile
import zipfile

def package_for_evren():
    print("=" * 60)
    print("   PACKAGING TURKISH TEXT CLASSIFIER FOR EVREN AI")
    print("=" * 60)
    
    model_dir = "artifacts/model"
    dist_dir = "artifacts/dist"
    os.makedirs(dist_dir, exist_ok=True)
    
    files_to_package = [
        "config.json",
        "metadata.json",
        "turkish_text_classifier.pt",
        "turkish_text_classifier_full.pt",
        "turkish_text_classifier.joblib",
        "vectorizer.joblib",
        "vocab.json"
    ]
    
    # Verify all files exist
    for f in files_to_package:
        p = os.path.join(model_dir, f)
        if not os.path.exists(p):
            raise FileNotFoundError(f"Missing required packaging artifact: {p}")
        size_kb = os.path.getsize(p) / 1024
        print(f"  + Bundling {f:<32} ({size_kb:>8.2f} KB)")
        
    tar_path = os.path.join(dist_dir, "turkish_text_classifier_v1.0.0.tar.gz")
    with tarfile.open(tar_path, "w:gz") as tar:
        for f in files_to_package:
            full_path = os.path.join(model_dir, f)
            tar.add(full_path, arcname=f"turkish_text_classifier/{f}")
            
    zip_path = os.path.join(dist_dir, "turkish_text_classifier_v1.0.0.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files_to_package:
            full_path = os.path.join(model_dir, f)
            zf.write(full_path, arcname=f"turkish_text_classifier/{f}")
            
    print(f"\n[SUCCESS] Release packages created:")
    print(f"  TAR.GZ: {tar_path} ({os.path.getsize(tar_path)/1024:.2f} KB)")
    print(f"  ZIP:    {zip_path} ({os.path.getsize(zip_path)/1024:.2f} KB)")

if __name__ == "__main__":
    package_for_evren()
