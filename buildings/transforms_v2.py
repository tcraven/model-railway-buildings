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


def apply_transform(
    workplane: Workplane,
    transform: Transform
) -> Workplane:

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


def apply_reverse_transform(
    workplane: Workplane,
    transform: Transform
) -> Workplane:

    transformed_workplane = workplane
    for tf in reversed(transform):
        if type(tf) is Translate:
            v = (-tf.vector[0], -tf.vector[1], -tf.vector[2])
            transformed_workplane = transformed_workplane.translate(v)

        elif type(tf) is Rotate:
            transformed_workplane = transformed_workplane.rotate(
                tf.startVector, tf.endVector, -tf.angle)
        else:
            raise Exception("Unknown transform operation")
    
    return transformed_workplane
