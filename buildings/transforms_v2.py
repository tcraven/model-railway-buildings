from dataclasses import dataclass
from typing import Union
from cadquery import Workplane


Vector = tuple[float, float, float]


@dataclass
class Translate:
    vector: Vector


@dataclass
class Rotate:
    startVector: Vector
    endVector: Vector
    angle: float


Transform = list[Union[Translate, Rotate]]


def apply_transform(workplane: Workplane, transform: Transform) -> Workplane:
    transformed_workplane = workplane
    for tf in transform:
        if type(tf) is Translate:
            transformed_workplane = transformed_workplane.translate(tf.vector)

        elif type(tf) is Rotate:
            transformed_workplane = transformed_workplane.rotate(
                tf.startVector, tf.endVector, tf.angle)
        else:
            raise Exception("Unknown transform operation")
    
    return transformed_workplane
