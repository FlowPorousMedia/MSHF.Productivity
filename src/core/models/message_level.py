from enum import Enum

from src.app.i18n import _


class MessageLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

    @property
    def label(self):
        labels = {
            MessageLevel.DEBUG: _("DEBUG"),
            MessageLevel.INFO: _("INFO"),
            MessageLevel.WARNING: _("WARNING"),
            MessageLevel.ERROR: _("ERROR"),
            MessageLevel.CRITICAL: _("CRITICAL"),
        }
        return labels[self]

    @property
    def color(self):
        """Bootstrap-цвет (для UI/иконок)"""
        colors = {
            MessageLevel.DEBUG: "#6c757d",
            MessageLevel.INFO: "#007bff",
            MessageLevel.WARNING: "#ff8800",
            MessageLevel.ERROR: "#dc0000",
            MessageLevel.CRITICAL: "#660000",
        }
        return colors[self]

    @property
    def icon(self):
        """Иконка FontAwesome"""
        icons = {
            MessageLevel.DEBUG: "fa-solid fa-terminal",
            MessageLevel.INFO: "fa-solid fa-circle-info",
            MessageLevel.WARNING: "fa-solid fa-triangle-exclamation",
            MessageLevel.ERROR: "fa-solid fa-circle-xmark",
            MessageLevel.CRITICAL: "fa-solid fa-skull-crossbones",
        }
        return icons[self]
