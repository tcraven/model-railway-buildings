from cadquery import Workplane
from buildings.media_v2 import Media
from buildings.panels_v2 import Panel, PanelGroup, Cutout
from buildings.transforms_v2 import Transform, Translate, Rotate


DOOR_MARGIN = 1


def open_door(
    base_media: Media,
    media: Media,
    transform: Transform,
    door_width: float,
    door_height: float
) -> PanelGroup:
    frame = Panel(
        name="frame",
        transform=[
            Translate((0, 0, base_media.thickness - media.thickness))
        ],
        media=media,
        workplane=door_frame(
            thickness=media.thickness,
            center_frame_thickness=0.75,
            door_width=door_width,
            door_height=door_height
        )
    )
    base_back_hole = Cutout(
        transform=[
            Translate((0, 0, 0))
        ],
        subtract_from=["base_wall", "inside_wall"],
        workplane=door_hole_base(
            door_width=door_width,
            door_height=door_height
        )
    )
    front_hole = Cutout(
        transform=[
            Translate((0, 0, 0))
        ],
        subtract_from=["outside_wall"],
        workplane=door_hole_front(
            door_width=door_width,
            door_height=door_height
        )
    )
    return PanelGroup(
        name="door",
        panels=[frame],
        cutouts=[base_back_hole, front_hole],
        transform=transform
    )


def _door_hole(
    door_margin: float,
    door_width: float,
    door_height: float
) -> Workplane:
    hole_width = door_width + 2 * door_margin
    hole_height = door_height + 2 * door_margin
    return (
       Workplane("XY")
        .box(hole_width, hole_height, 100)
    )


def door_hole_base(door_width: float, door_height: float) -> Workplane:
    return _door_hole(
        door_width=door_width,
        door_height=door_height,
        door_margin=DOOR_MARGIN)
    

def door_hole_front(door_width: float, door_height: float) -> Workplane:
    return _door_hole(
        door_width=door_width,
        door_height=door_height,
        door_margin=0)


def door_frame(
    thickness: float,
    center_frame_thickness: float,
    door_width: float,
    door_height: float
) -> Workplane:
    door_margin = DOOR_MARGIN
    frame_thickness = 0.5

    panel = (
        Workplane("XY")
        .box(
            door_width + 2 * door_margin,
            door_height + 2 * door_margin,
            thickness)
        .translate((0, 0, 0.5 * thickness))
    )

    hole = (
        Workplane("XY")
        .box(
            door_width - 4 * frame_thickness,
            door_height - 2 * frame_thickness,
            10)
        .translate((
            0,
            -frame_thickness,
            0
        ))
    )

    # vertical_frame = (
    #     Workplane("XY")
    #     .box(
    #         center_frame_thickness,
    #         door_height - 4 * frame_thickness,
    #         thickness)
    #     .translate((
    #         0,
    #         0,
    #         0.5 * thickness))
    # )
    # horizontal_frame = (
    #     Workplane("XY")
    #     .box(
    #         door_width - 2 * frame_thickness,
    #         center_frame_thickness,
    #         thickness)
    #     .translate((
    #         0,
    #         0,
    #         0.5 * thickness))
    # )

    door_panel = panel - hole
    return door_panel
