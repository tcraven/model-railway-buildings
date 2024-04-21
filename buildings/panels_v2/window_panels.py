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


def inner_frames(
    hole_width: float,
    hole_height: float,
    thickness: float,
    horizontal_panel_count: int,
    vertical_panel_count: int
) -> Workplane:
    center_frame_thickness = 0.75
    horiz_d = hole_width / horizontal_panel_count
    vert_d = hole_height / vertical_panel_count
    horiz_wp = panels_v2.basic_rect(
        width=hole_width,
        height=center_frame_thickness,
        thickness=thickness
    )
    vert_wp = panels_v2.basic_rect(
        width=center_frame_thickness,
        height=hole_height,
        thickness=thickness
    )

    wp = None
    for i in range(1, horizontal_panel_count):
        f_wp = vert_wp.translate((-0.5 * hole_width + i * horiz_d, 0, 0))
        if wp is None:
            wp = f_wp
        else:
            wp += f_wp
        
    for i in range(1, vertical_panel_count):
        f_wp = horiz_wp.translate((0, -0.5 * hole_height + i * vert_d, 0))
        if wp is None:
            wp = f_wp
        else:
            wp += f_wp

    return wp


def signal_box_front_window_set(
    base_media: Media,
    media: Media,
    transform: Transform,
    window_width: float,
    window_height: float,
    sill_width: float,
    sill_height: float,
    window_margin: float = 1,
    sill_offset: float = 0
) -> PanelGroup:
    
    # TO DO:
    # - Simplify by defining one side and using reflection for the other side?
    # - How to create left and right window sets?
    # - Perhaps repeat first then refactor?
    # - The left side includes the door and has a different number of panes?

    # Window shape parameters 1 1 1
    a = 0.75
    b = 0.75
    d = 1.25
    c = (window_width - 2 * d - 5 * a - 6 * b) / 14
    hole_height = window_height - 2 * a
    Cw = b + 3 * c
    Cx = 0.5 * (a + b + 3 * c)
    Dx = 1.5 * a + 2 * b + 5 * c
    Dw = 2 * b + 4 * c

    # Frame layer 0
    frame0_wp = panels_v2.basic_rect(
        width=window_width,
        height=window_height + 2 * window_margin,
        thickness=media.thickness
    )

    C_wp = panels_v2.basic_rect(
        width=Cw,
        height=hole_height,
        thickness=10
    )
    D_wp = panels_v2.basic_rect(
        width=Dw,
        height=hole_height,
        thickness=10
    )

    frame0_wp -= C_wp.translate((Cx, 0, -5))
    frame0_wp -= D_wp.translate((Dx, 0, -5))
    frame0_wp -= C_wp.translate((-Cx, 0, -5))
    frame0_wp -= D_wp.translate((-Dx, 0, -5))

    frame0 = Panel(
        name="frame",
        transform=[
            Translate((0, 0, base_media.thickness - media.thickness))
        ],
        media=media,
        workplane=frame0_wp
    )

    # Frame layer 1
    frame1_wp = panels_v2.basic_rect(
        width=window_width - 4 * media.thickness,
        height=window_height + 2 * window_margin,
        thickness=media.thickness
    )

    C1w = 3 * c
    hole1_height = window_height - 2 * a - 2 * b
    C1_wp = panels_v2.basic_rect(
        width=C1w,
        height=hole1_height,
        thickness=10
    )
    C1f_wp = inner_frames(
        hole_width=C1w,
        hole_height=hole1_height,
        thickness=media.thickness,
        horizontal_panel_count=3,
        vertical_panel_count=3
    )
    frame1_wp -= C1_wp.translate((Cx, 0, -5))
    frame1_wp += C1f_wp.translate((Cx, 0, 0))
    frame1_wp -= C1_wp.translate((-Cx, 0, -5))
    frame1_wp += C1f_wp.translate((-Cx, 0, 0))

    D1w = 2 * c
    D1_offset_x = 0.5 * b + c
    D1_wp = panels_v2.basic_rect(
        width=D1w,
        height=hole1_height,
        thickness=10
    )
    D1f_wp = inner_frames(
        hole_width=D1w,
        hole_height=hole1_height,
        thickness=media.thickness,
        horizontal_panel_count=2,
        vertical_panel_count=3
    )
    frame1_wp -= D1_wp.translate((Dx + D1_offset_x, 0, -5))
    frame1_wp += D1f_wp.translate((Dx + D1_offset_x, 0, 0))
    frame1_wp -= D1_wp.translate((Dx - D1_offset_x, 0, -5))
    frame1_wp += D1f_wp.translate((Dx - D1_offset_x, 0, 0))

    frame1_wp -= D1_wp.translate((-Dx + D1_offset_x, 0, -5))
    frame1_wp += D1f_wp.translate((-Dx + D1_offset_x, 0, 0))
    frame1_wp -= D1_wp.translate((-Dx - D1_offset_x, 0, -5))
    frame1_wp += D1f_wp.translate((-Dx - D1_offset_x, 0, 0))

    frame1 = Panel(
        name="frame",
        transform=[
            Translate((0, 0, base_media.thickness - 2 * media.thickness))
        ],
        media=media,
        workplane=frame1_wp
    )

    sill = Panel(
        name="sill",
        transform=[
            Translate((
                sill_offset,
                -0.5 * window_height - 0.5 * sill_height,
                base_media.thickness + media.thickness
            ))
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
            Translate((0, 0, -20))
        ],
        subtract_from=["base_wall", "inside_wall"],
        workplane=panels_v2.basic_rect(
            width=window_width + 2 * window_margin,
            height=window_height + 2 * window_margin,
            thickness=100
        )
    )
    front_hole = Cutout(
        transform=[
            Translate((0, 0, -20))
        ],
        subtract_from=["outside_wall"],
        workplane=panels_v2.basic_rect(
            width=window_width,
            height=window_height,
            thickness=100
        )
    )
    return PanelGroup(
        name="window",
        panels=[sill, frame0, frame1],
        cutouts=[base_back_hole, front_hole],
        transform=transform
    )



def signal_box_right_window_set(
    base_media: Media,
    media: Media,
    transform: Transform,
    front_window_width: float,
    window_height: float,
    # sill_width: float,
    sill_height: float,
    window_margin: float = 1,
    # sill_offset: float = 0
) -> PanelGroup:
    
    # TO DO:
    # - Simplify by defining one side and using reflection for the other side?
    # - How to create left and right window sets?
    # - Perhaps repeat first then refactor?
    # - The left side includes the door and has a different number of panes?
    # Window shape parameters 1 1 1
    a = 0.75
    b = 0.75
    d = 1.25

    window_width = 0.5 * front_window_width + 0.5 * a
    sill_width = window_width
    sill_offset = 0

    c = (front_window_width - 2 * d - 5 * a - 6 * b) / 14
    hole_height = window_height - 2 * a
    Cw = b + 3 * c
    Cx = 0.5 * (a + b + 3 * c) + 0.5 * a
    Dx = 1.5 * a + 2 * b + 5 * c + 0.5 * a
    Dw = 2 * b + 4 * c


    # Frame layer 0
    frame0_wp = (
        panels_v2.basic_rect(
            width=window_width,
            height=window_height + 2 * window_margin,
            thickness=media.thickness
        )
        .translate((0.5 * window_width, 0, 0))
    )
    

    C_wp = panels_v2.basic_rect(
        width=Cw,
        height=hole_height,
        thickness=10
    )
    D_wp = panels_v2.basic_rect(
        width=Dw,
        height=hole_height,
        thickness=10
    )

    frame0_wp -= C_wp.translate((Cx, 0, -5))
    frame0_wp -= D_wp.translate((Dx, 0, -5))
    # frame0_wp -= C_wp.translate((-Cx, 0, -5))
    # frame0_wp -= D_wp.translate((-Dx, 0, -5))

    frame0 = Panel(
        name="frame",
        transform=[
            Translate((
                0,
                0,
                base_media.thickness - media.thickness
            ))
        ],
        media=media,
        workplane=frame0_wp
    )

    # Frame layer 1
    frame1_wp = (
        panels_v2.basic_rect(
            width=window_width - 2 * media.thickness,
            height=window_height + 2 * window_margin,
            thickness=media.thickness
        )
        .translate((0.5 * window_width, 0, 0))
    )

    C1w = 3 * c
    hole1_height = window_height - 2 * a - 2 * b
    C1_wp = panels_v2.basic_rect(
        width=C1w,
        height=hole1_height,
        thickness=10
    )
    C1f_wp = inner_frames(
        hole_width=C1w,
        hole_height=hole1_height,
        thickness=media.thickness,
        horizontal_panel_count=3,
        vertical_panel_count=3
    )
    frame1_wp -= C1_wp.translate((Cx, 0, -5))
    frame1_wp += C1f_wp.translate((Cx, 0, 0))
    # frame1_wp -= C1_wp.translate((-Cx, 0, -5))
    # frame1_wp += C1f_wp.translate((-Cx, 0, 0))

    D1w = 2 * c
    D1_offset_x = 0.5 * b + c
    D1_wp = panels_v2.basic_rect(
        width=D1w,
        height=hole1_height,
        thickness=10
    )
    D1f_wp = inner_frames(
        hole_width=D1w,
        hole_height=hole1_height,
        thickness=media.thickness,
        horizontal_panel_count=2,
        vertical_panel_count=3
    )
    frame1_wp -= D1_wp.translate((Dx + D1_offset_x, 0, -5))
    frame1_wp += D1f_wp.translate((Dx + D1_offset_x, 0, 0))
    frame1_wp -= D1_wp.translate((Dx - D1_offset_x, 0, -5))
    frame1_wp += D1f_wp.translate((Dx - D1_offset_x, 0, 0))

    # frame1_wp -= D1_wp.translate((-Dx + D1_offset_x, 0, -5))
    # frame1_wp += D1f_wp.translate((-Dx + D1_offset_x, 0, 0))
    # frame1_wp -= D1_wp.translate((-Dx - D1_offset_x, 0, -5))
    # frame1_wp += D1f_wp.translate((-Dx - D1_offset_x, 0, 0))

    frame1 = Panel(
        name="frame",
        transform=[
            Translate((0, 0, base_media.thickness - 2 * media.thickness))
        ],
        media=media,
        workplane=frame1_wp
    )

    sill = Panel(
        name="sill",
        transform=[
            Translate((
                sill_offset + 0.5 * window_width,
                -0.5 * window_height - 0.5 * sill_height,
                base_media.thickness + media.thickness
            ))
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
            Translate((0.5 * window_width, 0, -20))
        ],
        subtract_from=["base_wall", "inside_wall"],
        workplane=panels_v2.basic_rect(
            width=window_width + 2 * window_margin,
            height=window_height + 2 * window_margin,
            thickness=100
        )
    )
    front_hole = Cutout(
        transform=[
            Translate((0.5 * window_width, 0, -20))
        ],
        subtract_from=["outside_wall"],
        workplane=panels_v2.basic_rect(
            width=window_width,
            height=window_height,
            thickness=100
        )
    )
    return PanelGroup(
        name="window",
        panels=[sill, frame0, frame1],
        cutouts=[base_back_hole, front_hole],
        transform=transform
    )
