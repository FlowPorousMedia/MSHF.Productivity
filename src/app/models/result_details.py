from src.core.models.message_level import MessageLevel


class ResultDetails:
    def __init__(self):
        self.tp: MessageLevel = MessageLevel.INFO
        self.message: str = None
        self.title: str = None
