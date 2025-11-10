import gettext
from pathlib import Path

# src/app/i18n.py
LOCALE_DIR = Path(__file__).resolve().parent.parent / "translations"


def set_language(lang: str):
    global tr
    translation = gettext.translation(
        domain="messages",
        localedir=LOCALE_DIR,
        languages=[lang],
        fallback=True,
    )
    tr = translation.gettext


tr = gettext.gettext
