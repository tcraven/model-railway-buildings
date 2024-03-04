from cadquery import Workplane
from buildings import panels_v2
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

    door_panel = panel - hole
    return door_panel


def front_door(
    base_media: Media,
    media: Media,
    transform: Transform,
    width: float,
    height: float,
    base_cutout_margin: float = 2
) -> PanelGroup:
    
    frame_width = width + 2 * base_cutout_margin
    frame_height = height + 2 * base_cutout_margin
    window_frame_thickness = 1.5
    inner_window_frame_thickness = 0.75
    window_radius = 0.5 * width - window_frame_thickness
    window_radius2 = 0.5 * window_radius + 0.5 * inner_window_frame_thickness
    window_radius3 = 0.5 * window_radius - 0.5 * inner_window_frame_thickness
    window_offset_y = 0.5 * (height - width)

    frame_wp0 = panels_v2.arch(
        width=frame_width,
        height=frame_height,
        thickness=media.thickness
    )

    frame_wp1 = (
        panels_v2.semicircle_panel(
            radius=window_radius,
            thickness=10
        )
        .translate((0, window_offset_y, -5))
    )

    frame_wp2 = (
        panels_v2.semicircle_panel(
            radius=window_radius2,
            thickness=media.thickness
        )
        .translate((0, window_offset_y, 0))
    )

    frame_wp3 = (
        panels_v2.semicircle_panel(
            radius=window_radius3,
            thickness=10
        )
        .translate((0, window_offset_y, -5))
    )

    spoke_length = 0.5 * window_radius + 0.5 * inner_window_frame_thickness
    spoke_offset_y = 0.75 * window_radius + 0.25 * inner_window_frame_thickness
    frame_wp4 = (
        panels_v2.basic_rect(
            width=inner_window_frame_thickness,
            height=spoke_length,
            thickness=media.thickness
        )
        .translate((0, spoke_offset_y, 0))
        .rotate((0, 0, 0), (0, 0, 1), 30)
        .translate((0, window_offset_y, 0))
    )
    frame_wp5 = (
        panels_v2.basic_rect(
            width=inner_window_frame_thickness,
            height=spoke_length,
            thickness=media.thickness
        )
        .translate((0, spoke_offset_y, 0))
        .rotate((0, 0, 0), (0, 0, 1), -30)
        .translate((0, window_offset_y, 0))
    )

    # Door opening
    door_frame_thickness = 1
    frame_wp6 = (
        panels_v2.basic_rect(
            width=width - 2 * door_frame_thickness,
            height=height - 0.5 * width - window_frame_thickness,
            thickness=10  # media.thickness
        )
        .translate((0, -0.25 * width - 0.5 * window_frame_thickness, -5))
    )

    frame_wp = (
        frame_wp0 - frame_wp1 + frame_wp2 - frame_wp3
        + frame_wp4 + frame_wp5
        - frame_wp6
    )

    frame = Panel(
        name="frame",
        transform=[
            Translate((0, 0, base_media.thickness - media.thickness))
        ],
        media=media,
        workplane=frame_wp
    )

    door_height = (
        height - 0.5 * width - window_frame_thickness + base_cutout_margin
        + 0.5 * window_frame_thickness
    )
    door_offset_y = (
        -0.25 * width - 0.5 * window_frame_thickness
        - 0.5 * base_cutout_margin + 0.25 * window_frame_thickness
    )
    door = Panel(
        name="door",
        transform=[
            Translate((0, 0, base_media.thickness - 2 * media.thickness))
        ],
        media=media,
        workplane=(
            panels_v2.basic_rect(
                width=frame_width,
                height=door_height,
                thickness=media.thickness
            )
            .translate((0, door_offset_y, 0))
        )
    )

    base_back_hole = Cutout(
        transform=[
            Translate((0, 0, -50))
        ],
        subtract_from=["base_wall", "inside_wall"],
        workplane=panels_v2.arch(
            width=frame_width,
            height=frame_height,
            thickness=100
        )
    )
    front_hole = Cutout(
        transform=[
            Translate((0, 0, -50))
        ],
        subtract_from=["outside_wall"],
        workplane=panels_v2.arch(
            width=width,
            height=height,
            thickness=100
        )
    )
    return PanelGroup(
        name="door",
        panels=[frame, door],
        cutouts=[base_back_hole, front_hole],
        transform=transform
    )
