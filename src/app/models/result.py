from typing import Any

from src.app.models.result_details import ResultDetails


class Result:
    def __init__(self):
        self.success: bool = False
        self.data: Any = None
        self.details: ResultDetails = None
