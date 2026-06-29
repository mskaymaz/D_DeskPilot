# Todo Data Model

## Ana Model

```json
{
  "id": "uuid",
  "title": "Kodları kontrol et",
  "description": "Release öncesi son gözden geçirme",
  "status": "pending",
  "priority": "high",
  "planned_for": "today",
  "due_date": null,
  "category": "İş",
  "tags": ["release", "kontrol"],
  "order": 10,
  "focus_today": true,
  "checklist": [],
  "created_at": "2026-06-29T15:00:00",
  "updated_at": "2026-06-29T15:00:00",
  "completed_at": null
}
```

## Alanlar

| Alan | Tip | Açıklama |
|---|---|---|
| `id` | string | Benzersiz görev kimliği |
| `title` | string | Görev başlığı |
| `description` | string | Açıklama |
| `status` | string | pending / in_progress / completed / cancelled |
| `priority` | string | low / normal / high / urgent |
| `planned_for` | string | today / tomorrow / this_week / someday / none |
| `due_date` | string/null | İsteğe bağlı tarih |
| `category` | string | Kategori |
| `tags` | list | Etiketler |
| `order` | number | Kullanıcı sıralaması |
| `focus_today` | bool | Bugünün odak listesinde mi |
| `checklist` | list | Alt görevler |
| `created_at` | string | Oluşturma zamanı |
| `updated_at` | string | Güncelleme zamanı |
| `completed_at` | string/null | Tamamlanma zamanı |

## Checklist Modeli

```json
{
  "id": "uuid",
  "title": "Testleri çalıştır",
  "completed": false,
  "order": 1
}
```

## Panel Tema Modeli

```json
{
  "theme_name": "Mavi Odak",
  "panel_bg": "#1e293b",
  "card_bg": "#334155",
  "text_color": "#f8fafc",
  "muted_text_color": "#cbd5e1",
  "border_color": "#475569",
  "accent_color": "#38bdf8",
  "corner_radius": 14,
  "panel_scale": 1.0
}
```

## Panel Boyut Modeli

```json
{
  "todo_panel_x": 100,
  "todo_panel_y": 100,
  "todo_panel_width": 380,
  "todo_panel_height": 560,
  "todo_panel_scale": 1.0
}
```

## Veri Kuralları

- Başlık boş olamaz.
- Öncelik boşsa `normal` olur.
- Durum boşsa `pending` olur.
- `order` yoksa liste sonuna eklenir.
- Eski kayıtlar varsayılan değerlerle tamamlanır.
- Unicode/Türkçe karakterler korunur.
