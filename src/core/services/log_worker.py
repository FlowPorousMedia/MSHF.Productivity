from datetime import datetime
from typing import Any, Dict

from src.core.models.logcategory import LogCategory
from src.core.models.message_level import MessageLevel


def make_log(
    message: str,
    level: MessageLevel = MessageLevel.INFO,
    category: LogCategory = LogCategory.SYSTEM,
    user_visible: bool = False,
) -> Dict[str, Any]:
    return {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "level": level,
        "category": category,
        "message": message,
        "user_visible": user_visible,
    }
