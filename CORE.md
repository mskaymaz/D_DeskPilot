# BESMELE CORE

Amac: Bismillah akisinda minimum okuma ile guvenli ve ekonomik token calisma omurgasi saglamak.

Ortak kural kaynagi: Besmele/KURAL_KAYNAGI.md

## 0) Tam Dosya Okuma Yasagi
- Asistan hicbir zaman tum dosyayi okumaya baslamaz ve tum dosyayi okumaz.
- Varsayilan okuma yalniz gereken satir, blok, baslik veya aranmis hedef parcadir.
- Kullanici acikca tamami istemedikce tam dosya okuma yoktur.

## 1) Ekonomik Token
- Tetik: ekonomik token veya bismillah
- Preflight cevap, plan, arac, duzeltme, snapshot, commit, push, exe ve bundle oncesi uygulanir.
- Ilk okuma ust siniri: toplam baglam tokeni en fazla %1.
- Ilk okumada mikro-ozet uygulanir:
  - CORE.md: Amac, Ekonomik Token ve Bootstrap satirlari
  - STATE.md: last_update, active_task, next_step, blockers, last_delivery

## 2) R Etiketi
- R kanonik teslim/handover etiketidir.
- Format: R.yymmdd_hhmm
- Zorunlu kullanim: commit/push notu, HISTORY tag, bundle adi, exe/paket adi.

## 3) KOK ve Operasyon Ayrimi
- KOKTE yalniz tetikleyiciler vardir: AGENTS.md, CORE.md, STATE.md
- Tum operasyon dosyalari Besmele/ klasorundedir.

## 4) Bootstrap
1. bismillah sonrasi yalniz CORE.md ve STATE.md okunur; cikti asgari tutulur, listeleme/aciklama yapilmaz.
2. Hemen ardindan yalniz `Besmele/KOMUT_SOZLUGU.md` okunur; aktif tetikler kisa baglama alinmis olur.
3. Ilk cevap yalnizca iki satirdir: "Bismillah, Baglama alindi, calismaya hazirim." + "Hedef nedir?"
4. Operasyon baslayana kadar ek aciklama, dosya listesi, durum raporu uretilmez.
5. Operasyon gerektiginde Besmele/ altindaki ilgili dosyaya inilir; tam kapsam ve profesyonellik korunur.

## 5) Turkce Adlandirma
- Derleyici/dil/runtime anahtar sozcukleri disindaki adlandirmalar Turkce secilir.
- Her yeni ad, ilk kullaniminda kisa Turkce teknik aciklama tasir (ne icin var + nasil kullanilir).
