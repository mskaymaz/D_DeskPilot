# BASLANGIC OZETI

Amac: Besmele'yi ilk kez gorecek ekip uyeleri icin 1 sayfalik hizli giris.

## Besmele Nedir?
- Repo-ustu AI calisma omurgasidir.
- Yeni ve mevcut repolara entegre olabilir.
- Task, hafiza, teslim ve devralma duzenini korur.

## Ilk 3 Dosya
1. `STATE.md`
2. `Besmele/README.md`
3. `Besmele/KOMUT_SOZLUGU.md`

## En Kisa Kullanim
1. `bismillah`
2. aktif durumu oku
3. isi yap
4. `mola` veya `yedek` ile guvenli teslim ver

## En Onemli Komutlar
- `bismillah`: baglama giris
- `eko`: gereksiz detayi azalt
- `list?`: komutlari vitrin gibi ozetle
- `mola` / `yedek`: kaydet, commit et, push et
- `temizle`: guvenli artefakt temizligi
- `optimize`: talimat ve `md` sisligini guvenli analiz et

## list? ile Ne Gorulur?
- giris: `bismillah`, `eko`, `banaver`
- teslim: `mola`, `yedek`
- bakim: `temizle`
- konsolidasyon: `optimize`

## Nerede Ne Var?
- Kok: tetikleyiciler ve durum
- `Besmele/`: kurallar, komutlar, rehberler, hafiza, araclar

## Yeni Repoya Kurulum
1. `AGENTS.md`, `CORE.md`, `STATE.md` kokte olsun
2. `Besmele/` klasoru eklensin
3. `python Besmele/tools/validate_besmele.py` ile kontrol et

## Mevcut Repoda Dikkat
- Mevcut task ve handover dosyalarini silme
- Once oku, sonra esle
- Temizlikte once liste, sonra onay

## Takilinca Nereye Bakilir?
- hizli genel bakis: `Besmele/README.md`
- ekip kullanim rehberi: `Besmele/EKIP_EL_KITABI.md`
- teknik entegrasyon: `Besmele/ENTEGRASYON_REHBERI.md`

Ne zaman acilir?
- Yeni ekip uyesi 2 dakikada sistemi anlamak istediginde.
