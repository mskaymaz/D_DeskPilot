import pytest
from datetime import datetime, timedelta
from hatirlatici_modeli import HatirlaticiModeli, TekrarTipi, HatirlaticiDurumu, asdict
from hatirlatici_servisi import HatirlaticiServisi

def test_hatirlatici_modeli_olusturma():
    """Hatırlatıcı modelinin temel alanlarını doğrular."""
    zaman = datetime.now() + timedelta(hours=1)
    model = HatirlaticiModeli(
        baslik="Test Başlığı",
        hatirlatma_zamani=zaman,
        aciklama="Test Açıklaması"
    )
    
    assert model.baslik == "Test Başlığı"
    assert model.durum == HatirlaticiDurumu.AKTIF
    assert model.tekrar_tipi == TekrarTipi.YOK

def test_hatirlatici_json_donusumu():
    """Modelin JSON sözlüğüne ve geri dönüştürülmesini test eder."""
    zaman = datetime.now().replace(microsecond=0) # ISO format hassasiyeti için
    model = HatirlaticiModeli(baslik="JSON Test", hatirlatma_zamani=zaman)
    
    sozluk = model.to_dict()
    yeni_model = HatirlaticiModeli.from_dict(sozluk)
    
    assert yeni_model is not None
    assert yeni_model.baslik == model.baslik
    assert yeni_model.hatirlatma_zamani == zaman
    assert yeni_model.id == model.id

def test_zamani_gelenleri_tara(tmp_path, monkeypatch):
    """Zamanı geçmiş hatırlatıcıların doğru tespit edilmesini test eder."""
    # Uygulama veri dizini olarak geçici bir klasör kullan
    monkeypatch.setattr("hatirlatici_servisi.APP_DATA_DIR", str(tmp_path))
    
    servis = HatirlaticiServisi()
    
    # 1. Gelecekteki hatırlatıcı (yakalanmamalı)
    gelecek_zaman = datetime.now() + timedelta(days=1)
    h1 = HatirlaticiModeli(baslik="Gelecek", hatirlatma_zamani=gelecek_zaman)
    
    # 2. Geçmişteki hatırlatıcı (yakalanmalı)
    gecmis_zaman = datetime.now() - timedelta(minutes=10)
    h2 = HatirlaticiModeli(baslik="Geçmiş", hatirlatma_zamani=gecmis_zaman)
    
    servis.hatirlatici_ekle(h1)
    servis.hatirlatici_ekle(h2)
    
    gelenler = servis.zamani_gelenleri_tara()
    assert len(gelenler) == 1
    assert gelenler[0].baslik == "Geçmiş"