def make_response(
    logs=None,
    message=None,
    result=None,
    status_text=None,
    progress_value=0,
    progress_text="0%",
    progress_visible=False,
    state="idle",
):
    """
    Унифицированный ответ для колбеков расчёта.

    Аргументы:
        logs — список логов
        message — словарь message-request (или None)
        result — данные для solver-result-store (или None)
        status_text — текст для статусбара
        progress_value — число (0–100)
        progress_text — строка процента, например "10%"
        progress_visible — bool, отображать ли progress-wrapper
        state — новое состояние приложения ("idle", "running", "error" и т.д.)

    Возвращает:
        Кортеж значений в порядке:
        (log-store, message-request, solver-result-store,
         status-text, calculation-progress, progress-percent,
         progress-wrapper, app-state)
    """
    progress_style = (
        {"display": "flex", "flex": "1", "alignItems": "center", "marginLeft": "10px"}
        if progress_visible
        else {"display": "none"}
    )

    return (
        logs or [],
        message,
        result,
        status_text or "",
        progress_value,
        progress_text,
        progress_style,
        state,
    )
