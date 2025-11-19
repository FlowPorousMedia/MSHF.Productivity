import gettext
from pathlib import Path

LOCALE_DIR = (Path(__file__).resolve().parent.parent / "translations").resolve()

_current_lang = "en"  # язык по умолчанию

_translation = gettext.translation(
    domain="messages",
    localedir=LOCALE_DIR,
    languages=[_current_lang],
    fallback=True,
)


def set_language(lang: str):
    global _translation, _current_lang
    _current_lang = lang
    _translation = gettext.translation(
        domain="messages",
        localedir=LOCALE_DIR,
        languages=[lang],
        fallback=True,
    )


def get_current_language() -> str:
    """Возвращает код текущего языка"""
    return _current_lang


def _(text: str) -> str:
    return _translation.gettext(text)
