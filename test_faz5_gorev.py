import pytest
from datetime import datetime, timedelta
from gorev_modeli import GorevModeli, GorevOnceligi
from gorev_servisi import GorevServisi

def test_gorev_modeli_olusturma():
    """Görev modelinin temel alanlarını doğrular."""
    gorev = GorevModeli(baslik="Kodları incele", oncelik=GorevOnceligi.YUKSEK)
    
    assert gorev.baslik == "Kodları incele"
    assert gorev.oncelik == GorevOnceligi.YUKSEK
    assert gorev.tamamlandi is False
    assert isinstance(gorev.id, str)

def test_gorev_json_donusumu():
    """Görev modelinin JSON dönüşümünü test eder."""
    bitis = datetime.now() + timedelta(days=2)
    gorev = GorevModeli(
        baslik="Test Görevi", 
        oncelik=GorevOnceligi.DUSUK,
        bitis_tarihi=bitis
    )
    
    sozluk = gorev.to_dict()
    yeni_gorev = GorevModeli.from_dict(sozluk)
    
    assert yeni_gorev is not None
    assert yeni_gorev.baslik == "Test Görevi"
    assert yeni_gorev.oncelik == GorevOnceligi.DUSUK
    assert yeni_gorev.bitis_tarihi.replace(microsecond=0) == bitis.replace(microsecond=0)

def test_gorev_servisi_kayit_ve_yukleme(tmp_path, monkeypatch):
    """Görev servisinin verileri doğru kaydedip yüklediğini doğrular."""
    # Uygulama veri dizini olarak geçici bir klasör kullan
    monkeypatch.setattr("gorev_servisi.APP_DATA_DIR", str(tmp_path))
    
    servis = GorevServisi()
    g1 = GorevModeli(baslik="Görev 1", oncelik=GorevOnceligi.YUKSEK)
    g2 = GorevModeli(baslik="Görev 2", oncelik=GorevOnceligi.NORMAL)
    
    servis.gorev_ekle(g1)
    servis.gorev_ekle(g2)
    
    # Yeni bir servis örneği oluştur (disketten okumasını zorla)
    yeni_servis = GorevServisi()
    assert len(yeni_servis.gorevleri_al()) == 2
    assert yeni_servis.gorevleri_al()[0].baslik == "Görev 1"

def test_gorev_siralamasi():
    """Görevlerin öncelik ve tamamlanma durumuna göre doğru sıralandığını doğrular."""
    servis = GorevServisi()
    # Test verilerini temizle ve yeni ekle
    servis._gorevler = [
        GorevModeli(baslik="Düşük Aktif", oncelik=GorevOnceligi.DUSUK, tamamlandi=False),
        GorevModeli(baslik="Yüksek Tamamlanmış", oncelik=GorevOnceligi.YUKSEK, tamamlandi=True),
        GorevModeli(baslik="Yüksek Aktif", oncelik=GorevOnceligi.YUKSEK, tamamlandi=False),
        GorevModeli(baslik="Normal Aktif", oncelik=GorevOnceligi.NORMAL, tamamlandi=False)
    ]
    
    sirali = servis.gorevleri_sirali_al()
    
    assert sirali[0].baslik == "Yüksek Aktif"
    assert sirali[1].baslik == "Normal Aktif"
    assert sirali[2].baslik == "Düşük Aktif"
    assert sirali[3].baslik == "Yüksek Tamamlanmış"