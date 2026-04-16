# AGENTS.md

Repo: Besmele

## -0) TAM_DOSYA_OKUMA_YASAGI (MUST, VAZGECILMEZ)
- Asistan hicbir zaman tum dosyayi okumaya baslamaz ve tum dosyayi okumaz.
- Varsayilan okuma yalniz gereken satir, blok, baslik veya aranmis hedef parcadir.
- Kullanici acikca tamami istenmedikce tam dosya okuma yoktur.

## -1) Ekonomik Token (MUST)
- Tetik: ekonomik token veya bismillah.
- Preflight cevap, plan, arac, duzeltme, snapshot, commit, push, exe ve bundle oncesi sessizce tekrar edilir.
- Kural: yalniz istenen kapsam, minimum dosya, kisa durum.
- Ortak kaynak: Besmele/KURAL_KAYNAGI.md

## -1.1) DERINLIKLI_DURUST_TAVSIYE (MUST)
- Bu ilke tum yapi icin gecerlidir; tek bir maddeye ozgu degildir.
- AI yalniz komut uygulamaz; mimari, kalite, ergonomi, risk, sadelik ve daha iyi alternatifler konusunda varsayilan olarak dusunur.
- Kullanici acikca daraltmadikca profesyonel urun dusuncesiyle karsi oneride bulunur.

## -2) CALISMA_DISIPLINI (MUST)
- Tek sinir Ekonomik Token ilkesidir; sayisal komut veya dosya butcesi yoktur.
- Isleme baslamadan once okunan dosyalar tek satirda yazilir; okuma yapilmadiysa islem yapilmaz.
- Kullanici "fren" yazarsa aninda durulur; yeni komut/edit calistirilmaz.
- Kalici kararlar unutulmasin diye ilgili referans dosyasina ayni turda not dusulur (en az bir dosya: FAZ_YOL_HARITASI veya HISTORY).

## 0) R Etiketi (MUST, UNUTULMAZ)
- R, kanonik teslim/handover etiketidir.
- Dogru format: R.yymmdd_hhmm
- Zorunlu yerler: commit/push notu, HISTORY tag, bundle dosya adi, exe/paket dosya adi.
- R ekle denirse yalniz harf eklenmez, tam format eklenir.

## 1) Bismillah
1. Yalniz CORE.md ve STATE.md oku.
2. Hemen ardindan Besmele/KOMUT_SOZLUGU.md oku.
3. Ilk satir: Bismillah, Baglama alindi, calismaya hazirim.
4. Sonraki satirda hedef sor.

## 2) Yol Haritasi
- KOKTE sadece tetikleyiciler kalir: AGENTS.md, CORE.md, STATE.md
- Tum operasyon dosyalari Besmele/ klasorundedir.

## 3) Operasyon Dosya Yollari
- Besmele/README.md
- Besmele/KURAL_KAYNAGI.md
- Besmele/HEDEF_MIMARI.md
- Besmele/KOMUT_SOZLUGU.md
- Besmele/OPTIMIZE_POLITIKASI.md
- Besmele/PROFIL_REHBERI.md
- Besmele/ENTEGRASYON_REHBERI.md
- Besmele/WORKBOARD.md
- Besmele/HISTORY.md
- Besmele/FAZ_YOL_HARITASI.md
- Besmele/optional/CIHAZ_TESTI.md
- Besmele/plans/TASK-xxx.md
- Besmele/plans/TASK-SABLON.md
- Besmele/tools/validate_besmele.py

## 4) Turkce Adlandirma ve Ilk Kullanim Aciklamasi (MUST)
- Derleyici/dil/runtime anahtar sozcukleri disindaki tum adlandirmalar Turkce secilir.
- Her yeni ad, ilk kullaniminda kisa Turkce teknik aciklama tasir (ne icin var + nasil kullanilir).

Not: Varsayilan teknoloji listesi sinirlayici degildir; asistan gerekceyle farkli dil/cati onerebilir. Son karar her zaman kullanicidadir.
