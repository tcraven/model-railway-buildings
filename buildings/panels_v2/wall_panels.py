from buildings import panels_v2
from buildings.media_v2 import Media
from buildings.panels_v2 import Panel, PanelGroup
from buildings.transforms_v2 import Transform, Translate, Rotate


def wall(
    base_media: Media,
    front_media: Media,
    back_media: Media,
    transform: Transform
) -> PanelGroup:
    base = Panel(
        name="base_wall",
        media=base_media,
        workplane=panels_v2.basic_rect(
            width=90,
            height=50,
            thickness=base_media.thickness
        )
    )
    front = Panel(
        name="front_wall",
        media=front_media,
        workplane=panels_v2.basic_rect(
            width=90,
            height=50,
            thickness=front_media.thickness
        ),
        transform=[Translate((0, 0, base_media.thickness))]
    )
    back = Panel(
        name="back_wall",
        media=back_media,
        workplane=panels_v2.basic_rect(
            width=90,
            height=50,
            thickness=back_media.thickness
        ),
        transform=[Translate((0, 0, -back_media.thickness))]
    )
    return PanelGroup(
        name="wall",
        panels=[base, front, back],
        transform=transform
    )
