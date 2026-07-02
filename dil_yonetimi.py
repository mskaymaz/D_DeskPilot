import json
from functools import lru_cache
from pathlib import Path

from utils import resource_path

SUPPORTED_LANGUAGES = ("tr", "en", "ar")
DEFAULT_LANGUAGE = "tr"
RTL_LANGUAGES = {"ar"}


def normalize_language(language):
    language = (language or DEFAULT_LANGUAGE).lower()
    return language if language in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE


@lru_cache(maxsize=None)
def _load(language):
    language = normalize_language(language)
    path = Path(resource_path(f"translations/{language}.json"))
    if not path.exists() and language != DEFAULT_LANGUAGE:
        path = Path(resource_path(f"translations/{DEFAULT_LANGUAGE}.json"))
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def t(key, language=None, fallback=None):
    language = normalize_language(language)
    data = _load(language)
    if key in data:
        return data[key]
    if language != DEFAULT_LANGUAGE:
        default_data = _load(DEFAULT_LANGUAGE)
        if key in default_data:
            return default_data[key]
    return fallback if fallback is not None else key


def is_rtl(language):
    return normalize_language(language) in RTL_LANGUAGES
