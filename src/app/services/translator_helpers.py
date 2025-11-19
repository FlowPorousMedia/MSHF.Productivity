from functools import wraps
from src.app.i18n import set_language


def with_language(func):
    @wraps(func)
    def wrapper(language, *args, **kwargs):
        set_language(language)
        return func(language, *args, **kwargs)

    return wrapper
