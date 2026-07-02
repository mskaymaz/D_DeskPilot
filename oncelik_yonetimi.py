from gorev_modeli import GorevOnceligi

DEFAULT_TASK_PRIORITIES = [
    {"key": "low", "name": "Düşük", "color": "#22c55e"},
    {"key": "normal", "name": "Normal", "color": "#3b82f6"},
    {"key": "high", "name": "Yüksek", "color": "#f97316"},
]


def priority_key(value):
    if isinstance(value, GorevOnceligi):
        return value.value
    return str(value or GorevOnceligi.NORMAL.value)


def task_priorities(settings):
    items = getattr(settings, "task_priorities", None) or DEFAULT_TASK_PRIORITIES
    return [p for p in items if isinstance(p, dict) and p.get("key")]


def priority_info(settings, value):
    key = priority_key(value)
    for item in task_priorities(settings):
        if item.get("key") == key:
            return item
    return next(p for p in DEFAULT_TASK_PRIORITIES if p["key"] == "normal")


def priority_name(settings, value):
    return priority_info(settings, value).get("name", "Normal")


def priority_color(settings, value):
    return priority_info(settings, value).get("color", "#3b82f6")


def default_task_priorities():
    return [dict(p) for p in DEFAULT_TASK_PRIORITIES]
