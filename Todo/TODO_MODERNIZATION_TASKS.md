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

## TASK-003 - Task Card Widget`r`n`r`nStatus: Completed

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




---

# TASK-005 - Task State & Workflow Modernization

Status: Planned

## Goal

Transform the Todo module from a simple task list into a structured task management system.

---

## Design Rule

Priority never changes automatically.

State may change automatically.

Priority belongs to the user.

State belongs to the workflow.

---

## Task States

Every task can be in one of the following states:

1. Active
2. Overdue (automatic)
3. Completed
4. Cancelled

Only one visual state may be displayed at a time.

Priority of visual states:

Cancelled

>

Completed

>

Overdue

>

Active

---

## List Organization

▼ HIGH

    Overdue

    Active

▼ NORMAL

    Overdue

    Active

▼ LOW

    Overdue

    Active

────────────────────────

▶ COMPLETED

────────────────────────

▶ CANCELLED

Completed and Cancelled sections are collapsed by default.

---

## Card Overlays

Active

(no overlay)

Overdue

Overlay

SÜRES GEÇT

Semi-transparent Red

Completed

Overlay

TAMAMLANDI

Semi-transparent Green

Cancelled

Overlay

PTAL EDLD

Semi-transparent Gray

Overlay is rendered on its own transparent layer.

It never hides the existing card contents.

---

## Automatic Overdue Detection

Every refresh compares

Current Computer Time

with

Task Due Date

If

CurrentTime > DueDate

and task is still Active

state automatically becomes Overdue.

---

## Description Preview

Card contains

• Title

• One-line description preview

• Conversation bubble icon

Selecting the icon opens a silent dialog.

No system beep.

Dialog contains

Title

Full Description

Readable typography

---

## Delete Policy

Delete never removes a task permanently.

Delete changes the task state to

Cancelled.

Permanent deletion will later be available from

Settings

↓

Cancelled Tasks

---

## Planned Settings

Hide Completed

Hide Cancelled

Highlight Overdue

Auto Archive

Permanent Delete Cancelled

---

Reason

The Todo module should evolve into a lightweight professional task manager while remaining fully offline.
