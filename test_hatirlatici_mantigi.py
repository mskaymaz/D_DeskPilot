from datetime import datetime, timedelta
from hatirlatici_modeli import HatirlaticiModeli, TekrarTipi, HatirlaticiDurumu
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

def test_yaklasan_hatirlaticilari_zamana_gore_siralar(tmp_path, monkeypatch):
    """Yaklaşan görünümün yalnızca aktif ve gelecekteki kayıtları sıraladığını test eder."""
    monkeypatch.setattr("hatirlatici_servisi.APP_DATA_DIR", str(tmp_path))

    servis = HatirlaticiServisi()
    uzak = HatirlaticiModeli(
        baslik="Uzak",
        hatirlatma_zamani=datetime.now() + timedelta(hours=2),
    )
    yakin = HatirlaticiModeli(
        baslik="Yakın",
        hatirlatma_zamani=datetime.now() + timedelta(hours=1),
    )
    tamamlandi = HatirlaticiModeli(
        baslik="Tamamlandı",
        hatirlatma_zamani=datetime.now() + timedelta(minutes=10),
        durum=HatirlaticiDurumu.TAMAMLANDI,
    )

    servis.hatirlatici_ekle(uzak)
    servis.hatirlatici_ekle(tamamlandi)
    servis.hatirlatici_ekle(yakin)

    yaklasanlar = servis.yaklasan_hatirlaticilari_al()
    assert [h.baslik for h in yaklasanlar] == ["Yakın", "Uzak"]

def test_gunluk_hatirlaticilari_bugunu_saat_sirasiyla_getirir(tmp_path, monkeypatch):
    """Günlük özetin yalnızca bugünkü kayıtları saat sırasıyla getirdiğini test eder."""
    monkeypatch.setattr("hatirlatici_servisi.APP_DATA_DIR", str(tmp_path))

    servis = HatirlaticiServisi()
    simdi = datetime.now()
    bugun_gec = HatirlaticiModeli(
        baslik="Bugün Geç",
        hatirlatma_zamani=simdi.replace(hour=9, minute=0, second=0, microsecond=0),
    )
    bugun_yakin = HatirlaticiModeli(
        baslik="Bugün Yakın",
        hatirlatma_zamani=simdi.replace(hour=11, minute=0, second=0, microsecond=0),
    )
    yarin = HatirlaticiModeli(
        baslik="Yarın",
        hatirlatma_zamani=simdi + timedelta(days=1),
    )

    servis.hatirlatici_ekle(bugun_yakin)
    servis.hatirlatici_ekle(yarin)
    servis.hatirlatici_ekle(bugun_gec)

    gunluk = servis.gunluk_hatirlaticilari_al(simdi.date())
    assert [h.baslik for h in gunluk] == ["Bugün Geç", "Bugün Yakın"]

def test_toplu_erteleme_sadece_aktifleri_gunceller(tmp_path, monkeypatch):
    """Toplu ertelemenin aktif kayıtları güncellediğini test eder."""
    monkeypatch.setattr("hatirlatici_servisi.APP_DATA_DIR", str(tmp_path))

    servis = HatirlaticiServisi()
    aktif = HatirlaticiModeli(
        baslik="Aktif",
        hatirlatma_zamani=datetime.now() + timedelta(hours=1),
    )
    tamamlandi = HatirlaticiModeli(
        baslik="Tamamlandı",
        hatirlatma_zamani=datetime.now() + timedelta(hours=1),
        durum=HatirlaticiDurumu.TAMAMLANDI,
    )

    ertelenen_sayi = servis.hatirlaticilari_ertele([aktif, tamamlandi], 15)

    assert ertelenen_sayi == 1
    assert aktif.erteleme_zamani is not None
    assert tamamlandi.erteleme_zamani is None

def test_toplu_etkinlestirme_durumlari_koruyarak_degistirir(tmp_path, monkeypatch):
    """Toplu durum işleminin yalnızca aktif/devre dışı kayıtları değiştirdiğini test eder."""
    monkeypatch.setattr("hatirlatici_servisi.APP_DATA_DIR", str(tmp_path))

    servis = HatirlaticiServisi()
    aktif = HatirlaticiModeli(
        baslik="Aktif",
        hatirlatma_zamani=datetime.now() + timedelta(hours=1),
    )
    devre_disi = HatirlaticiModeli(
        baslik="Devre Dışı",
        hatirlatma_zamani=datetime.now() + timedelta(hours=1),
        durum=HatirlaticiDurumu.DEVRE_DISI,
    )
    tamamlandi = HatirlaticiModeli(
        baslik="Tamamlandı",
        hatirlatma_zamani=datetime.now() + timedelta(hours=1),
        durum=HatirlaticiDurumu.TAMAMLANDI,
    )

    kapatilan = servis.hatirlaticilari_etkinlestir(
        [aktif, tamamlandi],
        False,
    )
    acilan = servis.hatirlaticilari_etkinlestir(
        [aktif, devre_disi, tamamlandi],
        True,
    )

    assert kapatilan == 1
    assert acilan == 2
    assert aktif.durum == HatirlaticiDurumu.AKTIF
    assert devre_disi.durum == HatirlaticiDurumu.AKTIF
    assert tamamlandi.durum == HatirlaticiDurumu.TAMAMLANDI

def test_kacirilan_hatirlaticilar_isaretlenir(tmp_path, monkeypatch):
    """Tolerans süresini aşan aktif kayıtların kaçırıldı işaretlendiğini test eder."""
    monkeypatch.setattr("hatirlatici_servisi.APP_DATA_DIR", str(tmp_path))

    servis = HatirlaticiServisi()
    gecmis = HatirlaticiModeli(
        baslik="Kaçırıldı",
        hatirlatma_zamani=datetime.now() - timedelta(minutes=5),
    )
    yakin = HatirlaticiModeli(
        baslik="Henüz Bekliyor",
        hatirlatma_zamani=datetime.now() - timedelta(seconds=10),
    )
    servis.hatirlatici_ekle(gecmis)
    servis.hatirlatici_ekle(yakin)

    kacirilanlar = servis.kacirilanlari_tara(tolerans_saniye=60)

    assert [h.baslik for h in kacirilanlar] == ["Kaçırıldı"]
    assert gecmis.durum == HatirlaticiDurumu.KACIRILDI
    assert yakin.durum == HatirlaticiDurumu.AKTIF

def test_kacirilan_hatirlaticilar_listesi_sadece_kacirilanlari_getirir(tmp_path, monkeypatch):
    """Kaçırılanlar görünümünün yalnızca ilgili durumdaki kayıtları getirdiğini test eder."""
    monkeypatch.setattr("hatirlatici_servisi.APP_DATA_DIR", str(tmp_path))

    servis = HatirlaticiServisi()
    gecmis = HatirlaticiModeli(
        baslik="Kaçırılan Kayıt",
        hatirlatma_zamani=datetime.now() - timedelta(hours=1),
        durum=HatirlaticiDurumu.KACIRILDI,
    )
    aktif = HatirlaticiModeli(
        baslik="Aktif Kayıt",
        hatirlatma_zamani=datetime.now() + timedelta(hours=1),
    )
    servis.hatirlatici_ekle(aktif)
    servis.hatirlatici_ekle(gecmis)

    liste = servis.kacirilan_hatirlaticilari_al()
    assert [h.baslik for h in liste] == ["Kaçırılan Kayıt"]
