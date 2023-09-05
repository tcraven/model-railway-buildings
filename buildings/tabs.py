from dataclasses import dataclass


class TabDirection:
    IN = "IN"
    OUT = "OUT"


@dataclass
class Tab:
    direction: str
    width: float
    height: float
    thickness: float
    offset: float = 0
