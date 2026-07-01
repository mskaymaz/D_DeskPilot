# FAZ YOL HARITASI

Amac: Faz kararlarini kalici hafizada tutmak ve ileri asamada nereden devam edecegimizi tek dosyadan gostermek.

## Durum Ozeti
- A fazi: tamamlandi
- B fazi: tamamlandi (kalan yok)
- Mimari yenileme: basladi
- C fazi: mimari yenileme tamamlaninca acilacak

## A Fazi (Tamamlandi)
- [x] Ortak kurallari tek kaynakta toplama
- [x] Encoding/bozuk karakter temizligi
- [x] Operasyon dosyalarina "ne zaman acilir" notlari
- [x] STATE alan zorunluluk/tutarlilik kontrolu
- [x] Turkce adlandirma mini ornek rehberi
- [x] TASK-xxx sablonunu kisa-standart hale getirme

## B Fazi (Tamamlandi)
- [x] Validator'i Git hook + CI'ye baglama
- [x] R.yymmdd_hhmm uretimini commit/bundle/release adimlarinda otomasyon
- [x] HISTORY.md tek komut append
- [x] Yeni repo icin tek komut bootstrap script

B fazinda eklenmeyenler:
- 2026-04-01 itibariyla kalan madde yok.

## C Oncesi Mimari Yenileme (Basladi)
- [x] Tek cumlelik nihai yon netlestirildi
- [x] HEDEF_MIMARI ve TASK-004 acildi
- [x] Mevcut dosyalari cekirdek / operasyon / yardimci / arsiv olarak haritala
- [x] KOMUT_SOZLUGU ve `list?` yuzeyini kur
- [x] Profil ve entegrasyon belgelerini ac
- [x] Bootstrap/validator yapisini yeni agacla senkronla
- [x] `ozetten_kur`, `repoyu_incele`, `temizlik_oner` modlarini resmi hale getir
- [x] Mevcut repo task hafizasini koruma ve `ENTEGRASYON_HARITASI` ciktisini tanimla
- [x] `temizle` komut ailesini guvenli artefakt temizligi olarak yeniden tanimla
- [x] `git diff` tabanli aktif oturum devri katmanini ekle
- [ ] Eski yapidan kalan fazlaliklari temizle ve teknik kirilganliklari kapat

- [x] R.260701_1711: Gorevlerim paneli UI/odak duzeltmeleri ve serbest dagit baslangic cift pencere sorunu kapatildi

## C Fazi (Beklemede)
- [ ] STATE yari otomatik guncelleme
- [ ] "Sadece istenen kapsam" otomatik kontrolu
- [x] Bundle/exe/push scriptlesmesi
- [ ] Kurallari makinece okunur formata tasima
- [ ] Basarili teslim sonrasi otomatik handover snapshot

## Ileri Seviye Uygulama Tetik Notu
- Ileri seviye bir uygulama gelistirme karari alindiginda once mimari yenileme tamamlanir; ardindan C fazindaki tum maddeler planli sekilde devreye alinir.

Ne zaman acilir?
- Faz bazli ilerleme durumu veya sonraki teslim kapsam karari gerektiginde.
