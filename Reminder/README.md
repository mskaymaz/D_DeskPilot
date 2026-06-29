# Reminder Module Documentation

Bu klasör, `D_DigitalSaat` uygulamasındaki Hatırlatma sisteminin geliştirme planını, mimarisini, görevlerini ve testlerini takip etmek için oluşturulmuştur.

## Dosyalar

| Dosya | Amaç |
|---|---|
| `REMINDER_ARCHITECTURE.md` | Hatırlatma sisteminin mimarisi |
| `REMINDER_TASKS.md` | Yapılacak işler ve ilerleme takibi |
| `REMINDER_DATA_MODEL.md` | Hatırlatma veri modeli |
| `REMINDER_TESTS.md` | Test senaryoları |
| `REMINDER_IDEAS.md` | Sonradan değerlendirilecek fikirler |
| `REMINDER_CHANGELOG.md` | Tamamlanan işler ve değişiklik geçmişi |

## Çalışma Kuralı

- Yeni fikirler önce `REMINDER_IDEAS.md` dosyasına eklenir.
- Onaylanan fikirler `REMINDER_TASKS.md` içine task olarak taşınır.
- Veri modelini etkileyen her karar `REMINDER_DATA_MODEL.md` içine yazılır.
- Tamamlanan işler `REMINDER_CHANGELOG.md` içine eklenir.
- Her kod değişikliğinden sonra `python -m py_compile .\*.py` kontrolü yapılır.
