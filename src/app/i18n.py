import gettext
from pathlib import Path

LOCALE_DIR = (Path(__file__).resolve().parent.parent / "translations").resolve()

_translation = gettext.translation(
    domain="messages",
    localedir=LOCALE_DIR,
    languages=["en"],  # язык по умолчанию
    fallback=True,
)


def set_language(lang: str):
    global _translation
    _translation = gettext.translation(
        domain="messages",
        localedir=LOCALE_DIR,
        languages=[lang],
        fallback=True,
    )


def _(text: str) -> str:
    return _translation.gettext(text)
