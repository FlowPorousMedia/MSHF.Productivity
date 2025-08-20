from typing import List


class ModelResultData:
    def __init__(self):
        self.name: str = None
        self.q_values: List[float] = None
        self.param1_values: List[float] = None
        self.param1_capt: str = None
        self.param2_values: List[float] = None
        self.param2_capt: str = None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "q_values": self.q_values,
            "param1_values": self.param1_values,
            "param1_capt": self.param1_capt,
            "param2_values": self.param2_values,
            "param2_capt": self.param2_capt,
        }
