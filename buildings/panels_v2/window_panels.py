from cadquery import Workplane
from buildings import panels_v2
from buildings.media_v2 import Media
from buildings.panels_v2 import Panel, PanelGroup, Cutout
from buildings.transforms_v2 import Transform, Translate, Rotate


def window(
    base_media: Media,
    media: Media,
    transform: Transform,
    window_width: float,
    window_height: float,
    sill_width: float,
    sill_height: float,
    window_margin: float = 1,
    no_vertical_frame: bool = False,
    top_arc_height: float = 0
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
            window_height=window_height,
            window_margin=window_margin,
            no_vertical_frame=no_vertical_frame
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
            window_height=window_height,
            window_margin=window_margin
        )
    )
    front_hole = Cutout(
        transform=[
            Translate((0, 0, 0))
        ],
        subtract_from=["outside_wall"],
        workplane=window_hole_front(
            window_width=window_width,
            window_height=window_height,
            top_arc_height=top_arc_height
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
    window_width: float,
    window_height: float,
    window_margin: float
) -> Workplane:
    hole_width = window_width + 2 * window_margin
    hole_height = window_height + 2 * window_margin
    return (
       Workplane("XY")
        .box(hole_width, hole_height, 100)
    )


def window_hole_base(
    window_width: float,
    window_height: float,
    window_margin: float
) -> Workplane:
    return _window_hole(
        window_width=window_width,
        window_height=window_height,
        window_margin=window_margin)
    

def window_hole_front(
    window_width: float,
    window_height: float,
    top_arc_height: float
) -> Workplane:
    hole_wp = _window_hole(
        window_width=window_width,
        window_height=window_height,
        window_margin=0)
    
    if top_arc_height > 0:
        hole_wp += (
            panels_v2.arc_panel(
                width=window_width,
                height=top_arc_height,
                thickness=100
            )
            .translate((0, 0.5 * window_height, 0))
        )
    
    return hole_wp


def window_frame(
    thickness: float,
    center_frame_thickness: float,
    window_width: float,
    window_height: float,
    window_margin: float,
    no_vertical_frame: bool
) -> Workplane:
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

    window_panel = panel - hole

    if not no_vertical_frame:
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
        window_panel += vertical_frame
    
    window_panel += horizontal_frame

    return window_panel


def arch_faux_window(
    base_media: Media,
    media: Media,
    transform: Transform,
    window_width: float,
    window_height: float,
    sill_width: float,
    sill_height: float,
    window_margin: float = 1
) -> PanelGroup:
    frame = Panel(
        name="frame",
        transform=[
            Translate((0, 0, base_media.thickness - media.thickness))
        ],
        media=media,
        workplane=panels_v2.basic_rect(
            width=window_width + 2 * window_margin,
            height=window_height + 2 * window_margin,
            thickness=media.thickness
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
            window_height=window_height,
            window_margin=window_margin
        )
    )
    front_hole = Cutout(
        transform=[
            Translate((0, 0, 0))
        ],
        subtract_from=["outside_wall"],
        workplane=panels_v2.arch(
            width=window_width,
            height=window_height,
            thickness=100
        )
    )
    return PanelGroup(
        name="window",
        panels=[frame, sill],
        cutouts=[base_back_hole, front_hole],
        transform=transform
    )
