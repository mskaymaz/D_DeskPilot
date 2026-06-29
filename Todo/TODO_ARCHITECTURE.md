# Todo Architecture

## Amaç

To-do sistemini günlük ve yakın dönem iş takibi için gelişmiş, modern ve sürdürülebilir bir modül haline getirmek.

## Ayrım

### Reminder

- İleri tarihli olaylar
- Toplantı
- Sınav
- Ödev teslimi
- Randevu
- Fatura
- Zamanı kritik işler
- Sesli/önceden uyarı sistemi

### Todo

- Bugün yapılacak işler
- Yarın yapılacaklar
- Bu hafta takip edilecekler
- Kısa vadeli görevler
- Günlük odak listesi
- Alt görevler
- Öncelik ve ilerleme takibi

## Mimari İlke

```text
Common Core
│
├─ title
├─ description
├─ created_at
├─ updated_at
├─ status
└─ category
│
├─ Reminder Module
│  ├─ due_at
│  ├─ voice_alerts
│  ├─ repeat_rule
│  └─ notification_state
│
└─ Todo Module
   ├─ priority
   ├─ planned_for
   ├─ order
   ├─ checklist
   ├─ focus_today
   └─ completed_at
```

## Önerilen Dosya Yapısı

```text
todo_modeli.py
todo_depo.py
todo_servisi.py
todo_panel.py
todo_formu.py
todo_kart.py
todo_tema.py
todo_resize.py
todo_filtre.py
todo_unicode.py
todo_test_yardimci.py
```

## Katmanlar

### 1. Model Katmanı

Sadece veri yapısını bilir.

Sorumluluklar:

- Görev başlığı
- Açıklama
- Öncelik
- Durum
- Planlanan gün
- Alt görevler
- Tamamlanma bilgisi
- Panel görünüm ayarları

### 2. Depo Katmanı

JSON okuma/yazma işlerinden sorumludur.

Sorumluluklar:

- Görevleri yükleme
- Görevleri kaydetme
- Eski kayıtları yeni modele dönüştürme
- Bozuk veri durumunda uygulamayı çökertmeme

### 3. Servis Katmanı

İş mantığını yönetir.

Sorumluluklar:

- Görev ekleme
- Görev silme
- Görev tamamlama
- Sıralama
- Filtreleme
- Bugün/yaklaşan/tamamlanan ayrımı
- Alt görev ilerleme hesabı

### 4. UI Katmanı

Sadece görsel sunumu ve kullanıcı etkileşimini yönetir.

Sorumluluklar:

- Panel görünümü
- Görev kartları
- Hızlı ekleme
- Filtre çubukları
- Tema kontrolleri
- Resize davranışı

### 5. Tema Katmanı

Ayarlar penceresini şişirmeden panel içi görsel kişiselleştirme sağlar.

Sorumluluklar:

- Panel zemin rengi
- Yazı rengi
- Çerçeve rengi
- Kart rengi
- Öncelik renkleri
- Köşe yumuşaklığı
- Gölge / derinlik etkisi

### 6. Resize Katmanı

Panel büyüyüp küçülürken tüm içerik oranlı büyür/küçülür.

Sorumluluklar:

- Yazı boyutlarını ölçekleme
- Checkbox boyutlarını ölçekleme
- Kart boşluklarını ölçekleme
- İkon boyutlarını ölçekleme
- Butonları ölçekleme
- Minimum/maksimum boyut sınırı

## Kod Kuralları

- Her dosya mümkünse 500 satır altında kalacak.
- UI ve servis kodu karıştırılmayacak.
- Unicode/Türkçe karakterler korunacak.
- `py_compile` zorunlu.
- Dead code bırakılmayacak.
- Tekrarlı stiller `todo_tema.py` içine taşınacak.
- Resize matematiği tek yerde tutulacak.
