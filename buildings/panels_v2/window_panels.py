from cadquery import Workplane
from buildings.media_v2 import Media
from buildings.panels_v2 import Panel, PanelGroup, Cutout
from buildings.transforms_v2 import Transform, Translate, Rotate


WINDOW_MARGIN = 1


def window(
    base_media: Media,
    media: Media,
    transform: Transform,
    window_width: float,
    window_height: float,
    sill_width: float,
    sill_height: float

) -> PanelGroup:
    frame = Panel(
        name="frame",
        transform=[
            Translate((0, 0, base_media.thickness - media.thickness))
        ],
        media=media,
        workplane=window_frame(
            thickness=media.thickness,
            center_frame_thickness=0.75,
            window_width=window_width,
            window_height=window_height
        )
    )
    sill = Panel(
        name="sill",
        transform=[
            Translate((0, -0.5 * window_height - 0.5 * sill_height, base_media.thickness + 2 * media.thickness))
        ],
        media=media,
        workplane=window_sill(
            thickness=media.thickness,
            width=sill_width,
            height=sill_height
        )
    )
    base_back_hole = Cutout(
        transform=[
            Translate((0, 0, 0))
        ],
        subtract_from=["base_wall", "inside_wall"],
        workplane=window_hole_base(
            window_width=window_width,
            window_height=window_height
        )
    )
    front_hole = Cutout(
        transform=[
            Translate((0, 0, 0))
        ],
        subtract_from=["outside_wall"],
        workplane=window_hole_front(
            window_width=window_width,
            window_height=window_height
        )
    )
    return PanelGroup(
        name="window",
        panels=[frame, sill],
        cutouts=[base_back_hole, front_hole],
        transform=transform
    )


def window_sill(thickness: float, width: float, height: float) -> Workplane:
    # width = 14 + 3
    # height = 2
    return (
        Workplane("XY")
        .box(
            width,
            height,
            thickness)
        .translate((0, 0, 0.5 * thickness))
    )


def _window_hole(
    window_margin: float,
    window_width: float,
    window_height: float
) -> Workplane:
    hole_width = window_width + 2 * window_margin
    hole_height = window_height + 2 * window_margin
    return (
       Workplane("XY")
        .box(hole_width, hole_height, 100)
    )


def window_hole_base(window_width: float, window_height: float) -> Workplane:
    return _window_hole(
        window_width=window_width,
        window_height=window_height,
        window_margin=WINDOW_MARGIN)
    

def window_hole_front(window_width: float, window_height: float) -> Workplane:
    return _window_hole(
        window_width=window_width,
        window_height=window_height,
        window_margin=0)


def window_frame(
    thickness: float,
    center_frame_thickness: float,
    window_width: float,
    window_height: float
) -> Workplane:
    window_margin = WINDOW_MARGIN
    # window_width = 14
    # window_height = 23
    frame_thickness = 0.5

    panel = (
        Workplane("XY")
        .box(
            window_width + 2 * window_margin,
            window_height + 2 * window_margin,
            thickness)
        .translate((0, 0, 0.5 * thickness))
    )

    hole = (
        Workplane("XY")
        .box(
            window_width - 4 * frame_thickness,
            window_height - 6 * frame_thickness,
            10)
        .translate((0, 0, 0))
    )

    vertical_frame = (
        Workplane("XY")
        .box(
            center_frame_thickness,
            window_height - 4 * frame_thickness,
            thickness)
        .translate((
            0,
            0,
            0.5 * thickness))
    )
    horizontal_frame = (
        Workplane("XY")
        .box(
            window_width - 2 * frame_thickness,
            center_frame_thickness,
            thickness)
        .translate((
            0,
            0,
            0.5 * thickness))
    )

    window_panel = panel - hole + vertical_frame + horizontal_frame
    return window_panel
