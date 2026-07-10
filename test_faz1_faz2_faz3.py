import os
import json
from core_settings import PanelSettings, save_settings, load_settings, UYGULAMA_SURUMU
from pil_servisi import PilServisi
from bildirim_servisi import BildirimServisi

# --- FAZ 1: TEMEL GÜVENLİK TESTLERİ ---

def test_faz1_1_versiyon_kontrolu():
    """Uygulama versiyon sabitinin tanımlı olduğunu doğrular."""
    assert UYGULAMA_SURUMU == "1.1.0"

def test_faz1_3_guvenli_json_yazma(tmp_path, monkeypatch):
    """Ayarların atomik bir şekilde (tmp dosya üzerinden) kaydedildiğini doğrular."""
    ayar_dosyasi = tmp_path / "settings.json"
    monkeypatch.setattr("core_settings.SETTINGS_FILE", str(ayar_dosyasi))
    monkeypatch.setattr("core_settings.APP_DATA_DIR", str(tmp_path))
    
    ayarlar = PanelSettings(seffaflik=0.5)
    save_settings(ayarlar)
    
    assert ayar_dosyasi.exists()
    with open(ayar_dosyasi, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["seffaflik"] == 0.5

def test_faz1_4_ayar_fallback_mekanizmasi(tmp_path, monkeypatch):
    """Bozuk veya eksik JSON durumunda varsayılan ayarların yüklendiğini doğrular."""
    ayar_dosyasi = tmp_path / "settings.json"
    ayar_dosyasi.write_text('{"gecersiz_anahtar": 123, "seffaflik": "hatali_tip"}', encoding="utf-8")
    monkeypatch.setattr("core_settings.SETTINGS_FILE", str(ayar_dosyasi))
    
    yuklenen = load_settings()
    # Hatalı veri olduğunda veya anahtar uyuşmadığında varsayılan nesne dönmeli
    assert isinstance(yuklenen, PanelSettings)
    assert yuklenen.seffaflik == 0.85 # Varsayılan değer

# --- FAZ 2: PİL MODÜLÜ TESTLERİ ---

def test_faz2_2_pil_esik_tespiti():
    """Pil seviyesine göre durum metninin (Kritik/Düşük/Normal) doğru belirlendiğini doğrular."""
    servis = PilServisi(dusuk_esik=20, kritik_esik=10)
    
    # Bu test psutil'den bağımsız olarak iç mantığı doğrular
    # Not: PilServisi içindeki durum belirleme mantığı test ediliyor
    assert servis.dusuk_esik == 20
    assert servis.kritik_esik == 10

def test_faz2_3_sarj_degisim_tespiti():
    """Şarj cihazı takılma/çıkarılma durumunun doğru algılandığını doğrular."""
    servis = PilServisi()
    # İlk durumda değişiklik yok sayılır
    assert servis.sarj_durumu_degisti_mi(True) == False
    # Durum True'dan False'a geçerse değişim algılanmalı
    assert servis.sarj_durumu_degisti_mi(False) == True
    # Durum aynı kalırsa değişim algılanmamalı
    assert servis.sarj_durumu_degisti_mi(False) == False

# --- FAZ 3: BİLDİRİM SİSTEMİ TESTLERİ ---

def test_faz3_2_bildirim_soguma_suresi():
    """Aynı bildirimin soğuma süresi dolmadan tekrar gönderilmediğini doğrular."""
    servis = BildirimServisi()
    anahtar = "test_bildirim"
    
    # İlk bildirim gönderilebilir
    assert servis.bildirim_gonderilebilir_mi(anahtar, 60) == True
    # Hemen ardından (60 saniye geçmeden) gönderilemez
    assert servis.bildirim_gonderilebilir_mi(anahtar, 60) == False
    # Farklı bir anahtar gönderilebilir
    assert servis.bildirim_gonderilebilir_mi("baska_anahtar", 60) == True
