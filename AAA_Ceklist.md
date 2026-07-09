# D_DeskPilot Geliştirme El Kitabı (Master Checklist)

Sıralama:

Giriş ve Proje Vizyonu
Sistem Çekirdeği
Saat Modülü
Tarih Modülü
Pil Modülü
Hatırlatıcı Modülü
Todo Modülü
Bildirim Sistemi
Ayarlar
Pencere Sistemi
Tasarım Sistemi
Dil Sistemi
Paketleme ve Dağıtım
Kod Kalitesi
Teknik Terimler Sözlüğü


> Bu doküman ürün geliştirme boyunca tek ana kontrol listesidir.
> Her madde tamamlandıkça işaretlenebilir.

---

# 1. Sistem Çekirdeği

- [ ] Tek uygulama örneği (Aynı anda yalnızca bir DeskPilot çalışır.)
- [ ] Güvenli başlangıç / kapanış
- [ ] JSON veri yönetimi
- [ ] Ayarların güvenli kaydedilmesi
- [ ] Log sistemi
- [ ] Hata kurtarma
- [ ] Atomic Write (Önce geçici dosyaya yazıp sonra güvenli şekilde kaydetme.)
- [ ] Otomatik yedekleme

### V2+

- [ ] Event Bus (Modüllerin birbirine doğrudan bağlı olmadan haberleşmesini sağlayan ortak iletişim yapısı.)
- [ ] Service Registry (Servislerin tek merkezden yönetildiği yapı.)

---

# 2. Saat Modülü

# Saat Modülü

- [x] Dijital saat
- [x] Font seçimi
- [x] Dijital font desteği
- [x] Yazı tipi boyutu
- [x] Yazı rengi ve biçimi
- [x] 12 / 24 saat formatı
- [x] Saniye gösterimi
- [x] Serbest konumlandırma
- [x] Günlük alarm oluşturma
- [x] Haftalık alarm oluşturma
- [x] Birden fazla alarm desteği
- [x] Alarm başlığı / kısa açıklama
- [x] Alarm geldiğinde metni sesli okuma (TTS)
- [x] Alarm sesi seçimi
- [-] Alarm ses seviyesi iptal edildi..
- [x] Alarmı ertele (Snooze)
- [x] Alarmı durdur
- [x] Alarmı aktif / pasif yapma
- [x] Alarm listesi yönetimi
- [x] Kaçırılan alarm bildirimi
- [x] Sessiz mod desteği
- [x] Alarm sesleri dinleme eklendi
- [x] Alarm yapısını varsayılana döndürme butonu eklendi


### V2+

- [ ] Dünya saatleri
- [ ] Çoklu saat desteği

---

# 3. Tarih Modülü

- [x] Miladi tarih
- [x] Hicri tarih
- [x] Tarih formatları
- [x] Yazı tipi seçimi (sadece kalın)
- [x] Yazı boyutu
- [x] Yazı rengi ve biçimi
- [x] Tarih modülünü göster / gizle
- [x] Serbest konumlandırma
- [x] Gün adını gösterme (Pazartesi, Salı...)
- [x] Ay adını uzun / kısa gösterme (Ocak / Oca)
- [ ] Hafta numarasını gösterme
- [ ] Hicri tarih gösterimini aç / kapat
- [ ] Miladi ve Hicri tarih sıralamasını değiştirme
- [ ] Özel günleri vurgulama (Resmî ve dinî günler)
- [ ] Bugünün anlamlı günü bilgisi (isteğe bağlı)

### V2+

- [ ] Bölgesel takvim desteği
- [ ] Birden fazla takvim sistemi
- [ ] Takvim açılır penceresi
- [ ] Dünya ülkelerine göre hafta başlangıcı


# 4. Pil Modülü

- [ ] Pil yüzdesi
- [ ] Şarj durumu
- [ ] Şarj oluyor / Dolu / Pilde çalışıyor bilgisi
- [ ] Düşük pil bildirimi
- [ ] Kritik pil uyarısı
- [ ] Tam şarj bildirimi
- [ ] Şarj kablosu takıldı / çıkarıldı bildirimi
- [ ] Kalan tahmini kullanım süresi
- [ ] Tam doluma kalan tahmini süre
- [ ] Pil simgesi gösterimi
- [ ] Pil yüzdesini göster / gizle
- [ ] Pil durum metnini göster / gizle
- [ ] Bildirim seviyelerini kullanıcı belirleyebilsin
- [ ] Sessiz mod desteği
- [ ] Pil bilgisi okunamıyorsa güvenli durum gösterimi
- [ ] Dizüstü / Masaüstü uyumluluğu
- [ ] Serbest konumlandırma
- [ ] Yazı tipi seçimi
- [ ] Yazı boyutu
- [ ] Yazı rengi ve biçimi

### V2+

- [ ] Pil kullanım istatistikleri
- [ ] Günlük pil kullanım grafiği
- [ ] Şarj döngüsü bilgisi (Destekleyen cihazlarda)
- [ ] Pil sağlığı bilgisi (Destekleyen cihazlarda)
- [ ] Enerji tüketim analizi
- [ ] Birden fazla pil desteği


# 5. Hatırlatıcı Modülü (Reminder-YENİ)
Bence özellikle şunlar kullanıcı tarafından her gün kullanılacak özellikler:

⭐⭐⭐⭐⭐ Yaklaşan hatırlatıcılar görünümü
⭐⭐⭐⭐ Günlük özet görünümü
⭐⭐⭐⭐ Toplu erteleme
⭐⭐⭐⭐ Toplu etkinleştirme / devre dışı bırakma
⭐⭐⭐⭐ Kaçırılan hatırlatıcı bildirimi
⭐⭐⭐⭐ Windows açıldığında kaçırılan hatırlatıcıları kontrol etme

## Hatırlatıcı Yönetimi

- [ ] Hatırlatıcı oluşturma
- [ ] Hatırlatıcı düzenleme
- [ ] Hatırlatıcı silme
- [ ] Başlık
- [ ] Açıklama
- [ ] Tarih ve saat seçimi

---

## Tekrarlama

- [ ] Tek seferlik hatırlatıcı
- [ ] Günlük tekrar
- [ ] Haftalık tekrar
- [ ] Aylık tekrar
- [ ] Yıllık tekrar
- [ ] Belirli günlerde tekrar

---

## Bildirim

- [ ] Popup hatırlatma penceresi
- [ ] Bildirim sesi seçimi
- [ ] Hatırlatma metnini sesli okuma (TTS)
- [ ] Erteleme (Snooze)
- [ ] Hatırlatıcıyı kapatma
- [ ] Sessiz mod desteği
- [ ] Kaçırılan hatırlatıcı bildirimi
- [ ] Windows açıldıktan sonra kaçırılan hatırlatıcıları kontrol etme

---

## Liste ve Görünüm

- [ ] Yaklaşan hatırlatıcılar görünümü
- [ ] Günlük özet görünümü
- [ ] Hatırlatıcı listesi görünümü
- [ ] Tamamlanan hatırlatıcılar
- [ ] Geçmiş
- [ ] Filtreleme
- [ ] Arama (Başlık, açıklama ve ilgili alanlarda hızlı arama)

---

## Toplu İşlemler

- [ ] Toplu seçim
- [ ] Toplu silme
- [ ] Toplu erteleme
- [ ] Toplu etkinleştirme / devre dışı bırakma

---

## İstatistik

- [ ] Hatırlatıcı istatistikleri
  - Toplam hatırlatıcı
  - Aktif hatırlatıcı
  - Bugünkü hatırlatıcılar
  - Bu haftaki hatırlatıcılar
  - Tamamlanan hatırlatıcılar
  - Kaçırılan hatırlatıcılar
  - Ertelenen hatırlatıcılar

---

### V2+

## Akıllı Hatırlatıcılar

- [ ] Akıllı tekrar önerileri
- [ ] Konuma bağlı hatırlatıcılar
- [ ] Koşula bağlı hatırlatıcılar
- [ ] Öncelikli hatırlatıcılar
- [ ] Hatırlatıcı kategorileri
- [ ] Etiket sistemi
- [ ] Takvim görünümü
- [ ] Hatırlatıcı analizi ve kullanım raporları



# 5. Hatırlatıcı ************ ESKİSİ ***************

- [ ] Hatırlatıcı oluşturma
- [ ] Tekrar kuralları
- [ ] Erteleme
- [ ] Popup
- [ ] TTS (Bilgisayarın metni sesli okuması.)
****************************
Yani öncelik sıralamam şöyle olur:

⭐⭐⭐⭐⭐ Yaklaşan hatırlatıcılar görünümü
⭐⭐⭐⭐ Günlük özet görünümü
⭐⭐⭐ Hatırlatıcı istatistikleri
⭐⭐ JSON içe/dışa aktarma

# Hatırlatıcı Ek Özellikler

- [ ] Hatırlatıcı oluşturma
- [ ] Hatırlatıcı düzenleme
- [ ] Hatırlatıcı silme
- [ ] Tek seferlik hatırlatıcı
- [ ] Günlük tekrar
- [ ] Haftalık tekrar
- [ ] Aylık tekrar
- [ ] Yıllık tekrar
- [ ] Belirli günlerde tekrar
- [ ] Tarih ve saat seçimi
- [ ] Başlık
- [ ] Açıklama
- [ ] Hatırlatma metnini sesli okuma (TTS)
- [ ] Bildirim sesi seçimi
- [ ] Erteleme (Snooze)
- [ ] Hatırlatıcıyı kapatma
- [ ] Kaçırılan hatırlatıcı bildirimi
- [ ] Hatırlatıcı geçmişi
- [ ] Yaklaşan hatırlatıcılar listesi
- [ ] Tamamlanan hatırlatıcılar
- [ ] Arama Görevler arasında başlık, açıklama ve diğer ilgili alanlara göre hızlı arama yapabilme özelliği.
- [ ] Filtreleme
- [ ] Toplu işlemler
- [ ] Sessiz mod desteği
- [ ] Hatırlatıcı listesi görünümü
- [ ] Popup hatırlatma penceresi
- [ ] Windows açıldıktan sonra kaçırılan hatırlatıcıları kontrol etme
- [ ] JSON içe aktarma
- [ ] JSON dışa aktarma
- [ ] Hatırlatıcı istatistikleri


### V2+

- [ ] Akıllı tekrar önerileri

---


# 6. Todo Modülü (YENİ)

## Görev Yönetimi

- [ ] Görev oluşturma
- [ ] Görev düzenleme
- [ ] Görev tamamlama
- [ ] Görev iptal etme
- [ ] Görev silme
- [ ] Hızlı görev ekleme
- [ ] Görev başlığı
- [ ] Görev açıklaması
- [ ] Son tarih ve saat belirleme
- [ ] Dinamik öncelik sistemi
- [ ] Görev durum simgeleri

---

## Liste ve Görünüm

- [ ] Kart tabanlı görünüm
- [ ] Önceliğe göre sıralama
- [ ] Tarihe göre sıralama
- [ ] Bugün yapılacaklar görünümü
- [ ] Yaklaşan görevler görünümü
- [ ] Süresi geçen görevler görünümü
- [ ] Tamamlanan görevler görünümü
- [ ] Hızlı filtreler
- [ ] Arama (Başlık, açıklama ve ilgili alanlarda hızlı arama)
- [ ] Kart görünüm ayarları
- [ ] Görev renk temaları

---

## Toplu İşlemler

- [ ] Toplu seçim
- [ ] Toplu tamamlama
- [ ] Toplu iptal etme
- [ ] Toplu silme
- [ ] Toplu öncelik değiştirme

---

## Geçmiş ve İstatistik

- [ ] Tamamlanan görev geçmişi
- [ ] Süresi geçen görev geçmişi
- [ ] Görev istatistikleri
    - Toplam görev
    - Aktif görev
    - Tamamlanan görev
    - İptal edilen görev
    - Bugün tamamlanan
    - Bu hafta tamamlanan
    - Süresi geçen görev sayısı

---

## Veri Yönetimi

- [ ] JSON dışa aktarma
- [ ] JSON içe aktarma
- [ ] Otomatik yedekleme

---

## Bildirim ve Hatırlatma

- [ ] Yaklaşan görev bildirimi
- [ ] Süresi geçen görev bildirimi
- [ ] Görev tamamlandı bildirimi
- [ ] Sessiz mod desteği

---

## Görünüm Özelleştirme

- [ ] Kart renkleri
- [ ] Yazı tipi
- [ ] Yazı boyutu
- [ ] Simge boyutu
- [ ] Kart aralıkları
- [ ] Panel boyutu

---

### V2+

## Akıllı Görev Yönetimi

- [ ] Smart Todo (Görevleri analiz ederek öneriler sunan yapı.)
- [ ] Alt görevler (Subtasks)
- [ ] Kontrol listeleri (Checklist)
- [ ] Etiket sistemi
- [ ] Kanban görünümü
- [ ] Takvim görünümü
- [ ] Zaman çizelgesi görünümü

---

## Gelişmiş Organizasyon

- [ ] Kategoriler
- [ ] Görev grupları
- [ ] Favori görevler
- [ ] Arşivleme
- [ ] Yinelenen görevler

---

## Verimlilik

- [ ] Pomodoro entegrasyonu
- [ ] Çalışma süresi takibi
- [ ] Görev tamamlama analizi
- [ ] Başarı istatistikleri
- [ ] Verimlilik raporları

---

## Yapay Zekâ

- [ ] Görev önceliği önerileri
- [ ] Süre tahmini
- [ ] Günlük görev planı önerileri
- [ ] Akıllı görev sıralaması


# 6. Todo  Eski Hali ***************************************

- [x] Görev oluşturma
- [x] Düzenleme
- [x] Öncelik sistemi
- [x] Kart görünümü
- [X] Filtreleme
- [ ] Arama
- [ ] Tema
- [ ] Geçmiş
- Bugün içerisinde yapılacakların özet listesi (Bugün Yapılacaklar)

Ben olsam Todo için öncelik sıram
Özellik	Fayda
Bugün görünümü	⭐⭐⭐⭐⭐
Yaklaşan görevler	⭐⭐⭐⭐⭐
Geciken görevler	⭐⭐⭐⭐⭐
Hızlı filtreler	⭐⭐⭐⭐⭐
Güçlü arama	⭐⭐⭐⭐⭐
Toplu işlemler	⭐⭐⭐⭐
Tek tıkla öncelik değiştirme
Basit istatistik

Geciken Görevler
⚠ Süresi Geçen
Vergi   2 gün geçti
Araç Muayenesi  5 gün geçti gibi
**************************
# Todo Ek Özellikler
- [ ] Görev oluşturma
- [ ] Görev düzenleme
- [ ] Görev silme / iptal etme
- [ ] Görev tamamlama
- [ ] Dinamik öncelik sistemi
- [ ] Son tarih ve saat
- [ ] Kart tabanlı görünüm
- [ ] Önceliğe göre sıralama
- [ ] Tarihe göre sıralama
- [ ] Filtreleme
- [ ] Arama  Görevler arasında başlık, açıklama ve diğer ilgili alanlara göre hızlı arama yapabilme özelliği.
- [ ] Tamamlanan görev geçmişi
- [ ] Süresi geçen görevler
- [ ] Görev renk temaları
- [ ] Kart görünüm ayarları
- [ ] Hızlı görev ekleme
- [ ] Görev açıklaması
- [ ] Görev durum simgeleri
- [ ] Toplu seçim
- [ ] Toplu silme / tamamlama / iptal etme
- [ ] Görevleri dışa aktarma (JSON)
- [ ] Görevleri içe aktarma (JSON)
- [ ] Görev istatistikleri (Toplam, Aktif, Tamamlanan, İptal Edilen)

### V2+

- [ ] Smart Todo (Görevleri analiz ederek öneriler sunan yapı.)
- [ ] Alt görevler
- [ ] Etiket sistemi
- [ ] Kanban görünümü

---

# 7. Ayarlar

- [ ] Genel ayarlar
- [ ] Dil sistemi
- [ ] Tema
- [ ] Fontlar
- [ ] Canlı önizleme

### V2+

- [ ] Profil desteği
- [ ] Senkronizasyon ayarları

---

# 8. Bildirim Sistemi

- [ ] Görsel bildirim
- [ ] Sesli bildirim
- [ ] Sessiz mod

### V2+

- [ ] Akıllı bildirim önceliklendirme

---

# 9. Paketleme

- [ ] EXE oluşturma
- [ ] Asset paketleme
- [ ] Windows başlangıcı

### V2+

- [ ] Otomatik güncelleme

---

# 10. Kod Kalitesi

- [ ] Syntax kontrolleri
- [ ] Manuel testler
- [ ] Performans kontrolleri

### V2+

- [ ] CI (Kod değiştikçe otomatik doğrulama sistemi.)
- [ ] Benchmark (Performans karşılaştırma testleri.)

Not: Alarm kısmı bitti.
