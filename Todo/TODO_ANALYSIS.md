# TODO Mevcut Sistem Analizi

## Dosyalar

- gorev_modeli.py: Görev veri modeli ve öncelik enum yapısı.
- gorev_servisi.py: JSON tabanlı yerel/offline görev saklama servisi.
- gorev_arayuzu.py: Mevcut tablo tabanlı görev arayüzü.
- test_faz5_gorev.py: Görev sistemi testleri.

## Mevcut Model

- Başlık
- Öncelik: düşük / normal / yüksek
- Tamamlandı bilgisi
- ID
- Opsiyonel bitiş tarihi
- Oluşturulma zamanı

## Veri Saklama

- Yerel JSON dosyası kullanılıyor.
- Online servis, API, abonelik veya bulut bağımlılığı yok.
- UTF-8 JSON yazımı mevcut.

## Mevcut UI Durumu

- QTableWidget tabanlı.
- Gri/tablo hissi baskın.
- Modern kart yapısı yok.
- Panel içi tema kontrolleri yok.
- Orantılı resize sistemi yok.
- Bugünkü / yarınki / bu haftaki odak yapısı yok.

## lk Uygulanacak Görev

TASK-002 ile modern Todo görsel mimarisi başlatılmalı.

Önerilen ilk kod adımı:
- gorev_tema.py oluştur.
- gorev_karti.py oluştur.
- gorev_arayuzu.py içinde tablo yapısını bozmadan önce tema altyapısı hazırlanmalı.
