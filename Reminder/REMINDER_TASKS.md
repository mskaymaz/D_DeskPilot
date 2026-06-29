# Reminder Tasks

## Durum Etiketleri

| İşaret | Anlam |
|---|---|
| `[ ]` | Başlanmadı |
| `[~]` | Devam ediyor |
| `[x]` | Tamamlandı |
| `[!]` | Sorunlu / tekrar bakılacak |
| `[?]` | Karar bekliyor |

---

# TASK-001 - Mevcut Hatırlatma Sistemini Analiz Et

## Status

- [ ] Not Started
- [ ] In Progress
- [ ] Completed
- [ ] Needs Review

## Goal

Mevcut hatırlatma sisteminin dosyalarını, veri akışını, UI yapısını ve bildirim sistemini çıkarmak.

## Scope

- [ ] Hatırlatma ile ilgili dosyaları listele
- [ ] Veri kayıt formatını incele
- [ ] Hatırlatma ekleme/düzenleme akışını incele
- [ ] Hatırlatma listesi UI yapısını incele
- [ ] Bildirim servisini incele
- [ ] 500 satır üstü dosyaları belirle

## Acceptance Criteria

- [ ] İlgili dosyalar net listelendi
- [ ] Veri modeli özetlendi
- [ ] Riskli noktalar yazıldı
- [ ] Sonraki task için yol netleşti

## Notes

-

---

# TASK-002 - Veri Modelini Genişlet

## Status

- [ ] Not Started
- [ ] In Progress
- [ ] Completed
- [ ] Needs Review

## Goal

Hatırlatma modeline sesli uyarı alanlarını geriye uyumlu şekilde eklemek.

## Scope

- [ ] `voice_enabled` alanı ekle
- [ ] `voice_alerts` listesi ekle
- [ ] `voice_repeat_rule` alanı ekle
- [ ] `notified_keys` alanı ekle
- [ ] Eski kayıtlar için varsayılan değer üret
- [ ] Bozuk kayıtları güvenli işle

## Acceptance Criteria

- [ ] Eski hatırlatmalar bozulmadan açılıyor
- [ ] Yeni alanlar kaydediliyor
- [ ] Uygulama çökmeden çalışıyor
- [ ] `py_compile` başarılı

## Notes

-

---

# TASK-003 - Kalan Süre Metni Üretici

## Status

- [ ] Not Started
- [ ] In Progress
- [ ] Completed
- [ ] Needs Review

## Goal

TTS ve bildirimlerde kullanılacak Türkçe kalan süre metnini üretmek.

## Scope

- [ ] Dakika metni üret
- [ ] Saat metni üret
- [ ] Gün metni üret
- [ ] `Zamanı geldi` metni üret
- [ ] Geçmiş zaman durumunu yönet

## Acceptance Criteria

- [ ] `5 dakika kaldı`
- [ ] `1 saat kaldı`
- [ ] `3 saat kaldı`
- [ ] `1 gün kaldı`
- [ ] `Zamanı geldi`

## Notes

-

---

# TASK-004 - TTS Servisi Ekle

## Status

- [ ] Not Started
- [ ] In Progress
- [ ] Completed
- [ ] Needs Review

## Goal

Başlık, açıklama ve kalan süreyi okuyabilen TTS servisi eklemek.

## Scope

- [ ] `tts_servisi.py` oluştur
- [ ] Windows TTS / pyttsx3 desteği ekle
- [ ] Erkek ses tercih mekanizması ekle
- [ ] Varsayılan sese düşme ekle
- [ ] Okuma kuyruğu ekle
- [ ] Test okuma fonksiyonu ekle
- [ ] Hata durumunda uygulamayı çökertme

## Acceptance Criteria

- [ ] Başlık okunuyor
- [ ] Açıklama okunuyor
- [ ] Kalan süre okunuyor
- [ ] TTS yoksa uygulama çalışmaya devam ediyor

## Notes

-

---

# TASK-005 - Çoklu Sesli Ön Uyarı Sistemi

## Status

- [ ] Not Started
- [ ] In Progress
- [ ] Completed
- [ ] Needs Review

## Goal

Kullanıcının birden fazla ön uyarı zamanı tanımlamasını sağlamak.

## Scope

- [ ] Hazır seçenekleri ekle
- [ ] Özel süre eklemeyi destekle
- [ ] En fazla 10 uyarı sınırı koy
- [ ] Aynı uyarının tekrar eklenmesini engelle
- [ ] Ana zamandan sonraya uyarı eklemeyi engelle

## Acceptance Criteria

- [ ] 1 gün önce eklenebiliyor
- [ ] 3 saat önce eklenebiliyor
- [ ] 20 dakika önce eklenebiliyor
- [ ] 10 sınırı çalışıyor
- [ ] Tekrar kayıt engelleniyor

## Notes

-

---

# TASK-006 - Tekrarlı Sesli Uyarı Kuralı

## Status

- [ ] Not Started
- [ ] In Progress
- [ ] Completed
- [ ] Needs Review

## Goal

Örneğin “1 gün kala başla, 3 saatte bir hatırlat” kuralını desteklemek.

## Scope

- [ ] Başlangıç süresi alanı ekle
- [ ] Aralık süresi alanı ekle
- [ ] En fazla 1 kural sınırı koy
- [ ] Çakışan uyarıları tekilleştir
- [ ] Ana zamana kadar çalıştır

## Acceptance Criteria

- [ ] 1 gün kala 3 saatte bir çalışıyor
- [ ] Çakışan uyarı iki kez okunmuyor
- [ ] Kural kapatılabiliyor
- [ ] Kural kaydediliyor

## Notes

-

---

# TASK-007 - Hatırlatma Ekle/Düzenle UI Yenileme

## Status

- [ ] Not Started
- [ ] In Progress
- [ ] Completed
- [ ] Needs Review

## Goal

Sesli uyarı seçeneklerini sade ve anlaşılır şekilde hatırlatma formuna eklemek.

## Scope

- [ ] Sesli uyarı açık/kapalı checkbox
- [ ] Hazır ön uyarı seçenekleri
- [ ] Özel uyarı ekleme alanı
- [ ] Tekrarlı uyarı alanı
- [ ] Okunacak metin önizlemesi
- [ ] Limit uyarıları

## Acceptance Criteria

- [ ] Kullanıcı formu karışık bulmadan kullanabiliyor
- [ ] Hatalı girişler engelleniyor
- [ ] Önizleme metni doğru
- [ ] Kaydetme çalışıyor

## Notes

-

---

# TASK-008 - Hatırlatma Listesi Görsel Yenileme

## Status

- [ ] Not Started
- [ ] In Progress
- [ ] Completed
- [ ] Needs Review

## Goal

Hatırlatma listesini kart tabanlı, okunabilir ve modern hale getirmek.

## Scope

- [ ] Kart görünümü
- [ ] Başlık vurgusu
- [ ] Açıklama özeti
- [ ] Tarih/saat gösterimi
- [ ] Aktif/gecikti/tamamlandı/pasif durum renkleri
- [ ] Sesli uyarı ikonu
- [ ] Yaklaşan hatırlatmaları üstte gösterme

## Acceptance Criteria

- [ ] Liste okunabilir
- [ ] Durumlar kolay ayırt ediliyor
- [ ] Sesli uyarı aktifliği görünür
- [ ] UI uygulama genel stiliyle uyumlu

## Notes

-

---

# TASK-009 - Bildirim Popup ve Erteleme

## Status

- [ ] Not Started
- [ ] In Progress
- [ ] Completed
- [ ] Needs Review

## Goal

Windows bildirimi yanında uygulama içi popup ve erteleme seçenekleri sunmak.

## Scope

- [ ] Popup tasarımı
- [ ] Tamamlandı butonu
- [ ] Ertele butonu
- [ ] Aç butonu
- [ ] 5/10/15/30 dakika seçenekleri
- [ ] 1 saat / yarın seçenekleri
- [ ] Özel zaman seçimi

## Acceptance Criteria

- [ ] Popup ana saat görünümünü kapatmıyor
- [ ] Erteleme kaydediliyor
- [ ] Tamamlandı çalışıyor
- [ ] Aç butonu ilgili hatırlatmayı açıyor

## Notes

-

---

# TASK-010 - Ayarlar Entegrasyonu

## Status

- [ ] Not Started
- [ ] In Progress
- [ ] Completed
- [ ] Needs Review

## Goal

Sesli hatırlatma için genel ayarları uygulama ayarlarına eklemek.

## Scope

- [ ] Genel sesli hatırlatma açık/kapalı
- [ ] Erkek ses tercih et
- [ ] Test sesi butonu
- [ ] Varsayılan ön uyarılar
- [ ] Sessiz saatler
- [ ] TTS hata durumunu kullanıcıya göstermeden loglama

## Acceptance Criteria

- [ ] Ayarlar kaydediliyor
- [ ] Test sesi çalışıyor
- [ ] Genel kapatma tüm TTS okumalarını durduruyor
- [ ] Uygulama çökmeden çalışıyor

## Notes

-
