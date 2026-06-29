# Todo Tasks

## Durum Etiketleri

| İşaret | Anlam |
|---|---|
| `[ ]` | Başlanmadı |
| `[~]` | Devam ediyor |
| `[x]` | Tamamlandı |
| `[!]` | Sorunlu / tekrar bakılacak |
| `[?]` | Karar bekliyor |

---

# TASK-001 - Mevcut To-do Sistemini Analiz Et

## Status

- [ ] Not Started
- [ ] In Progress
- [ ] Completed
- [ ] Needs Review

## Goal

Mevcut görev/to-do dosyalarını, veri modelini ve UI akışını çıkarmak.

## Scope

- [ ] `gorev_modeli.py` incele
- [ ] `gorev_servisi.py` incele
- [ ] `gorev_arayuzu.py` incele
- [x] Test dosyalarını incele
- [x] Veri saklama yerini belirle
- [x] 500 satır üstü dosya var mı kontrol et
- [x] Unicode/Türkçe karakter sorunu var mı kontrol et

## Acceptance Criteria

- [x] Dosya listesi çıkarıldı
- [x] Mevcut model özetlendi
- [x] UI eksikleri yazıldı
- [ ] İlk uygulanacak görev belirlendi

---

# TASK-002 - To-do Veri Modelini Netleştir

## Goal

Yakın dönem yapılacaklar için sade ama genişletilebilir veri modeli oluşturmak.

## Scope

- [ ] Başlık
- [ ] Açıklama
- [ ] Durum
- [ ] Öncelik
- [ ] Planlanan dönem
- [ ] Sıralama
- [ ] Alt görevler
- [ ] Tamamlanma zamanı
- [ ] Tema/panel ayarları

## Acceptance Criteria

- [ ] Eski kayıtlar bozulmadan açılıyor
- [ ] Yeni alanlar kaydediliyor
- [ ] JSON okunabilir kalıyor

---

# TASK-003 - Modern To-do Paneli Tasarla

## Goal

Gri duvar hissi vermeyen, estetik ve okunabilir panel oluşturmak.

## Scope

- [ ] Kart tabanlı görünüm
- [ ] Başlık alanı
- [ ] Hızlı görev ekleme
- [ ] Bugün / Yarın / Bu Hafta / Tamamlanan filtreleri
- [ ] Öncelik rozeti
- [ ] Durum renkleri
- [ ] Sempatik ikonlar
- [ ] Boş liste görünümü

## Acceptance Criteria

- [ ] Panel düz gri görünmüyor
- [ ] Görevler kart şeklinde
- [ ] Öncelik ve durum kolay ayırt ediliyor
- [ ] UI uygulamanın genel estetiğiyle uyumlu

---

# TASK-004 - Panel İçi Tema Kontrolleri

## Goal

Ayarlar penceresini kalabalıklaştırmadan panel üstünden tema/renk seçimi sağlamak.

## Scope

- [ ] Üst kısma küçük tema butonu ekle
- [ ] Hazır tema paletleri ekle
- [ ] Panel rengi seçimi
- [ ] Kart rengi seçimi
- [ ] Yazı rengi seçimi
- [ ] Çerçeve rengi seçimi
- [ ] Vurgu rengi seçimi
- [ ] Varsayılana dön butonu

## Acceptance Criteria

- [ ] Renkler anlık uygulanıyor
- [ ] Ayarlar penceresi şişmiyor
- [ ] Seçimler kaydediliyor
- [ ] Kontrast kötü olursa uyarı veriliyor veya düzeltiliyor

---

# TASK-005 - Oranlı Resize Sistemi

## Goal

Panel köşeden büyütülüp küçültüldüğünde tüm içerik oranlı büyüsün/küçülsün.

## Scope

- [ ] Resize handle ekle
- [ ] Panel boyutunu kaydet
- [ ] Scale hesabı ekle
- [ ] Yazı boyutlarını ölçekle
- [ ] Checkbox boyutlarını ölçekle
- [ ] Kart padding/margin değerlerini ölçekle
- [ ] İkonları ölçekle
- [ ] Minimum/maksimum scale sınırı koy

## Acceptance Criteria

- [ ] Panel büyüyünce içerik de büyüyor
- [ ] Panel küçülünce okunurluk korunuyor
- [ ] Checkboxlar tıklanabilir kalıyor
- [ ] Boyut kaydediliyor

---

# TASK-006 - Görev Kartı Bileşeni

## Goal

Tek görev için yeniden kullanılabilir kart bileşeni oluşturmak.

## Scope

- [ ] Checkbox
- [ ] Başlık
- [ ] Açıklama özeti
- [ ] Öncelik rozeti
- [ ] Planlanan dönem etiketi
- [ ] Alt görev ilerleme göstergesi
- [ ] Hızlı işlem butonları

## Acceptance Criteria

- [ ] Kart tek başına test edilebilir
- [ ] Tema renklerini kullanıyor
- [ ] Scale sistemine uyuyor
- [ ] Unicode karakterler bozulmuyor

---

# TASK-007 - Hızlı Görev Ekleme

## Goal

Kullanıcının çok hızlı görev eklemesini sağlamak.

## Scope

- [ ] Üstte hızlı giriş alanı
- [ ] Enter ile ekleme
- [ ] Boş başlık engeli
- [ ] Varsayılan öncelik normal
- [ ] Varsayılan dönem bugün

## Acceptance Criteria

- [ ] 2 saniyede görev eklenebiliyor
- [ ] Liste hemen güncelleniyor
- [ ] Kayıt kalıcı oluyor

---

# TASK-008 - Filtreleme ve Arama

## Goal

Görevleri hızlı bulma ve odaklanma imkanı sağlamak.

## Scope

- [ ] Bugün filtresi
- [ ] Yarın filtresi
- [ ] Bu hafta filtresi
- [ ] Tamamlananlar filtresi
- [ ] Arama kutusu
- [ ] Öncelik filtresi

## Acceptance Criteria

- [ ] Filtreler hızlı çalışıyor
- [ ] Arama Türkçe karakterlerle doğru çalışıyor
- [ ] Tamamlananlar gizlenip gösterilebiliyor

---

# TASK-009 - Alt Görevler

## Goal

Büyük işleri küçük adımlara bölme imkanı sağlamak.

## Scope

- [ ] Alt görev ekle
- [ ] Alt görev tamamla
- [ ] Alt görev sil
- [ ] İlerleme oranı göster
- [ ] Tüm alt görevler bitince ana görevi öner

## Acceptance Criteria

- [ ] Alt görevler kaydediliyor
- [ ] İlerleme doğru hesaplanıyor
- [ ] UI karmaşıklaşmıyor

---

# TASK-010 - Unicode ve Kod Temizliği

## Goal

Türkçe karakterleri, dosya boyutlarını ve kod kalitesini güvenceye almak.

## Scope

- [ ] Tüm yeni dosyalar UTF-8
- [ ] Türkçe metinler bozulmuyor
- [ ] Her dosya 500 satır altında
- [ ] UI/servis/model ayrımı korunuyor
- [ ] Kullanılmayan kodlar siliniyor
- [ ] `py_compile` başarılı

## Acceptance Criteria

- [ ] Türkçe karakter sorunu yok
- [ ] 500 satır üstü yeni dosya yok
- [ ] Uygulama açılıyor
- [ ] Temel To-do işlemleri çalışıyor

