# KURAL KAYNAGI

Amac: Tekrar eden cekirdek kurallari tek kaynaktan yonetmek.

## 0) TAM_DOSYA_OKUMA_YASAGI
- Asistan hicbir zaman tum dosyayi okumaya baslamaz ve tum dosyayi okumaz.
- Varsayilan okuma yalniz gereken satir, blok, baslik veya aranmis hedef parcadir.
- Kullanici acikca tamami istemedikce tam dosya okuma yoktur.

## 1) Ekonomik Token
- Tetik: ekonomik token veya bismillah
- Her cevap/plan/arac/duzeltme/snapshot/commit/push/exe/bundle oncesi sessiz preflight uygulanir.
- Kural: yalniz istenen kapsam, minimum dosya, kisa durum.
- `eko` ve `ozet` aktifken cevap yuzeyi en fazla 2-3 satirdir.
- Kullanici acikca istemedikce cevap asamasinda aciklama, gerekce veya ara rapor yazilmaz.

## 1.1) DERINLIKLI_DURUST_TAVSIYE
- Bu ilke tum yapi icin gecerlidir; tek bir maddeye ozgu degildir.
- AI yalniz komut uygulamaz; mimari, kalite, ergonomi, risk, sadelik ve daha iyi alternatifler konusunda varsayilan olarak dusunur.
- Kullanici acikca daraltmadikca profesyonel urun dusuncesiyle karsi oneride bulunur.

## 1.2) CALISMA_DISIPLINI
- Tek sinir Ekonomik Token ilkesidir; sayisal komut veya dosya butcesi yoktur.
- Islem oncesi okunan dosyalar tek satirda belirtilir; okuma yoksa islem yok.
- Kullanici "fren" yazdiginda surec aninda durdurulur.
- Kalici kararlar ayni turda en az bir referans dosyasina islenir (FAZ_YOL_HARITASI veya HISTORY).

## 1.3) MEVCUT_HAFIZA_KORUMA
- Mevcut repoda bulunan `task`, `roadmap`, `todo`, `progress`, `handover` ve benzeri ilerleme hafizasi otomatik silinmez.
- Bu dosyalar Besmele disi olsa bile once okunur, baglama alinir ve uygun formda haritalanir.
- Temizlik onerisi verilebilir; ancak hafiza dosyalari kullanici onayi olmadan kaldirilmaz.
- Gerekirse mevcut task yapisi aynen korunur, Besmele ise onu referanslayan bir ust katman olarak konumlanir.

## 1.4) TEMIZLIK_GUVENCESI
- `temizle` komut ailesi yalniz uretilmis, gecici, yeniden olusturulabilir artefaktlarla ilgilenir.
- `git` gecmisi, `md` talimatlari, task hafizasi ve tracked kaynak dosyalar varsayilan temizlik kapsaminda degildir.
- Temizlik once listeleme ile baslar; supheli veya tracked dosyalar kullanici onayi olmadan silinmez.
- Temizlik davranisinin ayrintili deseni `Besmele/TEMIZLIK_POLITIKASI.md` dosyasinda tutulur.

## 1.5) OTURUM_DEVIR_GUVENCESI
- Yari kalan uzun calismalarda teknik devam hafizasi icin `git diff` tabanli aktif oturum kaydi tutulabilir.
- Bu kayit `Besmele/oturumlar/AKTIF_OTURUM.md` ve gerekirse `AKTIF_OTURUM.patch` uzerinden okunur.
- Ana hafiza yine `STATE`, aktif `TASK` ve `HISTORY` dosyalaridir; oturum kaydi bunlari tamamlayan ikincil katmandir.
- `yedek/mola` akisi basarisiz olursa aktif oturum kaydi otomatik guncellenir.

## 1.6) OPTIMIZE_GUVENCESI
- `optimize` komutu sisligi azaltmak icin mimari seviyeyi, kapsam gucunu veya etki alanini dusuremez.
- Emin degilse uygula moduna gecmez; `uygun optimize yok` diyebilir.
- `STATE`, `HISTORY`, aktif `TASK` ve diger hafiza dosyalari varsayilan optimize hedefi degildir.
- Ayrintili sinirlar ve karar mantigi `Besmele/OPTIMIZE_POLITIKASI.md` dosyasinda tutulur.

## 2) R Etiketi
- R, kanonik teslim/handover etiketidir.
- Format: R.yymmdd_hhmm
- Zorunlu alanlar: commit/push notu, HISTORY tag, bundle/exe adlari.

## 3) Turkce Adlandirma
- Derleyici/dil/runtime anahtar sozcukleri disi adlandirmalar Turkce secilir.
- Her yeni ad ilk kullaniminda kisa Turkce teknik aciklama tasir (ne icin var + nasil kullanilir).
- Kisa ornekler: `kullanici_listesi`, `giris_dogrulama_yap`, `siparis_ozeti_hesapla`.

## 4) KOK ve Operasyon Ayrimi
- KOK: AGENTS.md, CORE.md, STATE.md
- Operasyon: Besmele/ klasoru

## 5) Bismillah Bootstrap
1. KOKTE yalniz CORE.md ve STATE.md okunur; cikti asgari tutulur.
2. Bismillah yaniti yalnizca iki satirdir: selamlama + hedef sorusu.
3. Operasyon baslayana kadar ek aciklama, listeleme, durum raporu uretilmez.
4. Operasyon gerektiginde Besmele/ altindaki ilgili dosya acilir; tam kapsam korunur.
