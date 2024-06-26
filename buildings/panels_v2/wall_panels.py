from cadquery import Workplane
from buildings import panels_v2
from buildings.media_v2 import Media
from buildings.panels_v2 import Cutout, Panel, PanelGroup
from buildings.panels_v2 import window_panels
from buildings.transforms_v2 import Transform, Translate, Rotate
from buildings.tabs import Tab, TabDirection


def basic_wall(
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


def wall(
    wall_base_media: Media,
    wall_front_media: Media,
    wall_back_media: Media,
    width: float,
    height: float,
    left_right_tab_direction: str,
    transform: Transform,
    name: str = "wall",
    tab_length_x: float = 30,
    tab_length_y: float = 30
) -> PanelGroup:
    if left_right_tab_direction == TabDirection.IN:
        base_wall_width = width - 2 * wall_front_media.thickness
    else:
        base_wall_width = width - 2 * (wall_front_media.thickness + wall_base_media.thickness)

    base_wall = Panel(
        name="base_wall",
        media=wall_base_media,
        workplane=panels_v2.rect(
            width=base_wall_width,
            height=height,
            thickness=wall_base_media.thickness,
            tab_left=Tab(
                direction=left_right_tab_direction,
                width=tab_length_y,
                height=wall_base_media.thickness,
                thickness=wall_base_media.thickness
            ),
            tab_right=Tab(
                direction=left_right_tab_direction,
                width=tab_length_y,
                height=wall_base_media.thickness,
                thickness=wall_base_media.thickness
            ),
            tab_bottom=Tab(
                direction=TabDirection.IN,
                width=tab_length_x,
                height=wall_base_media.thickness,
                thickness=wall_base_media.thickness
            ),
            tab_top=None
        )
    )
    if left_right_tab_direction == TabDirection.IN:
        inside_wall_width = base_wall_width - 2 * (wall_base_media.thickness + 0.25)
    else:
        inside_wall_width = base_wall_width - 2 * (wall_back_media.thickness + 0.25)

    inside_wall = Panel(
        name="inside_wall",
        media=wall_back_media,
        workplane=panels_v2.basic_rect(
            width=inside_wall_width,
            height=height - 2 * (wall_base_media.thickness + 0.25),
            thickness=wall_back_media.thickness
        ),
        transform=[Translate((0, 0, -wall_back_media.thickness))]
    )
    
    if left_right_tab_direction == TabDirection.IN:
        outside_wall_width = width
    else:
        outside_wall_width = width - 2 * wall_front_media.thickness

    outside_wall = Panel(
        name="outside_wall",
        media=wall_front_media,
        workplane=panels_v2.basic_rect(
            width=outside_wall_width,
            height=height,
            thickness=wall_front_media.thickness
        ),
        transform=[Translate((0, 0, wall_base_media.thickness))]
    )
    wall = PanelGroup(
        name=name,
        panels=[
            base_wall,
            outside_wall,
            inside_wall
        ],
        transform=transform
    )
    return wall


def gable_wall(
    wall_base_media: Media,
    wall_front_media: Media,
    wall_back_media: Media,
    roof_media: Media,
    roof_layer_count: int,
    width: float,
    height: float,
    gable_height: float,
    transform: Transform,
    name: str = "gable_wall",
    tab_length_x: float = 30,
    tab_length_y: float = 30,
    tab_length_roof: float = 20,
    tab_offset_roof: float = 5,
    roof_top_layer_no_tabs: bool = True
) -> PanelGroup:
    base_wall_width = width - 2 * wall_front_media.thickness
    gable_height_d = 2 * wall_front_media.thickness / width
    base_wall_gable_height = gable_height * (1 - gable_height_d)
    base_wall_height = height + gable_height * gable_height_d
    tab_offset = 0.5 * gable_height * gable_height_d
    if roof_top_layer_no_tabs:
        tab_top_height = (roof_layer_count - 1) * roof_media.thickness - 0.1
    else:
        tab_top_height = roof_layer_count * roof_media.thickness

    base_wall = Panel(
        name="base_wall",
        media=wall_base_media,
        workplane=panels_v2.gable_panel(
            width=base_wall_width,
            height=base_wall_height,
            gable_height=base_wall_gable_height,
            thickness=wall_base_media.thickness,
            tab_left=Tab(
                direction=TabDirection.IN,
                width=tab_length_y,
                height=wall_base_media.thickness,
                thickness=wall_base_media.thickness,
                offset=tab_offset
            ),
            tab_right=Tab(
                direction=TabDirection.IN,
                width=tab_length_y,
                height=wall_base_media.thickness,
                thickness=wall_base_media.thickness,
                offset=-tab_offset
            ),
            tab_bottom=Tab(
                direction=TabDirection.IN,
                width=tab_length_x,
                height=wall_base_media.thickness,
                thickness=wall_base_media.thickness
            ),
            tab_top_left=Tab(
                direction=TabDirection.OUT,
                width=tab_length_roof,
                offset=tab_offset_roof,
                height=tab_top_height,
                thickness=wall_base_media.thickness
            ),
            tab_top_right=Tab(
                direction=TabDirection.OUT,
                width=tab_length_roof,
                offset=-tab_offset_roof,
                height=tab_top_height,
                thickness=wall_base_media.thickness
            )
        ),
        transform=[Translate((
            0,
            0.5 * gable_height * gable_height_d,
            0
        ))]
    )

    inside_wall_width = base_wall_width - 2 * (wall_base_media.thickness + 0.25)

    inside_wall = Panel(
        name="inside_wall",
        media=wall_back_media,
        workplane=panels_v2.basic_rect(
            width=inside_wall_width,
            height=height - 2 * (wall_base_media.thickness + 0.25),
            thickness=wall_back_media.thickness
        ),
        transform=[Translate((0, 0, -wall_back_media.thickness))]
    )
    
    outside_wall_width = width

    outside_wall = Panel(
        name="outside_wall",
        media=wall_front_media,
        workplane=panels_v2.gable_panel(
            width=outside_wall_width,
            height=height,
            gable_height=gable_height,
            thickness=wall_front_media.thickness
        ),
        transform=[Translate((0, 0, wall_base_media.thickness))]
    )
    wall = PanelGroup(
        name=name,
        panels=[
            base_wall,
            outside_wall,
            inside_wall
        ],
        transform=transform
    )
    return wall


def bare_gable_wall(
    wall_base_media: Media,
    wall_front_media: Media,
    wall_back_media: Media,
    roof_media: Media,
    roof_layer_count: int,
    width: float,
    height: float,
    gable_height: float,
    transform: Transform,
    name: str = "gable_wall",
    tab_length_x: float = 30,
    tab_length_y: float = 30,
    tab_length_roof: float = 20,
    tab_offset_roof: float = 5,
    roof_top_layer_no_tabs: bool = True
) -> PanelGroup:
    base_wall_width = width - 2 * wall_front_media.thickness
    gable_height_d = 2 * wall_front_media.thickness / width
    base_wall_gable_height = gable_height * (1 - gable_height_d)
    base_wall_height = height + gable_height * gable_height_d
    tab_offset = 0.5 * gable_height * gable_height_d
    if roof_top_layer_no_tabs:
        tab_top_height = (roof_layer_count - 1) * roof_media.thickness - 0.1
    else:
        tab_top_height = roof_layer_count * roof_media.thickness

    base_wall = Panel(
        name="base_wall",
        media=wall_base_media,
        workplane=panels_v2.gable_panel(
            width=base_wall_width,
            height=base_wall_height,
            gable_height=base_wall_gable_height,
            thickness=wall_base_media.thickness,
            tab_left=Tab(
                direction=TabDirection.IN,
                width=tab_length_y,
                height=wall_base_media.thickness,
                thickness=wall_base_media.thickness,
                offset=tab_offset
            ),
            tab_right=Tab(
                direction=TabDirection.IN,
                width=tab_length_y,
                height=wall_base_media.thickness,
                thickness=wall_base_media.thickness,
                offset=-tab_offset
            ),
            tab_bottom=Tab(
                direction=TabDirection.IN,
                width=tab_length_x,
                height=wall_base_media.thickness,
                thickness=wall_base_media.thickness
            ),
            tab_top_left=Tab(
                direction=TabDirection.OUT,
                width=tab_length_roof,
                offset=tab_offset_roof,
                height=tab_top_height,
                thickness=wall_base_media.thickness
            ),
            tab_top_right=Tab(
                direction=TabDirection.OUT,
                width=tab_length_roof,
                offset=-tab_offset_roof,
                height=tab_top_height,
                thickness=wall_base_media.thickness
            )
        ),
        transform=[Translate((
            0,
            0.5 * gable_height * gable_height_d,
            0
        ))]
    )

    inside_wall_width = base_wall_width - 2 * (wall_base_media.thickness + 0.25)

    inside_wall = Panel(
        name="inside_wall",
        media=wall_back_media,
        workplane=panels_v2.basic_rect(
            width=inside_wall_width,
            height=height - 2 * (wall_base_media.thickness + 0.25),
            thickness=wall_back_media.thickness
        ),
        transform=[Translate((0, 0, -wall_back_media.thickness))]
    )

    wall = PanelGroup(
        name=name,
        panels=[base_wall, inside_wall],
        transform=transform
    )
    return wall


def chimney_hole(
    wall_media: Media,
    chimney_width: float,
    transform: Transform
) -> PanelGroup:
    hole_width = chimney_width + 2 * wall_media.thickness
    hole_height = 40
    return PanelGroup(
        name="chimney_hole",
        cutouts=[
            Cutout(
                transform=[
                    Translate((0, 0.5 * hole_height, 0))
                ],
                subtract_from=["base_wall", "inside_wall"],
                workplane=(
                    Workplane("XY")
                    .box(hole_width, hole_height, 100)
                )
            )
        ],
        transform=transform
    )


def connector_slots(
    base_media: Media,
    include_pins: bool,
    hole_spacing: float,
    pin_width: float,
    transform: Transform,
    pin_height: float = 10
) -> PanelGroup:
    
    hole_width = base_media.thickness
    hole_height = pin_width
    
    hole_wp = (
        Workplane("XY")
        .box(hole_width, hole_height, 100)
    )
    hole0 = Cutout(
        transform=[
            Translate((-0.5 * hole_spacing, 0, 0))
        ],
        subtract_from=["base_wall", "outside_wall"],
        # subtract_from=["base_wall", "outside_wall", "inside_wall"],
        workplane=hole_wp
    )
    hole1 = Cutout(
        transform=[
            Translate((0.5 * hole_spacing, 0, 0))
        ],
        subtract_from=["base_wall", "outside_wall"],
        # subtract_from=["base_wall", "outside_wall", "inside_wall"],
        workplane=hole_wp
    )

    panels = []
    if include_pins:
        pin0 = Panel(
            name="pin0",
            transform=[
                Rotate((0, 0, 0), (1, 0, 0), 90),
                Rotate((0, 0, 0), (0, 0, 1), 90),
                Translate((
                    -0.5 * hole_spacing - 0.5 * base_media.thickness,
                    0,
                    0.5 * pin_height
                ))
            ],
            media=base_media,
            workplane=panels_v2.basic_rect(
                width=pin_width,
                height=pin_height,
                thickness=base_media.thickness
            )
        )
        pin1 = Panel(
            name="pin1",
            transform=[
                Rotate((0, 0, 0), (1, 0, 0), 90),
                Rotate((0, 0, 0), (0, 0, 1), 90),
                Translate((
                    0.5 * hole_spacing - 0.5 * base_media.thickness,
                    0,
                    0.5 * pin_height
                ))
            ],
            media=base_media,
            workplane=panels_v2.basic_rect(
                width=pin_width,
                height=pin_height,
                thickness=base_media.thickness
            )
        )
        panels = [pin0, pin1]

    return PanelGroup(
        name="connector_slots",
        panels=panels,
        cutouts=[hole0, hole1],
        transform=transform
    )


def hole(
    hole_width: float,
    hole_height: float,
    transform: Transform,
) -> PanelGroup:        
    hole = Cutout(
        transform=[Translate((0, 0, -10))],
        subtract_from=["base_wall", "outside_wall", "inside_wall", "base_floor", "inside_floor"],
        workplane=(
            Workplane("XY")
            .box(hole_width, hole_height, 100)
        )
    )
    return PanelGroup(
        name="hole",
        cutouts=[hole],
        transform=transform
    )
