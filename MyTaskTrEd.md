## [ ] Doküman Kullanım Kuralı

- [x] `MyTaskTrEd.md` aktif çalışma checklist dosyasıdır.
- [ ] Yapılan başlıklar ve maddeler bu dosyadan silinerek ilerlenir.
- [ ] Kalıcı ana yapı `MyTaskTr.md` dosyasında korunur; master yapı oradan takip edilir.
- [ ] AI/Codex bu dosyada kalan en üst ilgili başlığı mevcut çalışma alanı olarak kabul eder; emin değilse kullanıcıdan netleştirme ister.
- [ ] Yeni görev eklemek gerekiyorsa önce `MyTaskTr.md` master yapısına uygunluğu kontrol edilir.

---

## [ ] Ürün Tanımı

D_DeskPilot, PySide6/PyQt6 ile geliştirilen, yerel öncelikli bir Windows masaüstü üretkenlik yardımcısıdır.

Temel amaç:
- [ ] Hafif bir masaüstü yüzeyi üzerinde saat, tarih ve pil durumunu göstermek.
- [ ] Hatırlatıcılar, yapılacak işler, bildirimler, ayarlar, sistem tepsisi kontrolü ve yerleşim davranışını tek uygulamada toplamak.
- [ ] v1 için özel, çevrimdışı, ücretsiz, kararlı ve Türkçe öncelikli kalmak.
- [ ] v1 kararlılığı tamamlanmadan başlatılmamak üzere gelecekteki yerelleştirme, senkronizasyon, mobil ve daha geniş üretkenlik özelliklerini izlemek.

## [ ] Mevcut Odak Kilidi

- [ ] Mevcut odak Faz 6 / Todo üzerindedir.
- [ ] Görev 6.2 tamamlanana kadar Hatırlatıcı, Senkronizasyon, Mobil, Paketleme veya genel yayın çalışmaları başlatılmamalıdır.
- [ ] Faz 10 yalnızca gelecek vizyonudur; mevcut Todo odağı sırasında uygulanmamalıdır.

## [ ] Vazgeçilmez Kurallar ***

- [x] Tam yerelleştirmeden önce Türkçe öncelikli v1 kararlılığı gelir.
- [x] v1 içinde ücretli servis, ücretli API, bulut bağımlılığı, kullanıcı hesabı veya zorunlu internet olmayacaktır.
- [x] v1 için veri saklama modeli JSON olarak kalacaktır.
- [???] İş mantığı servislerde/modellerde olmalı; arayüz yalnızca durumu göstermeli ve eylem göndermelidir.
- [x] Yamalar küçük ve özellik kapsamlı tutulmalıdır.
- [x] Mevcut görev uygulanırken ilgisiz dosyalar ve bölümler değiştirilmemelidir. Doğru yere odaklanılmalıdır.
- [x] Çalışan dosyalar; hata, özellik, performans veya dosya boyutu riski gerektirmedikçe refaktör edilmemelidir.
- [x] Dosyalar tercihen 400 satırın altında tutulmalıdır; 600 satır yalnızca kaçınılmazsa kabul edilmelidir.
- [ ] Her görevden sonra uygulama çalışır durumda kalmalıdır.
- [ ] Python kod düzenlemelerinde, değiştirilen dosya için söz dizimi kontrolü çalıştırılmalı veya neden atlandığı belirtilmelidir.

## [ ] Uygulama Kapısı ***

Uygulamadan önce:
- [x] Yalnızca mevcut görev ve doğrudan ilgili dosyalar okunmalıdır.
- [x] Değişebilecek dosyalar/katmanlar belirlenmelidir.
- [x] Benzer mantığın zaten mevcut olup olmadığı kontrol edilmelidir.
- [x] Gelecek görevlerin uygulanmasından kaçınılmalıdır.

Uygulamadan sonra:

- [x] Söz dizimi/test sonucu bildirilmeli veya çalıştırılmadıysa açıkça söylenmelidir.
- [x] Görev, yalnızca istenen kapsam tamamlandıktan sonra tamamlandı işaretlenmelidir.
- [x] Mevcut görev kullanıcı tarafından doğrulanmadan sonraki göreve geçilmemelidir.

## [ ] Mevcut Repo Durumu***

- [x] Pull sonrası mevcut dal: `main`.
- [x] Mevcut odak: Türkçe v1'i kararlı hale getirmek.
- [???] QuickActions kararlı/dondurulmuş kabul edilir. Açıkça istenmedikçe değiştirilmemelidir.
- [ ] Görev dışında kirli dosyalar bulunabilir; ilgisiz değişikliklerin üzerine yazılmamalıdır.

## [ ] Mevcut Mimari Özeti ***

- [x] Giriş: `main.py` -> `DeskPilot.py`. Her iki isimde olabilir. main.py kullanım kolaylığına ve hatırlamaya sahip.
- [ ] Ana pencere: `core_window.py`; pencere/çalışma zamanı/gezinme/ayarlar/üstte tutma/serbest yerleşim mixin'leriyle oluşur.
- [ ] Ayarlar: `core_settings.py`, `deskpilot.settings.json`, `ui_settings.py`, `ui_ayarlar_formlar.py`.
- [ ] Saat/tarih/pil: ana panel widget'ları ve `pil_servisi.py`.
- [ ] Hatırlatıcılar: `hatirlatici_modeli.py`, `hatirlatici_servisi.py`, `hatirlatici_listesi.py`, `hatirlatici_popup.py`.
- [ ] Todo: `gorev_modeli.py`, `gorev_servisi.py`, `gorev_arayuzu.py`, `kart.py`, `quick_actions.py`.
- [ ] Sistem tepsisi: `sistem_tepsisi.py`.
- [ ] Bildirim/günlükleme: `bildirim_servisi.py`, `log_servisi.py`, `utils.py`.
- [ ] i18n temeli: `dil_yonetimi.py`, `translations/*.json`.

## [ ] Tamamlanma İşaretleri ***

- [ ] `[x]` tamamlandı ve mevcut repoda var.
- [ ] `[ ]` bekliyor.
- [ ] `[~]` kısmi/devam ediyor; tamamlanmış sayılmamalıdır.
- [ ] `[!]` engelli veya açık karar gerektiriyor.

---

# [x] Faz 0 - Yönetim ve Güvenlik ***

Bu faz, geliştirme sırasında dağılmayı önleyen ana kuralları belirler. Amaç; tek görev kaynağı, sınırlı kapsam ve güvenli patch düzenini korumaktır.

## [ ] Görev 0.1 - Tek Görev Kaynağını Koru

**Geliştirici Notu:** Bu görev, hangi dosyanın ana plan olduğunu netleştirmek içindir. Birden fazla aktif checklist kalırsa geliştirme yönü karışır ve aynı iş iki farklı yerde farklı görünebilir.

Amaç:
- [x] Tek bir aktif ilerleme kaynağı tutmak ve paralel checklist kaymasını önlemek.

Kapsam:
- [x] Yalnızca görev yol haritası dokümanları.

Tamamlanma Kriterleri:
- [x] `Task.md` mevcut ana yol haritasıdır.
- [x] Gereksiz görev işaretçi dokümanları mevcut repodan kaldırıldı.
- [x] Ana yol haritasından fazla modül bazlı checklist'ler kaldırıldı.
- [x] İncelemeden sonra `MyTask.md` dosyasının `Task.md` yerine geçip geçmeyeceğine karar ver. Karar verildi. MyTask.md Task.md yapısının aktif görevi iptal edil. Ayrıca MyTaskTr.md MyTask.md yapısının Türkçe verisyonu ve yazılım yöneticisi için üretildi ve bunun üzerinden yazılım aşamaları takip ve devam edilecek.
- [x] Her tamamlanan özellikten sonra seçilen ana görev dosyasını güncelle.

## [ ] Görev 0.2 - Kapsamlı Çalışma Kurallarını Koru ***

**Geliştirici Notu:** Bu görev, SPP/EKO tarzı kontrollü geliştirme disiplinini korur. Amaç hızlı ama dağınık değişiklik yapmak değil, küçük ve doğrulanabilir adımlarla ilerlemektir.

Tamamlanma Kriterleri:
- [x] Repo talimatlarında SPP/EKO tarzı kurallar var.
- [x] Ekonomik token çalışma akışı tanımlı.
- [x] Görev uygulama kapısı mevcut.
- [x] Task okuma yapısı open ai ve codex yapısı tarafından başarılı olarak belirli bir aşamadan sonra sürdürülemediği için yazılım yöneticisi tarafından takip edilecek ve nelerin yapılacağı yönetici tarafından adım adım belirlenecek.
- [x] Ayrıntı istenmedikçe nihai görev cevaplarını kısa tut.
- [x] Commit ve yamaların açıklamalarını özellikle kapsamlı tut ve R zaman etiketini eklemeyi unutma.


# [ ] Faz 1 - Başlangıç, Ayarlar, Depolama ***

Bu faz, uygulamanın açılışını, ayar yönetimini ve JSON veri saklama güvenliğini sağlamlaştırır. Uygulama kapanıp açılsa bile veri kaybı olmamalı ve bozuk dosyalar sessizce çöküşe sebep olmamalıdır.

## [ ] Görev 1.1 - Uygulama Girişi ve Tekil Örnek

**Geliştirici Notu:** Uygulamanın aynı anda birden fazla kopya halinde açılmasını önlemek gerekir. Başlangıç sırasında eksik varlık veya basit hata varsa kullanıcıya anlaşılır şekilde yansıtılmalıdır.

Tamamlanma Kriterleri:
- [x] `main.py` başlatıcısı mevcut.
- [x] `DeskPilot.py` ana uygulama girişi.
- [x] Windows üzerinde tekil örnek mutex'i mevcut.
- [x] Temel başlangıç günlüklemesi mevcut.
- [ ] Temiz Windows oturumunda başlangıcı doğrula.
- [ ] Opsiyonel varlıklar eksikken başlangıcı doğrula.
- [ ] Yalnızca gerekirse net bir kritik başlangıç hata mesajı ekle.

## [ ] Görev 1.2 - Ayar Modeli ve JSON Kalıcılığı ***

**Geliştirici Notu:** Ayarlar her ne kadar eski ayarlar ile başlamışsa da yeni yapının ayarları eski olarak kalmak zorunda değil, ayarları güncel yapıya göre güncellemek gerekir. Bu prensip olmalı.

Tamamlanma Kriterleri:
- [x] `PanelSettings` mevcut.
- [x] Ayarlar uygulama verisinden veya yerel yedekten yükleniyor.
- [x] Eksik/bilinmeyen anahtarlar güvenli şekilde işleniyor.
- [x] Atomik ayar yazımı temp + replace kullanıyor.
- [x] Bozuk ayar dosyası yedekleniyor.
- [ ] Eski anahtar geçişlerini ve varsayılanları gözden geçir.
- [ ] Ölçek, opaklık, eşikler, aralıklar ve konumları sınırla.
- [ ] Yalnızca kullanışlı ve bakımı yapılabilir kalacaksa config örneği ekle.

## [ ] Görev 1.3 - Genel JSON Deposu Sağlamlaştırma

**Geliştirici Notu:** Ayarlardaki güvenli yazma yaklaşımı Todo ve Hatırlatıcı verilerine de uygulanmalıdır. Yarım kalan yazma işleminde kullanıcı verisi kaybolmamalıdır.

Amaç:
- [ ] Eski repodaki güvenli depolama vizyonunu tüm JSON kalıcılığına uygulamak.

Tamamlanma Kriterleri:
- [ ] Todo ve hatırlatıcılar için atomik yazma kullan.
- [ ] Todo/hatırlatıcılar için `.bak` kurtarma planı ekle.
- [ ] Kurtarma olaylarını günlükle.
- [ ] Sadece basit kalacaksa gizli ikincil yedek ekle.
- [ ] Yazma yarıda başarısız olursa veri kaybını önle.

## [ ] Görev 1.4 - Uygulama Yaşam Döngüsü

**Geliştirici Notu:** Başlangıç ve kapanış sırası açık olmalıdır. Servisler, zamanlayıcılar, sistem tepsisi ve bekleyen yazmalar kontrolsüz bırakılmamalıdır.

Amaç:
- [ ] Başlangıç ve kapanış sıralamasını açık tutmak.

Tamamlanma Kriterleri:
- [ ] Günlükleyici, ayarlar, depolama, servisler, sistem tepsisi ve arayüz için başlangıç sırasını tanımla.
- [ ] Zamanlayıcılar, sistem tepsisi, servisler ve bekleyen yazmalar için kapanış sırasını tanımla.
- [ ] Servis başlangıç hatasını sessiz çöküş olmadan ele al.
- [ ] Yaşam döngüsü mantığını küçük tut; uygulamayı yeni bir framework mantığıyla baştan yazma.

## [ ] Görev 1.5 - Olay Veriyolu (Event Bus)

**Geliştirici Notu:** Bu görev şimdilik ertelenmiştir. Ancak servisler ile arayüz arasındaki doğrudan bağlantı riskli hale gelirse basit bir olay sistemi gerekebilir.

Durum:
- [ ] Dokunulan kod gerektirmedikçe ertelendi.

Tamamlanma Kriterleri:
- [ ] Servisten arayüze güncellemeler için olay sınırlarını tanımla.
- [ ] Doğrudan bağlılık riskli hale gelirse basit subscribe/unsubscribe/publish ekle.
- [ ] Abone hatalarının tüm olayları bozmasını önle.
- [ ] Async framework eklemekten kaçın.

## [ ] Görev 1.6 - Servis Kayıt Merkezi (Service Registry)

**Geliştirici Notu:** Bu gelecek mimari çalışmasıdır. Mevcut uygulama tek adımda kayıt merkezi etrafında yeniden yazılmamalıdır.

Durum:
- [ ] Gelecek mimarisi için ertelendi.

Tamamlanma Kriterleri:
- [ ] Registry eklemenin ne zaman değerli olacağını tanımla.
- [ ] Bağımlılık bağlamayı basit tut.
- [ ] Uygulamayı tek adımda registry etrafında yeniden yazma.

---

# [ ] Faz 2 - Saat, Tarih, Pil

Bu faz ana görünür modüllerin kararlılığına odaklanır. Saat, tarih ve pil bileşenleri hem normal panelde hem serbest yerleşimde davranışını korumalıdır.

## [ ] Görev 2.1 - Saat Modülü Kararlılığı

**Geliştirici Notu:** Saat modülü uygulamanın ana yüzüdür; bu yüzden mevcut çalışan davranış korunmalıdır. Saniye genişlik zıplaması gibi ertelenmiş konular yalnızca açıkça istenirse ele alınmalıdır.

Tamamlanma Kriterleri:
- [x] Saat modülü mevcut.
- [x] Saat için dijital font render yolu mevcut.
- [x] Saat için stencil/varsayılan font yolu mevcut.
- [x] Sistem fontları seçilebilir kalıyor.
- [x] Saat font ölçekleme mevcut.
- [x] Saat ayarları yeniden başlatmadan sonra korunuyor.
- [ ] Saniye görünürlüğü anahtarını doğrula.
- [ ] Saniye görünürlüğü davranışını kararlı tut.
- [ ] Serbest yerleşimde saat davranışını kararlı tut.
- [ ] Açıkça istenmedikçe saniye genişliği titreme düzeltmesini ertele.

## [ ] Görev 2.2 - Tarih Modülü Kararlılığı

**Geliştirici Notu:** Tarih görünümü format, font ve görünürlük ayarlarıyla birlikte korunmalıdır. Dokunulduğunda yeniden başlatma ve serbest yerleşim etkileri de kontrol edilmelidir.

Tamamlanma Kriterleri:
- [x] Tarih modülü mevcut.
- [ ] Tarih formatı ayarını doğrula.
- [ ] Tarih fontu ayarını doğrula.
- [ ] Tarih görünürlüğü anahtarını doğrula.
- [ ] Dokunulduğunda tarih formatı, fontu, görünürlüğü, yeniden başlatma ve serbest yerleşim davranışını kararlı tut.

## [ ] Görev 2.3 - Pil Modülü Kararlılığı

**Geliştirici Notu:** Pil modülü cihazda pil yoksa veya bilgi alınamazsa güvenli davranmalıdır. Sessiz mod açıkken uyarı davranışı ayrıca korunmalıdır.

Tamamlanma Kriterleri:
- [x] Pil modülü mevcut.
- [x] Pil eşikleri mevcut.
- [x] Şarja takma/çıkarma algısı mevcut.
- [ ] Pil bilgisi alınamıyorsa güvenli geri dönüş davranışını koru.
- [ ] Düşük/kritik/dolu uyarı davranışını kararlı tut.
- [ ] Pil uyarılarında sessiz moda uyulmasını sağla.
- [ ] Yeniden başlatmadan sonra pil görüntüsünü doğrula.

---

# [ ] Faz 3 - Pencere, Yerleşim, Sistem Tepsisi

Bu faz pencere davranışı, serbest yerleşim ve sistem tepsisi kontrolünü korur. Özellikle QuickActions kararlı kabul edildiği için açıkça istenmedikçe dokunulmamalıdır.

## [ ] Görev 3.1 - Ana Pencere Kararlılığı

**Geliştirici Notu:** Ana pencere şeffaf, sürüklenebilir ve üstte kalma davranışıyla çalışır. Bu davranışlara dokunurken popup focus ve topmost sorunları yeniden üretilmemelidir.

Tamamlanma Kriterleri:
- [x] Şeffaf sürüklenebilir ana pencere mevcut.
- [x] Her zaman üstte davranışı ayrıştırıldı/kararlı hale getirildi.
- [x] Popup focus/topmost davranışı iyileştirildi.
- [ ] Gruplanmış başlangıç, eksik monitör geri dönüşü ve ölçekleme davranışını kararlı tut.
- [ ] Sağ tık + mouse wheel ölçeklemeyi doğrula.

## [ ] Görev 3.2 - Serbest Yerleşim (Free Layout)

**Geliştirici Notu:** Serbest yerleşim kullanıcının modülleri kendi konumunda tutmasını sağlar. Mevcut kayıtlı konum ve ölçek davranışı bozulmamalıdır.

Tamamlanma Kriterleri:
- [x] Serbest yerleşim mevcut.
- [x] Ayarlarda çoklu monitör alanları mevcut.
- [ ] Serbest yerleşim başlangıç davranışını koru.
- [ ] Tüm modülleri birlikte taşıma davranışını koru.
- [ ] Widget bazlı kayıtlı konumları ve ölçek sınırlarını koru.
- [ ] Yalnızca mevcut arayüze uygunsa düzenleme komutu ekle.

## [ ] Görev 3.3 - Sistem Tepsisi

**Geliştirici Notu:** Sistem tepsisi uygulamanın günlük kontrol noktasıdır. Göster/gizle, yeni hatırlatıcı, yeni görev ve çıkış gibi eylemler kararlı kalmalıdır.

Tamamlanma Kriterleri:
- [x] Sistem tepsisi entegrasyonu mevcut.
- [x] Göster/gizle eylemi mevcut.
- [x] Yeni Hatırlatıcı eylemi mevcut.
- [x] Yeni Todo eylemi mevcut.
- [x] Ayarlar eylemi mevcut.
- [x] Çıkış eylemi mevcut.
- [x] Sistem tepsisi tooltip özeti mevcut.
- [ ] Kapat/göster/gizle davranışını kararlı tut.
- [ ] Sistem tepsisi desteklenmiyorsa fallback'i basit tut.
- [ ] Yayından önce tepsi menüsü eylemlerini manuel doğrula.

## [ ] Görev 3.4 - Görüntüleme Modları

**Geliştirici Notu:** Eski overlay/combined/separated fikirleri şu an ertelenmiş vizyondur. Mevcut ana yüzey ve serbest yerleşim bunları zaten karşılıyorsa yeni mod eklenmemelidir.

Durum:
- [ ] Mevcut uygulama şu an mevcut ana/serbest yerleşim desenlerini kullanıyor; eski overlay/combined/separated vizyonu bilinçli olarak canlandırılmadıkça ertelidir.

Tamamlanma Kriterleri:
- [ ] Görev çubuğu overlay modunun v1'e ait olup olmadığına karar ver.
- [ ] Masaüstü birleşik modunun mevcut ana yüzeyden farklı olup olmadığına karar ver.
- [ ] Ayrı widget'ların zaten serbest yerleşim tarafından karşılanıp karşılanmadığına karar ver.
- [ ] Canlandırılırsa ortak saat/tarih/pil mantığını koru ve çift zamanlayıcıdan kaçın.

## [ ] Görev 3.5 - Pencere Katmanlama Yöneticisi

**Geliştirici Notu:** Topmost sorunu geri dönmedikçe bu çalışma ertelenmelidir. Eklenirse CPU artışı veya focus çalma gibi yan etkiler oluşturmamalıdır.

Durum:
- [ ] Topmost kararsızlığı geri dönmedikçe ertelendi.

Tamamlanma Kriterleri:
- [ ] Normal topmost davranışı yetersizse ayarlanabilir topmost yenileme ekle.
- [ ] Yenileme aralığını güvenli aralığa sınırla.
- [ ] Gizli veya yok edilmiş pencereleri güvenli şekilde atla.
- [ ] CPU artışı veya focus çalma regresyonu olmadığını doğrula.

---

# [ ] Faz 4 - Bildirim Sistemi

Bu faz bildirimlerin tek ve ortak bir servis üzerinden yönetilmesini hedefler. Pil, hatırlatıcı ve gerekirse Todo uyarıları aynı kurallara uymalıdır.

## [ ] Görev 4.1 - Birleşik Bildirim Servisi

**Geliştirici Notu:** Modüllerin kendi içinde dağınık bildirim üretmesi yerine ortak servis davranışı kullanılmalıdır. Sessiz modda ses/TTS kapalı kalmalı, görsel uyarı gerekiyorsa korunmalıdır.

Amaç:
- [ ] Uyarı davranışını arayüze bağlı olmadan ortak bir servis üzerinden yönlendirmek.

Tamamlanma Kriterleri:
- [x] `bildirim_servisi.py` mevcut.
- [ ] Bildirim servisi davranışını birleştir.
- [ ] Pil uyarılarını ortak servisten geçir.
- [ ] Hatırlatıcı uyarılarını ortak servisten geçir.
- [ ] Yalnızca gerekirse Todo uyarılarını ortak servisten geçir.
- [ ] Kaynak bazlı bekleme/cooldown kuralları ekle.
- [ ] Sessiz moda uy: ses/TTS yok, görsel bildirim olabilir.

## [ ] Görev 4.2 - Bildirim Geçmişi ve Veri Sınırları

**Geliştirici Notu:** Bildirim geçmişi yalnızca ihtiyaç varsa eklenmelidir. Eklenirse sınırsız büyümemeli ve arayüz karmaşıklaşmamalıdır.

Tamamlanma Kriterleri:
- [ ] Gerekirse basit bildirim geçmişi modeli ekle.
- [ ] Bildirim geçmişini en fazla 500 kayıtla sınırla.
- [ ] Eski kayıtları başlangıçta ve yazma sonrası kırp.
- [ ] Arayüzü basit tut; analitik sistemi yapma.

---

# [ ] Faz 5 - Hatırlatıcı, Alarm, TTS

Bu faz hatırlatıcı sistemini v1 için kullanılabilir ve güvenilir hale getirir. TTS tamamen çevrimdışı olmalı, bulut/API bağımlılığı eklenmemelidir.

## [ ] Görev 5.1 - Hatırlatıcı Temeli

**Geliştirici Notu:** Temel hatırlatıcı modeli ve arayüzü mevcut. Bundan sonraki işler modeli genişletme, tetikleme güvenliği, snooze ve TTS üzerine kurulmalıdır.

Tamamlanma Kriterleri:
- [x] Hatırlatıcı modeli mevcut.
- [x] Hatırlatıcı JSON servisi mevcut.
- [x] Hatırlatıcı popup'ı mevcut.
- [x] Hatırlatıcı liste arayüzü mevcut.
- [x] Aktif/tamamlandı/kaçırıldı durumları mevcut.
- [x] Günlük/haftalık tekrar temeli mevcut.

## [ ] Görev 5.2 - Hatırlatıcı Veri Modeli Yükseltmesi

**Geliştirici Notu:** Yeni alanlar eski hatırlatıcı kayıtlarını bozmadan eklenmelidir. Bozuk kayıtlar uygulamayı çökertmeden güvenli şekilde atlanmalıdır.

Tamamlanma Kriterleri:
- [ ] Opsiyonel `voice_enabled` ekle.
- [ ] `voice_alerts` listesi ekle.
- [ ] `voice_repeat_rule` ekle.
- [ ] Çift uyarıyı önlemek için `notified_keys` ekle.
- [ ] Eski hatırlatıcılar varsayılanlarla yüklensin.
- [ ] Bozuk kayıtlar güvenli şekilde atlansın.

## [ ] Görev 5.3 - Hatırlatıcı Zaman Metni

**Geliştirici Notu:** Kullanıcıya okunacak veya gösterilecek kalan zaman metni doğal Türkçe olmalıdır. Geçmiş zaman ve zamanı geldi durumu ayrıca güvenli ele alınmalıdır.

Tamamlanma Kriterleri:
- [ ] Türkçe kalan zaman metni üret.
- [ ] Dakika/saat/gün metnini kapsa.
- [ ] `Zamanı geldi` durumunu kapsa.
- [ ] Geçmiş zamanı güvenli işle.

## [ ] Görev 5.4 - Hatırlatıcı Tetikleme ve Erteleme

**Geliştirici Notu:** Hatırlatıcılar tek seferlik akışta ve uygulama yeniden başlatıldığında güvenilir çalışmalıdır. Aynı uyarının iki kez tetiklenmesi engellenmelidir.

Tamamlanma Kriterleri:
- [ ] Tek seferlik hatırlatıcı akışını destekle.
- [ ] 5/10/60 dakika erteleme akışını destekle.
- [ ] Yeniden başlatma sonrası kaçırılmış hatırlatıcıyı işle.
- [ ] Tekrarlı uyarıların iki kez tetiklenmesini önle.

## [ ] Görev 5.5 - Hatırlatıcı Arayüz İyileştirme

**Geliştirici Notu:** Hatırlatıcı ekleme/düzenleme formu sade ama eksiksiz olmalıdır. Popup ana saat yüzeyini gereksiz yere gizlememelidir.

Tamamlanma Kriterleri:
- [ ] Ekle/düzenle formunu ayarları şişirmeden yenile.
- [ ] Okunacak metnin önizlemesini göster.
- [ ] Geçersiz giriş kurallarını uygula.
- [ ] Hatırlatıcı kartlarını ve durum renklerini iyileştir.
- [ ] Popup ana saat yüzeyini gereksiz yere gizlememeli.

## [ ] Görev 5.6 - Hatırlatıcı TTS

**Geliştirici Notu:** TTS çevrimdışı ve bloklamayan şekilde çalışmalıdır. Başarısız olursa uygulama sessizce çökmeden loglayarak devre dışı kalmalıdır.

Tamamlanma Kriterleri:
- [ ] Zaten yoksa çevrimdışı Windows/pyttsx3 TTS sarmalayıcısı ekle.
- [ ] Uygunsa erkek sesi tercih et.
- [ ] Sistem varsayılan sesine geri düş.
- [ ] TTS'i bloklamayan şekilde tut.
- [ ] TTS başarısız olursa sessizce devre dışı bırak/logla.
- [ ] Bulut/API TTS kullanma.

## [ ] Görev 5.7 - Temel Alarm

**Geliştirici Notu:** Alarm davranışı hatırlatıcıdan ayrı istenmedikçe v1 için ertelenmelidir. Eklenirse bildirim ve TTS kurallarını yeniden kullanmalıdır.

Durum:
- [ ] Kullanıcı açıkça hatırlatıcılardan ayrı alarm davranışı istemedikçe ertelendi.

Tamamlanma Kriterleri:
- [ ] Alarmın v1'de hatırlatıcıdan ayrı olup olmayacağını tanımla.
- [ ] Eklenirse tek seferlik ve basit günlük alarmı destekle.
- [ ] Pratikse etkinleştir/devre dışı bırak ve basit erteleme ekle.
- [ ] JSON'da yerel olarak sakla.
- [ ] Bildirim/TTS kurallarını yeniden kullan.

---

# [ ] Faz 6 - Todo Sistemi

Bu faz mevcut odak alanıdır. Amaç Todo modülünü profesyonel ama sade, Türkçe öncelikli ve yerel JSON uyumlu bir görev yöneticisine dönüştürmektir.

## [ ] Görev 6.1 - Todo Temeli

**Geliştirici Notu:** Temel Todo modeli, servisi ve arayüzü mevcut. Bundan sonraki işler mevcut çalışan yapıyı bozmadan model, workflow, filtre, tema ve resize tarafını tamamlamalıdır.

Tamamlanma Kriterleri:
- [x] Todo modeli mevcut.
- [x] Todo JSON servisi mevcut.
- [x] Todo arayüzü mevcut.
- [x] Dinamik öncelik temeli mevcut.
- [x] Görev kartı görsel yeniden tasarımı mevcut.
- [x] Yeni Görev dialogu mevcut.
- [x] Ortak tarih/saat düzenleyici mevcut.
- [x] Todo i18n pilot bağlantısı mevcut.

## [ ] Görev 6.2 - Todo Veri Modeli

**Geliştirici Notu:** Bu görev Todo için v1'de kullanılacak minimum ve kararlı veri modelini netleştirir. Eski JSON kayıtları bozulmadan yüklenmeli, gereksiz yeni alanlarla model şişirilmemelidir.

Uygulama Sırası:
- [ ] Önce mevcut Todo modeli, servisi ve arayüz alanlarını incele.
- [ ] Sonra yalnızca minimum v1 veri modeli alanlarını kesinleştir.

Tamamlanma Kriterleri:
- [x] Düzenlemeden önce mevcut alanları doğrula: başlık, açıklama, durum, öncelik, planlanan zaman, sıralama, tamamlanma/iptal zamanları.
- [x] Alt görevler/checklist'in v1 için ertelenip ertelenmeyeceğine karar ver.
- [x] Eski JSON uyumluluğunu koru.
- [x] JSON'u okunabilir ve kararlı tut.
- [x] Daha önce karar verilmiş silindi/iptal edildi durum davranışını yeniden açma.

## [ ] Görev 6.3 - Todo İş Akışı İyileştirme

**Geliştirici Notu:** Kullanıcı görevin aktif, gecikmiş, tamamlanmış, iptal edilmiş veya silinmiş olduğunu açıkça görebilmelidir. Erteleme ancak mevcut modele temiz oturuyorsa eklenmelidir.

Tamamlanma Kriterleri:
- [ ] Türkçe iş akışını iyileştir.
- [ ] Görev ekle/düzenle dialog davranışını destekle.
- [ ] Görev tarih ve saatini kaydet/yükle.
- [ ] Gecikmiş, tamamlanmış, iptal edilmiş ve silinmiş durumları net göster.
- [ ] Öncelik sıralaması ve tamamlananları temizleme davranışını kararlı tut.
- [ ] Yalnızca mevcut modele temiz uyuyorsa ertelemeyi destekle.

## [ ] Görev 6.4 - Todo Arayüz/Kullanıcı Deneyimi

**Geliştirici Notu:** Todo hızlı kullanılmalı, gri ve düz görünmemelidir. Filtreleme ve arama Türkçe karakterlerle güvenilir çalışmalıdır.

Tamamlanma Kriterleri:
- [ ] Kart tabanlı görsel dili koru.
- [ ] Hızlı görev girişini hızlı tut.
- [ ] Bugün, yarın, hafta, öncelik ve tamamlanan filtrelerini ekle/koru.
- [ ] Türkçe karakterlerle aramayı ekle/koru.
- [ ] Boş durumu kullanışlı tut.
- [ ] Panelin düz/gri görünmesini önle.

## [ ] Görev 6.5 - Todo Tema ve Yeniden Boyutlandırma

**Geliştirici Notu:** Todo içindeki renk ve boyut ayarları mümkün olduğunca Todo içinde kalmalıdır. Tema değişiklikleri anında uygulanmalı, okunabilirlik bozulursa güvenli fallback olmalıdır.

Tamamlanma Kriterleri:
- [ ] Pratik olduğunda mini panel tema kontrollerini Todo içinde tut.
- [ ] Panel/kart/metin/kenarlık/vurgu renklerini kaydet.
- [ ] Renkleri anında uygula.
- [ ] Kontrast koruması veya güvenli fallback ekle.
- [ ] Metin, checkbox, padding ve ikonlar için orantılı resize davranışını koru.

## [ ] Görev 6.6 - Todo Geçmiş Sınırları

**Geliştirici Notu:** Tamamlanmış görevler sınırsız büyürse JSON dosyası şişebilir. Ancak veri silme/kırpma görünür ve güvenli yapılmalıdır.

Tamamlanma Kriterleri:
- [ ] Tamamlanan Todo saklama kuralını tanımla.
- [ ] Yalnızca dosyalar çok büyüyebilecekse tamamlanan Todo geçmişini sınırla.
- [ ] Eski tamamlanan Todo'ları güvenli ve görünür şekilde kırp.

---

# [ ] Faz 7-10 ve v1'de Yapılmayacaklar

Bu bölüm, `MyTask.md` dosyasındaki Faz 7'den sonraki İngilizce görev yapısının Türkçe ve açıklamalı devamıdır.

Kaynak:
- [ ] `MyTask.md`
- [ ] Bu birleşik Türkçe dosya

Okuma notu:
- [ ] Faz 7-9 daha çok v1'i toparlama, ayarlar, tasarım, paketleme ve kalite kontrol tarafıdır.
- [ ] Faz 10 gelecek vizyonudur. v1 kararlı olmadan uygulanmamalıdır.

---

# [ ] Faz 7 - Ayarlar, Tasarım Sistemi, Çok Dil Temeli

Bu faz, uygulamanın ayarlar ekranını, görsel tutarlılığını ve çok dil altyapısını toparlar. Amaç v1 için Türkçe kullanımın net ve kararlı olmasıdır; İngilizce/Arapça tam cilalama v2'ye bırakılmıştır.

## [ ] Görev 7.1 - Ayarlar Penceresi

**Geliştirici Notu:** Ayarlar penceresi zaten mevcut. Bu görevde amaç yeni ve büyük bir ayar sistemi yazmak değil; Türkçe kullanım deneyimini, eksik/eski ayar anahtarlarını ve yeniden başlatma gerektiren durumları netleştirmektir.

Tamamlanma Kriterleri:
- [x] Ayarlar penceresi mevcut.
- [x] Dil sekmesi mevcut.
- [x] Saat font seçimi gömülü fontları destekliyor.
- [x] Görev önceliği ayarları mevcut.
- [ ] Türkçe ayarlar kullanıcı deneyimini gözden geçir.
- [ ] Dil değiştiğinde gerekiyorsa yeniden başlatma uyarısı ekle.
- [ ] Eksik/eski anahtar ve varsayılana sıfırlama akışlarını kararlı tut.
- [ ] Her ayarın yeniden başlatmadan sonra kalıcı olduğunu doğrula.

## [ ] Görev 7.2 - Tasarım Sistemi Birleştirme

**Geliştirici Notu:** Uygulama farklı ekranlarda farklı görsel diller kullanmamalıdır. Kartlar, butonlar, renkler, boşluklar ve okunabilirlik aynı aileden görünmelidir.

Tamamlanma Kriterleri:
- [ ] Paylaşılan bileşen stilini tutarlı tut.
- [ ] Düz ve gri duvar gibi görünen arayüzden kaçın.
- [ ] Kartları okunabilir ve kullanıcı dostu tut.
- [ ] Yeniden boyutlandırmayı orantılı tut.
- [ ] Erişilebilirlik ve kontrastı dikkate al.
- [ ] Kullanılan yerlerde hover ikonlarını ve tooltip'leri net tut.

## [ ] Görev 7.3 - i18n Temeli

**Geliştirici Notu:** i18n, uygulamanın ileride farklı dillere taşınabilmesi için altyapıdır. v1'de hedef Türkçe kararlılıktır; İngilizce ve Arapça metinleri mükemmelleştirme işi v2'ye bırakılmalıdır.

Tamamlanma Kriterleri:
- [x] `dil_yonetimi.py` mevcut.
- [x] `translations/tr.json`, `en.json`, `ar.json` mevcut.
- [x] `PanelSettings.language` mevcut.
- [x] Dil seçici mevcut.
- [x] Türkçe öncelikli v1 / v2 yerelleştirme kuralı mevcut.
- [ ] Yeni arayüz metinleri pratik olduğu yerde çeviri anahtarları kullansın.
- [ ] Todo arayüzünde kalan sabit metinleri denetle.
- [ ] v1'de İngilizce/Arapça cilalama yapma.
- [ ] v2: tam İngilizce geçişi.
- [ ] v2: tam Arapça/RTL geçişi.

## [ ] Görev 7.4 - Widget Bazlı Görünüm Ayarları

**Geliştirici Notu:** Saat, tarih ve pil bileşenleri için font, renk, kalınlık ve ölçek ayarları bozulmamalıdır. Canlı önizleme ancak mevcut ayar akışını kararsızlaştırmayacaksa eklenmelidir.

Tamamlanma Kriterleri:
- [ ] Saat/tarih/pil font kontrollerini kararlı tut.
- [ ] Varsa widget bazlı renk ve kalınlık ayarlarını kararlı tut.
- [ ] Her widget için ölçek sınırlarını koru.
- [ ] Ayar sistemini kararsızlaştırmayacaksa canlı önizleme ekle.

---

# [ ] Faz 8 - Varlıklar, Paketleme, Yayın

Bu faz, uygulamanın geliştirici ortamı dışında da düzgün çalışmasını hedefler. Fontlar, ikonlar, logo dosyaları ve EXE paketleme davranışı yayın öncesinde doğrulanmalıdır.

## [ ] Görev 8.1 - Varlıklar ve Fontlar

**Geliştirici Notu:** Kaynak modunda çalışan font ve ikon yolları paketlenmiş EXE içinde de çalışmalıdır. Kullanılmayan varlıklar ancak emin olunduktan sonra kaldırılmalıdır.

Tamamlanma Kriterleri:
- [x] Gömülü dijital fontlar mevcut.
- [x] Logo/ikon varlıkları mevcut.
- [x] Kum saati/gecikmiş görev ikonları mevcut.
- [x] Kaynak modunda varlık yolları çalışıyor.
- [ ] Yayın öncesi paketlenmiş varlık yollarını kararlı tut.
- [ ] Kullanılmayan varlıkları yalnızca incelemeden sonra kaldır.

## [ ] Görev 8.2 - Paketleme

**Geliştirici Notu:** Paketleme, uygulamayı son kullanıcıya geliştirici araçları olmadan çalıştırılabilir hale getirir. Bu aşamada ayar yolu, fontlar, ikonlar ve temiz kurulum davranışı özellikle kontrol edilmelidir.

Tamamlanma Kriterleri:
- [ ] Yayın build komutunu tanımla.
- [ ] EXE oluştur.
- [ ] EXE içinde ayar yolunu koru.
- [ ] EXE içinde varlıkları koru.
- [ ] Yayından önce temiz kurulum davranışını doğrula.
- [ ] Türkçe v1 yayın checklist'i hazırla.
- [ ] Release etiketi oluştur.

## [ ] Görev 8.3 - Windows Otomatik Başlatma

**Geliştirici Notu:** Windows ile otomatik başlatma opsiyonel bir v1 cilasıdır. Varsayılan olarak açık olmamalı; kullanıcı isterse etkinleşmelidir.

Durum:
- [ ] Opsiyonel v1 iyileştirmesi.

Tamamlanma Kriterleri:
- [ ] Windows otomatik başlatmanın v1'e dahil olup olmayacağına karar ver.
- [ ] Eklenirse registry/izin hatalarını güvenli şekilde ele al.
- [ ] Kullanıcı etkinleştirmedikçe ayarı kapalı tut.

---

# [ ] Faz 9 - Kod Sağlığı ve Doğrulama

Bu faz, uygulamanın çalışır kalmasını ve değişikliklerin kontrol edilmesini sağlar. Amaç ağır bir kalite sistemi kurmak değil; küçük ama güvenilir doğrulama alışkanlığı oluşturmaktır.

## [ ] Görev 9.1 - Hafif Kod Kontrol Politikası

**Geliştirici Notu:** Python dosyalarına dokunulduğunda en azından söz dizimi kontrolü yapılmalıdır. Davranış etkisi büyükse ilgili mevcut testler çalıştırılmalıdır.

Tamamlanma Kriterleri:
- [ ] Python kod düzenlemelerinde değiştirilen dosya için söz dizimi kontrolü çalıştır veya neden atlandığını açıkla.
- [ ] Davranış etkisi yüksek değişikliklerde ilgili mevcut testleri çalıştır.
- [ ] Her görev için ayrı checklist dosyası ekleme.

## [ ] Görev 9.2 - Temel Servis Testleri

**Geliştirici Notu:** Testler özellikle veri kaybı, yanlış tetikleme ve ayar bozulması gibi riskli alanları kapsamalıdır. Bu testler küçük ve doğrudan olmalıdır.

Tamamlanma Kriterleri:
- [ ] Ayarların varsayılanlarla yüklenmesini test et.
- [ ] Bozuk JSON kurtarmayı test et.
- [ ] Hatırlatıcı tetikleme mantığını test et.
- [ ] Bildirim cooldown davranışını test et.
- [ ] Todo sıralama/durum davranışını test et.
- [ ] Pil servis mantığına dokunulduğunda pil durum sınıflandırmasını test et.

## [ ] Görev 9.3 - Kod Sağlığı

**Geliştirici Notu:** Kod sağlığı, gereksiz büyük dosyaları ve UI içine kaçan iş mantığını engeller. Ancak bu görev uygulamayı tek seferde yeni klasör mimarisine taşıma anlamına gelmez.

Tamamlanma Kriterleri:
- [ ] Sebep yoksa yeni kaynak dosya 500 satırı geçmesin.
- [ ] Arayüz/iş mantığı sınırı net kalsın.
- [ ] Ölü kodu yalnızca gerçekten kullanılmadığı netse kaldır.
- [ ] Uygulamayı tek adımda `src/` mimarisine yeniden yazma.

## [ ] Görev 9.4 - Manuel Test Checklist'i

**Geliştirici Notu:** Yayın öncesinde kullanıcı gözüyle kontrol edilecek kısa bir liste gerekir. Bu liste pratik olmalı; çalıştırılamayacak kadar uzun olmamalıdır.

Tamamlanma Kriterleri:
- [ ] Yayından önce manuel checklist ekle veya güncelle.
- [ ] Başlangıç, sistem tepsisi, kapatınca tepsiye inme, saat, tarih, pil, ayarlar, hatırlatıcılar, Todo, TTS, JSON kurtarma ve paketlemeyi kapsa.
- [ ] Checklist'i gerçekten uygulanabilir tut.

## [ ] Görev 9.5 - CI ve Stil Kontrolleri

**Geliştirici Notu:** CI ve stil kontrolleri faydalıdır ama proje henüz küçük adımlarla ilerlerken ağır engellere dönüşmemelidir. Önce test komutları netleşmeli, sonra gerekiyorsa otomasyona bağlanmalıdır.

Durum:
- [ ] Opsiyonel geliştirici sağlığı çalışması.

Tamamlanma Kriterleri:
- [ ] Hafif test komutu dokümantasyonu ekle.
- [ ] Testler yeterince kararlı hale gelirse CI ekle.
- [ ] Küçük SPP/EKO görevlerini ağır araçlarla gereksiz yere engelleme.

---

# [ ] Faz 10 - Gelecek / v2+ Ertelenmiş Çalışmalar

Bu faz v1 için yapılacak işler değildir. Buradaki maddeler ürün büyüdüğünde yön kaybetmemek için tutulur. v1 kararlı olmadan bu maddeler uygulanmamalıdır.

## [ ] Görev 10.1 - Servis Kayıt Merkezi ve Olay Veriyolu

**Geliştirici Notu:** Bu mimari iyileştirme ancak mevcut doğrudan bağlantılar sorun üretmeye başladığında değerli olur. Amaç uygulamayı tek seferde baştan kurmak değildir.

Tamamlanma Kriterleri:
- [ ] Servis kayıt merkezi eklemenin ne zaman değerli olduğunu tanımla.
- [ ] Servisten arayüze olay sınırlarını tanımla.
- [ ] Yalnızca ilgili koda dokunurken kademeli taşıma yap.

## [ ] Görev 10.2 - Yedekleme Yöneticisi

**Geliştirici Notu:** JSON kurtarma ihtiyacı büyürse basit bir yerel yedekleme yöneticisi eklenebilir. Bulut veya senkronizasyon bu görevin konusu değildir.

Tamamlanma Kriterleri:
- [ ] JSON kurtarma ihtiyaç duyarsa basit yedekleme yöneticisi ekle.
- [ ] Yedeği yerel ve özel tut.
- [ ] Bu görevde senkronizasyon davranışı ekleme.

## [ ] Görev 10.3 - Akıllı Todo

**Geliştirici Notu:** Akıllı Todo, karmaşık proje yönetimi sistemi değildir. Sadece günlük kullanımda anlamlı basit görünümler eklenmelidir.

Tamamlanma Kriterleri:
- [ ] Bugün görünümü.
- [ ] Öncelik görünümü.
- [ ] Tamamlanan geçmişi görünümü.
- [ ] Karmaşık proje yönetimi sistemi yapma.

## [ ] Görev 10.4 - Temel İçgörüler

**Geliştirici Notu:** İçgörüler basit sayılardan ibaret olmalıdır. Pil analitiği veya ağır raporlama sistemi eklenmemelidir.

Tamamlanma Kriterleri:
- [ ] Tamamlanan görev sayısı.
- [ ] Kaçırılan hatırlatıcı sayısı.
- [ ] Aktif hatırlatıcı sayısı.
- [ ] Pil analitiğinden kaçın.

## [ ] Görev 10.5 - Hafif Otomasyon

**Geliştirici Notu:** Otomasyon özelliği eklenirse çok sınırlı tutulmalıdır. Script, zincirleme kural veya eklenti sistemi bu ürünün v1/v2 yakın hedefi değildir.

Tamamlanma Kriterleri:
- [ ] En fazla 10 basit JSON kuralı.
- [ ] Desteklenen tetikleyiciler yalnızca: pil seviyesi düştü, şarj çıkarıldı, zaman geldi.
- [ ] Desteklenen eylemler yalnızca: bildir, bildirimleri sustur, bildirim sıklığını azalt.
- [ ] Script, iç içe mantık, zincirleme veya eklenti sistemi yok.

## [ ] Görev 10.6 - Kısayollar ve Pano

**Geliştirici Notu:** Global kısayollar ve pano geçmişi kullanışlı olabilir ama opsiyonel kalmalıdır. Pano geçmişi eklenirse yerel, sınırlı ve kullanıcı isteğine bağlı olmalıdır.

Tamamlanma Kriterleri:
- [ ] Yeni Hatırlatıcı ve Arayüzü Göster/Gizle için global kısayol servisi.
- [ ] Eklenirse pano yöneticisi en fazla 100 kayıt tutsun.
- [ ] İkisini de opsiyonel ve hafif tut.
- [ ] Pano geçmişi kullanıcı isteğine bağlı ve yalnızca yerel olsun.

## [ ] Görev 10.7 - Opsiyonel Hesap ve Çoklu Masaüstü Senkronizasyonu

**Geliştirici Notu:** Bu uzun vadeli bir vizyondur. v1 yerel çalışmaya devam etmeli; hesap ve senkronizasyon daha sonra isteğe bağlı olmalıdır.

Durum:
- [ ] Yalnızca ertelenmiş gelecek vizyonu.

Amaç:
- [ ] Türkçe v1 kararlı olduktan sonra, aynı kullanıcının verilerine ve uyarılarına kendi masaüstü bilgisayarları arasında erişebilmesi için opsiyonel hesap tabanlı senkronizasyon eklemek.

Tamamlanma Kriterleri:
- [ ] Kimlik seçeneğine karar ver: e-posta magic link, OAuth, passkey, cihaz eşleştirme veya hibrit model.
- [ ] Kullanıcı, cihaz, oturum ve güvenilir cihaz modelini tanımla.
- [ ] Ayarlar, hatırlatıcılar, Todo ve bildirim durumu için şifreli senkronizasyon şeması tanımla.
- [ ] Çevrimdışı kuyruk ve arka plan senkronizasyon planı ekle.
- [ ] Birden fazla bilgisayardan gelen düzenlemeler için çakışma kuralları ekle.
- [ ] Hatırlatıcılar ve Todo için uzaktan uyarı yönlendirme ekle.
- [ ] Hesap kurtarma, dışa aktarma, silme ve gizlilik kontrolleri ekle.
- [ ] Senkronizasyon kararlı olana kadar opsiyonel ve varsayılan kapalı kalsın.

## [ ] Görev 10.8 - Android Mobil Eşlikçi

**Geliştirici Notu:** Mobil uygulama, masaüstü senkronizasyonu kararlı olmadan başlamamalıdır. Öncelik Android olabilir; iOS daha sonra düşünülmelidir.

Durum:
- [ ] Yalnızca ertelenmiş gelecek vizyonu.

Amaç:
- [ ] Masaüstü hesap/senkronizasyon kararlı olduktan sonra, cilalı arayüze sahip Android öncelikli mobil eşlikçi eklemek.

Tamamlanma Kriterleri:
- [ ] Android öncelikli ana ekran, hatırlatıcı, Todo ve uyarı ekranlarını tasarla.
- [ ] Masaüstü ile aynı hesap ve senkronizasyon API'sini kullan.
- [ ] Mümkün olduğunda yerel fallback ile push bildirimlerini destekle.
- [ ] Hızlı hatırlatıcı ekleme, hızlı Todo ekleme, erteleme, tamamlama ve kapatma akışlarını destekle.
- [ ] Mobil önbelleği çevrimdışı öncelikli tut.
- [ ] Masaüstü ve Android uyarı durumlarını tutarlı tut.
- [ ] iOS'u yalnızca Android çekirdeği kararlı olduktan sonra hazırla.

## [ ] Görev 10.9 - Global Sürüm Yayılımı

**Geliştirici Notu:** Global sürüm; dil, saat dilimi, bölge ve destek dokümantasyonu ister. Masaüstü senkronizasyonu ve Android akışı güvenilir olmadan global yayına gidilmemelidir.

Durum:
- [ ] Yalnızca ertelenmiş gelecek vizyonu.

Amaç:
- [ ] Global sürümlere ancak masaüstü senkronizasyonu ve Android eşlikçi güvenilir çalıştıktan sonra geçmek.

Tamamlanma Kriterleri:
- [ ] Türkçe v1 ve sync/mobile kilometre taşlarından sonra tam i18n akışını bitir.
- [ ] İngilizce arayüz/içerik geçişini tamamla.
- [ ] Hedefte kalırsa Arapça/RTL arayüz/içerik geçişini tamamla.
- [ ] Bölge, saat dilimi, tarih/saat ve bildirim yerel ayar kurallarını ekle.
- [ ] Genel gizlilik, veri işleme ve destek dokümantasyonunu hazırla.
- [ ] Ürün davranışı kararlı olduktan sonra global yayın varlıklarını hazırla.

## [ ] Görev 10.10 - Gelişmiş Widget Etkileşimi

**Geliştirici Notu:** Bu görev mevcut serbest yerleşim yetersiz kalırsa tekrar ele alınmalıdır. Yeni etkileşimler mevcut hover ve ölçekleme davranışını bozmamalıdır.

Tamamlanma Kriterleri:
- [ ] Mevcut serbest yerleşim yetersizse bireysel sürükle/bırak davranışını yeniden değerlendir.
- [ ] Mouse wheel ölçeklemeyi güvenli min/max sınırlarında tut.
- [ ] Hover eylem yönlendirmesini kararlı ve rahatsız etmeyecek şekilde tut.

---

# [ ] v1'de Ertelenen / Yapılmayacak İşler

Bu liste, v1'in kapsamını korumak içindir. Buradaki maddeler iyi fikir olabilir; ancak v1 kararlılığı tamamlanmadan yapılmamalıdır.

- [ ] SQLite geçişi yok.
- [ ] Eklenti sistemi yok.
- [ ] Bulut senkronizasyonu yok.
- [ ] Ücretli API veya ücretli servis yok.
- [ ] Dünya saati yok.
- [ ] Tam İngilizce/Arapça cilalama yok.
- [ ] Gelişmiş tema motoru yok.
- [ ] Uygulama genelinde büyük mimari yeniden yazım yok.
- [ ] Karmaşık tekrar/takvim motoru yok.
- [ ] Karmaşık otomasyon/script yok.
- [ ] Zorunlu hesap yok.
- [ ] Web arayüzü yok.
- [ ] QML/C++ yeniden yazımı yok.
