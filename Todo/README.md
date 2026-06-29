# Todo Module Documentation

Bu klasör, `D_DigitalSaat` uygulamasındaki To-do / Yapılacaklar sisteminin mimari, görsel, fonksiyonel ve test planını takip etmek için oluşturulmuştur.

## Ana Fikir

Hatırlatma sistemi ileri tarihli ve zamanı kritik olaylar içindir.

To-do sistemi ise daha yakın zamanlı, günlük/haftalık yapılacak işleri takip etmek içindir.

```text
Hatırlatma:
Zamanı gelince beni uyar.

To-do:
Yapılacak işlerimi düzenli ve güzel bir panelde takip et.
```

## Hedef

To-do paneli düz, gri, ruhsuz bir pencere olmayacak.

Hedef yapı:

- Estetik
- Sempatik
- Okunabilir
- Modern
- Hafif
- Hızlı
- Kişiselleştirilebilir
- Oranlı resize destekli
- Kod mimarisi sağlam
- 500 satır dosya sınırına uygun

## Dosyalar

| Dosya | Amaç |
|---|---|
| `TODO_ARCHITECTURE.md` | Sistem mimarisi |
| `TODO_UI_UX.md` | Görsel tasarım ve kullanıcı deneyimi |
| `TODO_DATA_MODEL.md` | Veri modeli |
| `TODO_TASKS.md` | Yapılacak işler |
| `TODO_TESTS.md` | Test planı |
| `TODO_IDEAS.md` | Sonradan değerlendirilecek fikirler |
| `TODO_CHANGELOG.md` | Tamamlanan işler |

## Genel Çalışma Kuralı

- Her task küçük ve kontrollü yapılır.
- Büyük dosyalar bölünür.
- 500 satır sınırı korunur.
- Unicode/Türkçe karakter bozulması kontrol edilir.
- UI sadece çalışır değil, estetik olmak zorundadır.
- Ayarlar penceresi şişirilmez.
- Panel içi hızlı tema/renk kontrolleri tercih edilir.
