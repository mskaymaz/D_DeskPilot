# Reminder Data Model

## Amaç

Hatırlatma verisini açık, geriye uyumlu ve genişletilebilir bir JSON modelinde tutmak.

## Ana Hatırlatma Modeli

```json
{
  "id": "uuid",
  "title": "Doktor randevusu",
  "description": "Tahlil sonuçlarını götür",
  "due_at": "2026-06-30T14:00:00",
  "enabled": true,
  "completed": false,
  "completed_at": null,
  "voice_enabled": true,
  "voice_alerts": [],
  "voice_repeat_rule": null,
  "notified_keys": []
}
```

## Alanlar

| Alan | Tip | Açıklama |
|---|---|---|
| `id` | string | Benzersiz hatırlatma kimliği |
| `title` | string | Hatırlatma başlığı |
| `description` | string | Kullanıcının açıklama metni |
| `due_at` | string | ISO formatında ana zaman |
| `enabled` | bool | Hatırlatma aktif mi |
| `completed` | bool | Tamamlandı mı |
| `completed_at` | string/null | Tamamlanma zamanı |
| `voice_enabled` | bool | Sesli uyarı açık mı |
| `voice_alerts` | list | Ön uyarı listesi |
| `voice_repeat_rule` | object/null | Tekrarlı sesli uyarı kuralı |
| `notified_keys` | list | Tekrarlı bildirim engelleme kayıtları |

## Voice Alert Modeli

```json
{
  "amount": 20,
  "unit": "minute"
}
```

Geçerli unit değerleri:

- `minute`
- `hour`
- `day`

## Repeat Rule Modeli

```json
{
  "enabled": true,
  "start_amount": 1,
  "start_unit": "day",
  "interval_amount": 3,
  "interval_unit": "hour"
}
```

Anlamı:

```text
Ana zamandan 1 gün önce başla.
3 saatte bir sesli uyarı yap.
Ana zamana kadar devam et.
```

## Limitler

- `voice_alerts` en fazla 10 eleman içerebilir.
- Aynı `amount + unit` ikilisi tekrar eklenemez.
- `voice_repeat_rule` en fazla 1 adet olabilir.
- Negatif veya sıfır süre kabul edilmez.
- Ana zamandan sonra ön uyarı üretilmez.

## Geriye Uyumluluk

Eski kayıtlar okunurken eksik alanlar varsayılan değerlerle tamamlanır.

Varsayılanlar:

```json
{
  "enabled": true,
  "completed": false,
  "completed_at": null,
  "voice_enabled": false,
  "voice_alerts": [],
  "voice_repeat_rule": null,
  "notified_keys": []
}
```
