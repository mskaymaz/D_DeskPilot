# Reminder Architecture

## Amaç

Hatırlatma sistemini sadece basit alarm yapısı olmaktan çıkarıp, gelişmiş, görsel olarak güçlü, TTS destekli ve sürdürülebilir bir masaüstü hatırlatma modülüne dönüştürmek.

## Ana İlkeler

- Mevcut çalışan yapı bozulmayacak.
- Kodlar modüler olacak.
- UI, veri modeli ve servis katmanı ayrılacak.
- Her dosya mümkün olduğunca 500 satır altında tutulacak.
- İnternet gerektirmeyen Windows TTS öncelikli olacak.
- Eski hatırlatma kayıtları bozulmadan okunacak.

## Önerilen Modüller

```text
Reminder System
│
├─ reminder_model.py
├─ reminder_store.py
├─ reminder_engine.py
├─ reminder_voice_alerts.py
├─ tts_servisi.py
├─ reminder_popup.py
├─ reminder_dialog.py
└─ reminder_list_ui.py
```

## Katmanlar

### 1. Veri Modeli

Sorumluluklar:

- Hatırlatma başlığı
- Açıklama
- Ana tarih/saat
- Aktif/pasif durumu
- Tamamlandı/gecikti bilgisi
- Sesli uyarı ayarları
- Çoklu ön uyarılar
- Tekrarlı sesli uyarı kuralı

### 2. Kayıt Katmanı

Sorumluluklar:

- JSON dosyasından okuma
- JSON dosyasına yazma
- Eski kayıtları yeni modele dönüştürme
- Bozuk kayıtları uygulamayı çökertmeden atlama/loglama

### 3. Hatırlatma Motoru

Sorumluluklar:

- Yaklaşan hatırlatmaları kontrol etme
- Ön uyarı zamanlarını hesaplama
- Kaçırılan uyarıları değerlendirme
- Tekrarlı uyarı kurallarını işletme
- Uyarıların tekrar tekrar çalmasını engelleme

### 4. Bildirim Katmanı

Sorumluluklar:

- Windows bildirimi gösterme
- Uygulama içi popup gösterme
- Tamamlandı / Ertele / Aç aksiyonlarını yönetme

### 5. TTS Katmanı

Sorumluluklar:

- Başlığı okuma
- Açıklamayı okuma
- Kalan süreyi okuma
- Erkek ses tercih etme
- Ses bulunamazsa varsayılan sese düşme
- Okuma kuyruğu yönetimi

## Sesli Uyarı Okuma Formatı

```text
Hatırlatma: {başlık}.
Açıklama: {açıklama}.
{Kalan süre} kaldı. Zamanı geldiğinde tekrar hatırlatırım.
```

Örnek:

```text
Hatırlatma: Doktor randevusu.
Açıklama: Tahlil sonuçlarını götür.
3 saat kaldı. Zamanı geldiğinde tekrar hatırlatırım.
```

## Sınırlar

- Her hatırlatma için en fazla 10 özel sesli ön uyarı.
- Her hatırlatma için en fazla 1 tekrarlı sesli uyarı kuralı.
- Aynı süre iki kez eklenemez.
- Ana zamandan sonraya ön uyarı eklenemez.
