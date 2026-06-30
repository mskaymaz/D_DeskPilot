# Todo Modernization Architecture

## Goal

Todo ekranı, Reminder için de kullanılacak ortak görsel dili kuracak ilk modüldür.

## Principles

- Offline-first.
- Ücretsiz, yerel, API bağımlılığı yok.
- PyQt/PySide uyumlu.
- Türkçe karakterler korunur.
- Dosyalar pratikte 500 satır altında tutulur.
- Büyük UI tek dosyada şişirilmez.
- Todo ve Reminder aynı tasarım dilini paylaşır.

## Target File Structure

- gorev_modeli.py
  - Görev veri modeli.
  - Veri alanları ve dönüşüm işlemleri.

- gorev_servisi.py
  - Yerel JSON saklama.
  - Görev ekleme/silme/güncelleme/sıralama.

- gorev_tema.py
  - Todo tema renkleri.
  - Panel, kart, buton stilleri.
  - İleride Reminder ile ortaklaştırılabilir.

- gorev_karti.py
  - Tek görev için modern kart widgetı.
  - Checkbox, başlık, öncelik, sil butonu.

- gorev_arayuzu.py
  - Ana Todo dialog/panel.
  - Kart listesini yönetir.
  - Panel içi tema kontrollerini barındırır.

- gorev_olcekleme.py
  - Panel boyutu değişince orantılı ölçek hesapları.
  - Font, boşluk, kart yüksekliği, buton ölçüleri.

## UI Direction

- Tablo görünümü kaldırılacak.
- Kart tabanlı listeye geçilecek.
- Gri duvar hissi olmayacak.
- Panel üstünde küçük tema kontrolleri olacak.
- Kullanıcı panel/kart/metin/vurgu rengini değiştirebilecek.
- Resize sırasında tüm öğeler orantılı büyüyüp küçülecek.

## Implementation Order

1. Tema altyapısı.
2. Görev kartı widgetı.
3. Dialog içinde kart listesi.
4. Panel içi tema kontrolleri.
5. Orantılı resize sistemi.
6. Reminder ile ortak tasarım bileşenleri.

