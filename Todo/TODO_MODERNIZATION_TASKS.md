# Todo Modernization Tasks

## TASK-001 - Existing Todo Analysis

Status: Completed

Notes:
- gorev_modeli.py incelendi.
- gorev_servisi.py incelendi.
- gorev_arayuzu.py incelendi.
- Mevcut UI tablo tabanlı.
- Yerel JSON saklama mevcut.
- Online bağımlılık yok.

---

## TASK-002 - Theme Foundation

Status: Completed

Goal:
Todo için ayrı tema modeli oluştur.

Files:
- gorev_tema.py

Acceptance:
- Varsayılan tema tanımlandı.
- Panel/kart/buton stilleri ayrıldı.
- Kod py_compile testinden geçti.

---

## TASK-003 - Task Card Widget

Status: Not Started

Goal:
Tek görev için modern kart widgetı oluştur.

Files:
- gorev_karti.py

Acceptance:
- Başlık gösterilir.
- Öncelik gösterilir.
- Checkbox çalışır.
- Sil butonu çalışır.
- Kart görünümü tema alır.

---

## TASK-004 - Replace Table With Card List

Status: Not Started

Goal:
gorev_arayuzu.py içindeki QTableWidget yapısını kart listesine dönüştür.

Files:
- gorev_arayuzu.py
- gorev_karti.py

Acceptance:
- Görevler kart olarak listelenir.
- Ekle/sil/tamamlandı akışı bozulmaz.
- Servis katmanı değişmeden çalışır.

---

## TASK-005 - In-Panel Theme Controls

Status: Not Started

Goal:
Global ayarları şişirmeden Todo panelinin içinde küçük tema kontrolleri ekle.

Acceptance:
- Panel rengi değiştirilebilir.
- Kart rengi değiştirilebilir.
- Metin rengi değiştirilebilir.
- Vurgu/kenarlık rengi değiştirilebilir.

---

## TASK-006 - Proportional Resize

Status: Not Started

Goal:
Panel köşelerden büyüyüp küçülürken UI oranlı ölçeklensin.

Files:
- gorev_olcekleme.py
- gorev_arayuzu.py
- gorev_karti.py

Acceptance:
- Fontlar ölçeklenir.
- Kart yüksekliği ölçeklenir.
- Padding/spacing ölçeklenir.
- Checkbox ve butonlar uyumlu kalır.

---

## TASK-007 - Shared Design Preparation For Reminder

Status: Not Started

Goal:
Todo tasarım dilini Reminder tarafına taşınabilir hale getir.

Acceptance:
- Ortak tema kararları netleşir.
- Kart sistemi Reminder için yeniden kullanılabilir olur.

