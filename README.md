# DigitalSaatV2

Windows uzerinde calisan dijital saat uygulamasi. Saat, tarih ve pil bilgisini tek pencerede veya serbest dagit modunda gosterir. Uygulama saydam, cercevesiz ve suruklenebilir bir pencere olarak calisir.

**Surum Bilgisi**
Surum: `V2.050226` (05 Subat 2026)
Windows exe: `DigitalSaatV2.050226.exe`

**Surumleme**
- Format: `V2.YYMMDD` (ornegin: `V2.050226`)
- Ayni gunde ikinci yayin gerekiyorsa: `V2.YYMMDD.1`, `V2.YYMMDD.2`
- Exe adi: `DigitalSaatV2.<surum>.exe`

**Ozellikler**
- Saat, tarih ve pil bilgisini goruntuleme
- Her zaman ustte kalma ve saydamlik ayari
- Cercevesiz pencere ve surukle-birak ile konumlandirma
- Saat gorunumu: font, boyut, renk, kalinlik, saniye gorunumu ve saniye boyutu
- Tarih gorunumu: font, boyut, renk, kalinlik ve format (ozel kisa format veya strftime)
- Pil gorunumu: font, boyut, renk ve kalinlik
- Dusuk pil uyarisi: seviye, tekrar araligi ve uyarı sesi secimi
- Tam dolu uyarisi: seviyeye geldiginde yesil yanip sonme
- Sarjdayken ikon gosterimi
- Otomatik baslatma (Windows acilisinda)
- Serbest dagit modu: pil/saat/tarih satirlari ayri pencerelerde, bagimsiz tasinabilir
- Sag tik menusu: Ayarlar ve Cikis

**Ayarlar**
Ayarlar penceresi sekmeli yapidadir: Genel, Pil, Saat, Tarih. Degisiklikler "Uygula" ile onizleme yapar, "Kaydet" ile kalici olur.

**Kullanim (Kisa Kilavuz)**
- Uygulama acilinca pencereyi tutup surukleyerek konumlandirabilirsiniz.
- Sag tik menusu ile Ayarlar veya Cikis secilebilir.
- Serbest dagit acikken saat/tarih/pil satirlari ayri pencerelere ayrilir ve bagimsiz tasinabilir.
- Ayarlar icindeki renk, font ve boyut degisiklikleri "Uygula" ile hemen gorulur.
- Pil uyarilari ve tam dolu uyarisi Pil sekmesinden yonetilir.

**Changelog**
- V2.050226 (05 Subat 2026)
  - Renk secici kapanma sorunu duzeltildi (Tarih/Saat/Pil renk secimi).
  - Serbest dagit pencereleri artik gorev cubugu ustune tasinabilir.

**Test (Hizli Kontrol)**
- Uygulama acilis ve kapama testi
- Tarih/Saat/Pil renk secici: OK ve kapatma (X) ile cikis testi
- Serbest dagit modunda pencereleri gorev cubugu ustune tasima testi
- Topla ve tekrar dagitinca konumlarin korunmasi
- Sag tik menusu ve Ayarlar penceresi acilis testi
- Pil uyarilari (dusuk/dolu) davranisi testi

**Build ve Release (Tek Komut)**
Release icin once temiz bir git durumuna (commitli) sahip olun.

Ornek:
```
powershell -ExecutionPolicy Bypass -File .\scripts\release.ps1 -Version V2.050226
```

Var olan tag/release uzerine yazmak icin:
```
powershell -ExecutionPolicy Bypass -File .\scripts\release.ps1 -Version V2.050226 -Overwrite
```
