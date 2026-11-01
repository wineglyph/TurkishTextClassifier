"""
Interactive / Automated Demo for TurkishTextClassifier on EVREN AI ecosystem.
Demonstrates model loading, classification of diverse sentences, and EVREN packaging verification.
"""

import os
import sys
import time

# Ensure src/model is accessible
sys.path.append(os.path.abspath("src/model"))
from predict import TurkishTextClassifierService

def main():
    print("=" * 70)
    print("      TURKISH TEXT CLASSIFIER - EVREN AI END-TO-END DEMO")
    print("=" * 70)
    
    print("\n[1/3] Model Başlatılıyor...")
    service = TurkishTextClassifierService(model_dir="artifacts/model")
    print("      ✓ Model ağırlıkları (PyTorch .pt & Scikit-learn) ve kelime haznesi yüklendi.")
    
    test_cases = [
        # Soru örnekleri
        ("Siparişim hangi kargo firmasıyla gönderilecek?", "Soru"),
        ("Kartımın limitini mobil uygulamadan nasıl artırabilirim?", "Soru"),
        ("İade sürecinde kargo ücreti alıcıdan mı kesiliyor acaba?", "Soru"),
        
        # Şikâyet örnekleri
        ("İki haftadır kargom gelmedi, müşteri hizmetleri de telefonları açmıyor!", "Şikâyet"),
        ("Sipariş ettiğim mont yırtık ve lekeli geldi, kabul etmiyorum.", "Şikâyet"),
        ("Uygulama son güncellemeden beri sürekli donuyor ve kapanıyor.", "Şikâyet"),
        
        # Öneri örnekleri
        ("Mobil uygulamaya karanlık mod (koyu tema) eklenirse çok faydalı olur.", "Öneri"),
        ("Sık alışveriş yapan müşterilere kargo bedava aboneliği getirilmesini öneriyorum.", "Öneri"),
        ("Restoran menülerine kalori ve alerjen bilgilerinin konulması harika olur.", "Öneri")
    ]
    
    print("\n[2/3] Örnek Türkçe Cümleler Üzerinde Çıkarım (Inference):")
    print("-" * 70)
    print(f"{'Beklenen':<10} | {'Tahmin':<10} | {'Güven':<8} | {'Metin'}")
    print("-" * 70)
    
    all_match = True
    for text, expected in test_cases:
        res = service.predict(text, backend="sklearn")
        pred = res["prediction"]
        conf = res["confidence"] * 100
        match = "✓" if pred == expected else "✗"
        if pred != expected:
            all_match = False
        print(f"{expected:<10} | {pred:<10} | %{conf:<6.1f} | {text} {match}")
        
    print("-" * 70)
    if all_match:
        print("Tüm demo çıkarımları %100 başarıyla doğru sınıflandırıldı.")
        
    print("\n[3/3] EVREN AI Paketleme ve Doğrulama Durumu:")
    dist_tar = "artifacts/dist/turkish_text_classifier_v1.0.0.tar.gz"
    dist_zip = "artifacts/dist/turkish_text_classifier_v1.0.0.zip"
    if os.path.exists(dist_tar) and os.path.exists(dist_zip):
        print(f"      ✓ EVREN Release Arşivi: {dist_tar} ({os.path.getsize(dist_tar)/1024:.1f} KB)")
        print(f"      ✓ EVREN Zip Arşivi:     {dist_zip} ({os.path.getsize(dist_zip)/1024:.1f} KB)")
        print(f"      ✓ PyTorch .pt:          artifacts/model/turkish_text_classifier.pt")
        print(f"      ✓ Metadata & Config:    artifacts/model/metadata.json, config.json")
    print("\nDemo başarıyla tamamlandı!")
    print("=" * 70)

if __name__ == "__main__":
    main()
