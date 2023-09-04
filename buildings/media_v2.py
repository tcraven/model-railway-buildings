from dataclasses import dataclass
from typing import Union


@dataclass
class SingleLayerMedia:
    name: str
    description: str
    thickness: float
    width: float
    height: float


@dataclass
class LayeredMedia:
    description: str
    media: SingleLayerMedia
    layer_count: int
    thickness: float


Media = Union[SingleLayerMedia, LayeredMedia]


CARD_169mm = SingleLayerMedia(
    name="card-1.69mm",
    description="1.69mm corrugated card",
    thickness=1.69,
    width=265,
    height=165
)

CARD_056mm = SingleLayerMedia(
    name="card-0.56mm",
    description="0.56mm white card",
    thickness=0.56,
    width=265,
    height=165
)

CARD_2x169mm = LayeredMedia(
    description="Two layers of 1.69mm corrugated card",
    media=CARD_169mm,
    layer_count=2,
    thickness=2 * 1.69
)

CARD_2x056mm = LayeredMedia(
    description="Two layers of 0.56mm card",
    media=CARD_056mm,
    layer_count=2,
    thickness=2 * 0.56
)
