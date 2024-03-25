from cadquery import Workplane
from buildings import panels_v2
from buildings.media_v2 import Media
from buildings.panels_v2 import Panel, PanelGroup, Cutout
from buildings.transforms_v2 import Transform, Translate, Rotate


DOOR_MARGIN = 1


def door(
    base_media: Media,
    media: Media,
    transform: Transform,
    door_width: float,
    door_height: float,
    is_open: bool
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
    door = Panel(
        name="door",
        transform=[
            Translate((0, 0, base_media.thickness - 2 * media.thickness))
        ],
        media=media,
        workplane=panels_v2.basic_rect(
            width=door_width + 2 * DOOR_MARGIN,
            height=door_height + 2 * DOOR_MARGIN,
            thickness=media.thickness
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

    panels = [frame]

    if not is_open:
        panels.append(door)

    return PanelGroup(
        name="door",
        panels=panels,
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


def _shelter_layer_1(
    width,
    height,
    inner_width,
    inner_height,
    frame_thickness,
    door_width,
    window_height,
    thickness
) -> Workplane:
    
    door_height = height - frame_thickness
    door_x = -0.5 * width + frame_thickness + 0.5 * door_width
    door_y = -0.5 * frame_thickness
    bottom_width = width - door_width - 3 * frame_thickness
    bottom_height = height - window_height - 2 * frame_thickness
    bottom_x = 0.5 * width - frame_thickness - 0.5 * bottom_width
    bottom_y = -0.5 * height + 0.5 * bottom_height
    window_width = (width - door_width - 5 * frame_thickness) / 3
    window_y = 0.5 * height - frame_thickness - 0.5 * window_height
    
    wp0 = panels_v2.basic_rect(
        width=inner_width,
        height=inner_height,
        thickness=thickness
    )
    door_wp = (
        panels_v2.basic_rect(
            width=door_width,
            height=door_height,
            thickness=100
        )
        .translate((door_x, door_y, -10))
    )
    bottom_wp = (
        panels_v2.basic_rect(
            width=bottom_width,
            height=bottom_height,
            thickness=100
        )
        .translate((bottom_x, bottom_y, -10))
    )

    wp = wp0 - door_wp - bottom_wp

    window_wp = panels_v2.basic_rect(
        width=window_width,
        height=window_height,
        thickness=100
    )

    for i in range(3):
        window_x = (
            0.5 * width - frame_thickness - 0.5 * window_width
            - i * (window_width + frame_thickness)
        )
        wp -= window_wp.translate((window_x, window_y, -10))

    return wp


def _shelter_layer_2(
    width,
    height,
    inner_width,
    inner_height,
    frame_thickness,
    door_frame_thickness,
    window_frame_thickness,
    window_center_frame_thickness,
    door_width,
    window_height,
    thickness
) -> Workplane:
    
    door_height = height - frame_thickness
    door_x = -0.5 * width + frame_thickness + 0.5 * door_width
    door_y = -0.5 * frame_thickness
    door_hole_width = door_width - 2 * door_frame_thickness
    door_hole_height = door_height - door_frame_thickness
    door_hole_y = door_y - 0.5 * door_frame_thickness

    window_width = (width - door_width - 5 * frame_thickness) / 3
    window_y = 0.5 * height - frame_thickness - 0.5 * window_height
    
    wp0 = panels_v2.basic_rect(
        width=inner_width,
        height=inner_height,
        thickness=thickness
    )
    door_hole_wp = (
        panels_v2.basic_rect(
            width=door_hole_width,
            height=door_hole_height,
            thickness=100
        )
        .translate((door_x, door_hole_y, -10))
    )

    wp = wp0 - door_hole_wp

    window_hole_height = window_height - 2 * window_frame_thickness
    
    window_hole_wp = panels_v2.basic_rect(
        width=window_width - 2 * window_frame_thickness,
        height=window_hole_height,
        thickness=100
    )
    window_horizontal_frame_wp = panels_v2.basic_rect(
        width=window_width,
        height=window_center_frame_thickness,
        thickness=thickness
    )
    window_vertical_frame_wp = panels_v2.basic_rect(
        width=window_center_frame_thickness,
        height=window_height,
        thickness=thickness
    )

    for i in range(3):
        window_x = (
            0.5 * width - frame_thickness - 0.5 * window_width
            - i * (window_width + frame_thickness)
        )
        wp -= window_hole_wp.translate((window_x, window_y, -10))
        wp += window_horizontal_frame_wp.translate((window_x, window_y + window_hole_height / 6, 0))
        wp += window_vertical_frame_wp.translate((window_x, window_y, 0))

    return wp


def shelter_inset_door_windows(
    base_media: Media,
    media: Media,
    transform: Transform,
    width: float,
    height: float,
    base_cutout_margin: float = 2
) -> PanelGroup:
    
    inner_width = width + 2 * base_cutout_margin
    inner_height = height + 2 * base_cutout_margin
    door_width = 11
    frame_thickness = 1
    door_x = -0.5 * width + frame_thickness + 0.5 * door_width

    layer1 = Panel(
        name="layer1",
        transform=[
            Translate((0, 0, base_media.thickness - media.thickness))
        ],
        media=media,
        workplane=_shelter_layer_1(
            width=width,
            height=height,
            inner_width=inner_width,
            inner_height=inner_height,
            frame_thickness=frame_thickness,
            door_width=11,
            window_height=14,
            thickness=media.thickness
        )
    )

    layer2 = Panel(
        name="layer2",
        transform=[
            Translate((0, 0, base_media.thickness - 2 * media.thickness))
        ],
        media=media,
        workplane=_shelter_layer_2(
            width=width,
            height=height,
            inner_width=inner_width,
            inner_height=inner_height,
            frame_thickness=frame_thickness,
            door_frame_thickness=1,
            window_frame_thickness=1,
            window_center_frame_thickness=0.75,
            door_width=door_width,
            window_height=14,
            thickness=media.thickness
        )
    )

    door = Panel(
        name="door",
        transform=[
            Translate((door_x, 0, base_media.thickness - 3 * media.thickness))
        ],
        media=media,
        workplane=panels_v2.basic_rect(
            width=door_width,
            height=inner_height,
            thickness=media.thickness
        )
    )
    
    base_back_hole = Cutout(
        transform=[
            Translate((0, 0, -50))
        ],
        subtract_from=["base_wall", "inside_wall"],
        workplane=panels_v2.basic_rect(
            width=inner_width,
            height=inner_height,
            thickness=100
        )
    )
    front_hole = Cutout(
        transform=[
            Translate((0, 0, -50))
        ],
        subtract_from=["outside_wall"],
        workplane=panels_v2.basic_rect(
            width=width,
            height=height,
            thickness=100
        )
    )

    return PanelGroup(
        name="door_windows",
        panels=[layer1, layer2, door],
        cutouts=[base_back_hole, front_hole],
        transform=transform
    )
