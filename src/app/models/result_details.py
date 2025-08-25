from src.app.models.message_type import MessageType


class ResultDetails:
    def __init__(self):
        self.tp: MessageType = MessageType.INFO
        self.message: str = None
        self.title: str = None
