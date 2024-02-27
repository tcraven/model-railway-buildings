import math
from cadquery import Workplane
from buildings import media_v2
from buildings import panels_v2
from buildings.media_v2 import Media
from buildings.panels_v2 import Panel, PanelGroup, Cutout
from buildings.panels_v2 import roof_panels, wall_panels, window_panels, houses, door_panels, chimneys
from buildings.transforms_v2 import Transform, Translate, Rotate
from buildings.tabs import Tab, TabDirection


def waiting_room_rafter_chimney_floor(
    base_media: Media,
    wall_media: Media,
    width: float,
    height: float,
    transform: Transform,
    name: str = "rafter_chimney_floor"
) -> PanelGroup:

    base_wp = panels_v2.rect(
        width=width,
        height=height,
        thickness=base_media.thickness,
        tab_left=Tab(
            direction=TabDirection.OUT,
            width=25,
            height=2 * base_media.thickness,
            thickness=base_media.thickness,
            offset=0
        ),
        tab_right=Tab(
            direction=TabDirection.OUT,
            width=25,
            height=2 * base_media.thickness,
            thickness=base_media.thickness,
            offset=0
        ),
        tab_bottom=None,
        tab_top=None
    )

    chimney_width = 8.44 + 2 * wall_media.thickness
    chimney_height = 11 + 2 * wall_media.thickness
    chimney_hole_width = chimney_width + 0.25
    chimney_hole_height = chimney_height + 0.25
    chimney_hole_offset_x = -3.5 - base_media.thickness + 0.5 * chimney_width

    chimney_hole_wp = panels_v2.basic_rect(
        width=chimney_hole_width,
        height=chimney_hole_height,
        thickness=20
    ).translate((chimney_hole_offset_x, 0, 0))

    base_wp0 = base_wp
    base_wp1 = base_wp - chimney_hole_wp

    base_wall0 = Panel(
        name="base_wall0",
        media=base_media,
        workplane=base_wp0,
        transform=[Translate((0, 0, 0))]
    )
    base_wall1 = Panel(
        name="base_wall1",
        media=base_media,
        workplane=base_wp1,
        transform=[Translate((0, 0, base_media.thickness))]
    )
    
    wall = PanelGroup(
        name=name,
        panels=[base_wall0, base_wall1],
        transform=transform
    )
    return wall


def waiting_room_gable_wall_with_chimney(
    base_media: Media,
    wall_media: Media,
    roof_media: Media,
    roof_layer_count: int,
    width: float,
    height: float,
    gable_height: float,
    transform: Transform,
    name: str = "gable_wall"
) -> PanelGroup:
    base_wall_width = width - 4 * wall_media.thickness
    gable_height_d = 4 * wall_media.thickness / width
    base_wall_gable_height = gable_height * (1 - gable_height_d)
    base_wall_height = height + gable_height * gable_height_d
    tab_offset = 0.5 * gable_height * gable_height_d

    base_wp0 = panels_v2.gable_panel(
        width=base_wall_width,
        height=base_wall_height,
        gable_height=base_wall_gable_height,
        thickness=base_media.thickness,
        tab_left=Tab(
            direction=TabDirection.IN,
            width=30,
            height=2 * base_media.thickness,
            thickness=base_media.thickness,
            offset=tab_offset
        ),
        tab_right=Tab(
            direction=TabDirection.IN,
            width=30,
            height=2 * base_media.thickness,
            thickness=base_media.thickness,
            offset=-tab_offset
        ),
        tab_bottom=None,
        tab_top_left=Tab(
            direction=TabDirection.OUT,
            width=20,
            offset=5,
            height=roof_layer_count * roof_media.thickness - 0.2,
            thickness=base_media.thickness
        ),
        tab_top_right=Tab(
            direction=TabDirection.OUT,
            width=20,
            offset=-5,
            height=roof_layer_count * roof_media.thickness - 0.2,
            thickness=base_media.thickness
        )
    )

    hole_offset_y = (
        15
        - 0.5 * base_wall_height
        - 0.5 * 2 * base_media.thickness
        - wall_media.thickness
    )
    hole_wp = panels_v2.basic_rect(
        width=30,
        height=2 * base_media.thickness,
        thickness=10
    ).translate((0, hole_offset_y, 0))

    base_wp = base_wp0 - hole_wp
    
    chimney_width = 9
    top_height = 7 * wall_media.thickness
    top_hole_width = 4
    HOLE_CLEARANCE = 0.025
    # core_base_layer_count=3,
    # core_wall_layer_count=0,
    shaft_height = 17  # 27
    shaft_base_height = 10  # 20
    core_width = chimney_width - 2 * wall_media.thickness
    chimney_z = 72
    
    base_chimney_wall_wp0 = panels_v2.rect(
        width=core_width,
        height=2 * shaft_height,
        thickness=base_media.thickness,
        tab_left=None,
        tab_right=None,
        tab_bottom=None,
        tab_top=Tab(
            direction=TabDirection.OUT,
            width=top_hole_width,
            height=top_height - 2 * HOLE_CLEARANCE,
            thickness=base_media.thickness
        )
    ).translate((
        0,
        chimney_z - 0.5 * base_wall_height,
        0
    ))

    base_wall0 = Panel(
        name="base_wall0",
        media=base_media,
        workplane=base_wp + base_chimney_wall_wp0,
        transform=[Translate((
            0,
            0.5 * gable_height * gable_height_d,
            0
        ))]
    )

    base_chimney_wall_wp1 = panels_v2.basic_rect(
        width=core_width,
        height=2 * shaft_height,
        thickness=base_media.thickness
    ).translate((
        0,
        chimney_z - 0.5 * base_wall_height,
        0
    ))

    base_wall1 = Panel(
        name="base_wall1",
        media=base_media,
        workplane=base_wp + base_chimney_wall_wp1,
        transform=[Translate((
            0,
            0.5 * gable_height * gable_height_d,
            base_media.thickness
        ))]
    )

    inside_wall_width = base_wall_width - 4 * base_media.thickness - 2
    inside_wall_height = height - 15 + wall_media.thickness - 4 * wall_media.thickness
    inside_wall_offset_y = 7.5 - 0.5 * wall_media.thickness

    inside_wall = Panel(
        name="inside_wall",
        media=wall_media,
        workplane=panels_v2.basic_rect(
            width=inside_wall_width,
            height=inside_wall_height,
            thickness=wall_media.thickness
        ),
        transform=[Translate((
            0,
            inside_wall_offset_y,
            -wall_media.thickness
        ))]
    )
    
    outside_wall_width = width

    outside_wall_wp = panels_v2.gable_panel(
        width=outside_wall_width,
        height=height,
        gable_height=gable_height,
        thickness=wall_media.thickness
    )
    outside_chimney_wall_wp0 = panels_v2.basic_rect(
        width=core_width,
        height=2 * shaft_height,
        thickness=wall_media.thickness
    ).translate((
        0,
        chimney_z - 0.5 * height,
        0
    ))
    outside_wall0 = Panel(
        name="outside_wall0",
        media=wall_media,
        workplane=outside_wall_wp + outside_chimney_wall_wp0,
        transform=[Translate((0, 0, 2 * base_media.thickness))]
    )

    outside_chimney_wall_wp1 = panels_v2.basic_rect(
        width=chimney_width,
        height=2 * shaft_base_height,
        thickness=wall_media.thickness
    ).translate((
        0,
        chimney_z - 0.5 * height,
        0
    ))
    outside_wall1 = Panel(
        name="outside_wall1",
        media=wall_media,
        workplane=outside_wall_wp + outside_chimney_wall_wp1,
        transform=[Translate((0, 0, 2 * base_media.thickness + wall_media.thickness))]
    )

    wall = PanelGroup(
        name=name,
        panels=[
            base_wall0,
            base_wall1,
            outside_wall0,
            outside_wall1,
            inside_wall
        ],
        transform=transform
    )
    return wall


def rafter_holes(
    wall_base_media: Media,
    transform: Transform
) -> PanelGroup:
    
    base_hole = Cutout(
        transform=[
            Translate((0, 0, 0))
        ],
        subtract_from=["base_wall"],
        workplane=(
            Workplane("XY")
            .box(
                wall_base_media.thickness,
                2 * wall_base_media.thickness,
                20
            )
        )
    )
    inside_hole = Cutout(
        transform=[
            Translate((0, 0, 0))
        ],
        subtract_from=["inside_wall"],
        workplane=(
            Workplane("XY")
            .box(
                wall_base_media.thickness + 2,
                4 * wall_base_media.thickness + 2,
                20
            )
        )
    )
    return PanelGroup(
        name="rafter_hole",
        panels=[],
        cutouts=[base_hole, inside_hole],
        transform=transform
    )


def waiting_room_rafter(
    wall_base_media: Media,
    wall_front_media: Media,
    roof_media: Media,
    roof_layer_count: int,
    width: float,
    gable_height: float,
    transform: Transform,
    name: str = "rafter"
) -> PanelGroup:
    height=wall_base_media.thickness
    base_wall_width = width - 2 * wall_front_media.thickness
    gable_height_d = 2 * wall_front_media.thickness / width
    base_wall_gable_height = gable_height * (1 - gable_height_d)
    base_wall_height = height + gable_height * gable_height_d
    bottom_tab_width = base_wall_width - 2 * wall_base_media.thickness
    height_d = gable_height * gable_height_d

    base_wp0 = panels_v2.gable_panel(
        width=base_wall_width,
        height=base_wall_height,
        gable_height=base_wall_gable_height,
        thickness=wall_base_media.thickness,
        tab_left=None,
        tab_right=None,
        tab_bottom=Tab(
            direction=TabDirection.OUT,
            width=bottom_tab_width,
            height=wall_base_media.thickness,
            thickness=wall_base_media.thickness,
            offset=0
        ),
        tab_top_left=Tab(
            direction=TabDirection.OUT,
            width=20,
            offset=5,
            height=roof_layer_count * roof_media.thickness - 0.2,
            thickness=wall_base_media.thickness
        ),
        tab_top_right=Tab(
            direction=TabDirection.OUT,
            width=20,
            offset=-5,
            height=roof_layer_count * roof_media.thickness - 0.2,
            thickness=wall_base_media.thickness
        )
    )

    # rafter z
    # height = 52
    # height - 0.5 * wall_base_media.thickness
    # chimney base z = 62
    # center of hole should be exactly chimney base z
    hole_wp = panels_v2.basic_rect(
        width=25,
        height=wall_base_media.thickness,
        thickness=20
    ).translate((
        0,
        10 + 0.5 * wall_base_media.thickness - 0.5 * height_d,
        -5
    ))

    base_wp = base_wp0 - hole_wp

    base_wall = Panel(
        name="base_wall",
        media=wall_base_media,
        workplane=base_wp,
        transform=[Translate((
            0,
            0.5 * gable_height * gable_height_d,
            0
        ))]
    )
    
    wall = PanelGroup(
        name=name,
        panels=[base_wall],
        transform=transform
    )
    return wall


def waiting_room_gable_wall(
    wall_base_media: Media,
    wall_front_media: Media,
    wall_back_media: Media,
    roof_media: Media,
    roof_layer_count: int,
    width: float,
    height: float,
    gable_height: float,
    transform: Transform,
    name: str = "gable_wall"
) -> PanelGroup:
    base_wall_width = width - 2 * wall_front_media.thickness
    gable_height_d = 2 * wall_front_media.thickness / width
    base_wall_gable_height = gable_height * (1 - gable_height_d)
    base_wall_height = height + gable_height * gable_height_d
    tab_offset = 0.5 * gable_height * gable_height_d

    base_wp0 = panels_v2.gable_panel(
        width=base_wall_width,
        height=base_wall_height,
        gable_height=base_wall_gable_height,
        thickness=wall_base_media.thickness,
        tab_left=Tab(
            direction=TabDirection.IN,
            width=30,
            height=wall_base_media.thickness,
            thickness=wall_base_media.thickness,
            offset=tab_offset
        ),
        tab_right=Tab(
            direction=TabDirection.IN,
            width=30,
            height=wall_base_media.thickness,
            thickness=wall_base_media.thickness,
            offset=-tab_offset
        ),
        tab_bottom=None,
        tab_top_left=Tab(
            direction=TabDirection.OUT,
            width=20,
            offset=5,
            height=roof_layer_count * roof_media.thickness - 0.2,
            thickness=wall_base_media.thickness
        ),
        tab_top_right=Tab(
            direction=TabDirection.OUT,
            width=20,
            offset=-5,
            height=roof_layer_count * roof_media.thickness - 0.2,
            thickness=wall_base_media.thickness
        )
    )

    hole_offset_y = (
        15
        - 0.5 * base_wall_height
        - 0.5 * wall_base_media.thickness
        - wall_back_media.thickness
    )
    hole_wp = panels_v2.basic_rect(
        width=30,
        height=wall_base_media.thickness,
        thickness=10
    ).translate((0, hole_offset_y, 0))

    base_wp = base_wp0 - hole_wp

    base_wall = Panel(
        name="base_wall",
        media=wall_base_media,
        workplane=base_wp,
        transform=[Translate((
            0,
            0.5 * gable_height * gable_height_d,
            0
        ))]
    )

    inside_wall_width = base_wall_width - 2 * wall_base_media.thickness - 2
    inside_wall_height = height - 15 + wall_back_media.thickness - 4 * wall_back_media.thickness
    inside_wall_offset_y = 7.5 - 0.5 * wall_back_media.thickness

    inside_wall = Panel(
        name="inside_wall",
        media=wall_back_media,
        workplane=panels_v2.basic_rect(
            width=inside_wall_width,
            height=inside_wall_height,
            thickness=wall_back_media.thickness
        ),
        transform=[Translate((
            0,
            inside_wall_offset_y,
            -wall_back_media.thickness
        ))]
    )
    
    outside_wall_width = width

    base_wall_gable_hyp = math.sqrt(
        base_wall_gable_height * base_wall_gable_height +
        0.25 * base_wall_width * base_wall_width
    )
    gable_hyp = math.sqrt(
        gable_height * gable_height +
        0.25 * width * width
    )
    outside_tab_offset = 5 - 0.5 * (gable_hyp - base_wall_gable_hyp)

    outside_wall = Panel(
        name="outside_wall",
        media=wall_front_media,
        workplane=panels_v2.gable_panel(
            width=outside_wall_width,
            height=height,
            gable_height=gable_height,
            thickness=wall_front_media.thickness,
            tab_top_left=Tab(
                direction=TabDirection.OUT,
                width=20,
                offset=outside_tab_offset,
                height=roof_layer_count * roof_media.thickness - 0.2,
                thickness=wall_front_media.thickness
            ),
            tab_top_right=Tab(
                direction=TabDirection.OUT,
                width=20,
                offset=-outside_tab_offset,
                height=roof_layer_count * roof_media.thickness - 0.2,
                thickness=wall_front_media.thickness
            )
        ),
        transform=[Translate((0, 0, wall_base_media.thickness))]
    )
    wall = PanelGroup(
        name=name,
        panels=[base_wall, outside_wall, inside_wall],
        transform=transform
    )
    return wall


def waiting_room_wall(
    wall_base_media: Media,
    wall_front_media: Media,
    wall_back_media: Media,
    width: float,
    height: float,
    transform: Transform,
    inside_wall_width_margin: float = 0,
    name: str = "wall"
) -> PanelGroup:
    
    base_wall_width = width - 2 * (wall_front_media.thickness + wall_base_media.thickness)

    base_wp0 = panels_v2.rect(
        width=base_wall_width,
        height=height,
        thickness=wall_base_media.thickness,
        tab_left=Tab(
            direction=TabDirection.OUT,
            width=30,
            height=wall_base_media.thickness,
            thickness=wall_base_media.thickness
        ),
        tab_right=Tab(
            direction=TabDirection.OUT,
            width=30,
            height=wall_base_media.thickness,
            thickness=wall_base_media.thickness
        ),
        tab_bottom=None,
        tab_top=None
    )
    floor_hole_wp = panels_v2.basic_rect(
        width=30,
        height=wall_base_media.thickness,
        thickness=10
    )

    floor_hole_offset_x = 40.25
    floor_hole_offset_y = (
        15 - 0.5 * height
        - 0.5 * wall_base_media.thickness - wall_back_media.thickness
    )
    floor_hole_wp0 = floor_hole_wp.translate((-floor_hole_offset_x, floor_hole_offset_y, 0))
    floor_hole_wp1 = floor_hole_wp.translate((floor_hole_offset_x, floor_hole_offset_y, 0))

    base_wp = base_wp0 - floor_hole_wp0 - floor_hole_wp1

    base_wall = Panel(
        name="base_wall",
        media=wall_base_media,
        workplane=base_wp
    )
    
    inside_wall_width = (
        base_wall_width - 2 * wall_back_media.thickness
        - inside_wall_width_margin
    )
    inside_wall_height = height - 15 + wall_back_media.thickness - 4 * wall_back_media.thickness
    # - wall_base_media.thickness
    inside_wall_offset_y = 7.5 - 0.5 * wall_back_media.thickness
    inside_wall = Panel(
        name="inside_wall",
        media=wall_back_media,
        workplane=panels_v2.basic_rect(
            width=inside_wall_width,
            height=inside_wall_height,
            thickness=wall_back_media.thickness
        ),
        transform=[Translate((
            0,
            inside_wall_offset_y,
            -wall_back_media.thickness
        ))]
    )
    
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
        panels=[base_wall, outside_wall, inside_wall],
        transform=transform
    )
    return wall


def waiting_room_floor(
    base_media: Media,
    wall_media: Media,
    width: float,
    height: float,
    transform: Transform
) -> PanelGroup:
    
    inner_width = width - 2 * (2 * wall_media.thickness + 2 * base_media.thickness)
    inner_height = height - 2 * (2 * wall_media.thickness + 2 * base_media.thickness)

    floor_wp_0 = panels_v2.rect(
        width=0.5 * inner_width,
        height=inner_height,
        thickness=base_media.thickness,
        tab_left=Tab(
            direction=TabDirection.OUT,
            width=30,
            height=1.75 * base_media.thickness,
            thickness=base_media.thickness
        ),
        tab_right=None,
        tab_bottom=Tab(
            direction=TabDirection.OUT,
            width=30,
            height=1.75 * base_media.thickness,
            thickness=base_media.thickness
        ),
        tab_top=Tab(
            direction=TabDirection.OUT,
            width=30,
            height=1.75 * base_media.thickness,
            thickness=base_media.thickness
        )
    )
    floor_wp_1 = panels_v2.rect(
        width=0.5 * inner_width,
        height=inner_height,
        thickness=base_media.thickness,
        tab_left=None,
        tab_right=Tab(
            direction=TabDirection.OUT,
            width=30,
            height=1.75 * base_media.thickness,
            thickness=base_media.thickness
        ),
        tab_bottom=Tab(
            direction=TabDirection.OUT,
            width=30,
            height=1.75 * base_media.thickness,
            thickness=base_media.thickness
        ),
        tab_top=Tab(
            direction=TabDirection.OUT,
            width=30,
            height=1.75 * base_media.thickness,
            thickness=base_media.thickness
        )
    )

    floor_wp = (
        floor_wp_0.translate((-0.25 * inner_width, 0, 0)) +
        floor_wp_1.translate((0.25 * inner_width, 0, 0))
    )

    floor_wp2 = panels_v2.basic_rect(
        width=inner_width - 2 * wall_media.thickness,
        height=inner_height - 2 * wall_media.thickness,
        thickness=wall_media.thickness
    )

    floor_p0 = Panel(
        name="base_floor_0",
        media=base_media,
        workplane=floor_wp,
        transform=[Translate((0, 0, 0))]
    )
    floor_p1 = Panel(
        name="base_floor_1",
        media=base_media,
        workplane=floor_wp,
        transform=[Translate((0, 0, base_media.thickness))]
    )
    floor_p2 = Panel(
        name="floor_0",
        media=wall_media,
        workplane=floor_wp2,
        transform=[Translate((0, 0, 2 * base_media.thickness))]
    )

    floor_pg = PanelGroup(
        name="floor",
        panels=[floor_p0, floor_p1, floor_p2],
        transform=transform
    )

    return floor_pg


def waiting_room(
    wall_base_media: Media,
    wall_front_media: Media,
    wall_back_media: Media,
    window_media: Media,
    roof_media: Media
) -> PanelGroup:

    length = 170
    width = 69
    height = 52
    gable_height = 22
    roof_overhang_left = 0
    roof_overhang_right = 5
    roof_overhang_width = 6
    roof_layer_count = 5

    wall_media = media_v2.CARD_056mm
    base_media = media_v2.CARD_169mm

    floor = waiting_room_floor(
        base_media=base_media,
        wall_media=wall_media,
        width=length,
        height=width,
        transform=[
            # Rotate((0, 0, 0), (1, 0, 0), 180),
            Translate((
                0,
                0,
                15 - 2 * base_media.thickness - wall_media.thickness - 0
            ))
        ]
    )

    front_wall = waiting_room_wall(
        name="front_wall",
        wall_base_media=wall_base_media,
        wall_front_media=wall_front_media,
        wall_back_media=wall_back_media,
        width=length,
        height=height,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), 90),
            Rotate((0, 0, 0), (0, 0, 1), 180),
            Translate((
                0,
                0.5 * width - wall_base_media.thickness - wall_front_media.thickness,
                0.5 * height
            ))
        ]
    )

    back_wall = waiting_room_wall(
        name="back_wall",
        wall_base_media=wall_base_media,
        wall_front_media=wall_front_media,
        wall_back_media=wall_back_media,
        width=length,
        height=height,
        inside_wall_width_margin=4,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), 90),
            Rotate((0, 0, 0), (0, 0, 1), 0),
            Translate((
                0,
                -0.5 * width + wall_base_media.thickness + wall_front_media.thickness,
                0.5 * height
            ))
        ]
    )

    right_wall = waiting_room_gable_wall_with_chimney(
        name="right_wall",
        base_media=base_media,
        wall_media=wall_media,
        roof_media=roof_media,
        roof_layer_count=roof_layer_count,
        width=width,
        height=height,
        gable_height=gable_height,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), 90),
            Rotate((0, 0, 0), (0, 0, 1), 90),
            Translate((
                0.5 * length - wall_base_media.thickness - wall_front_media.thickness,
                0,
                0.5 * height))
        ]
    )
    left_wall = waiting_room_gable_wall(
        name="left_wall",
        wall_base_media=wall_base_media,
        wall_front_media=wall_front_media,
        wall_back_media=wall_back_media,
        roof_media=roof_media,
        roof_layer_count=roof_layer_count,
        width=width,
        height=height,
        gable_height=gable_height,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), 90),
            Rotate((0, 0, 0), (0, 0, 1), -90),
            Translate((
                -0.5 * length + wall_base_media.thickness + wall_front_media.thickness,
                0,
                0.5 * height
            ))
        ]
    )

    rafter0 = waiting_room_rafter(
        name="rafter0",
        wall_base_media=wall_base_media,
        wall_front_media=wall_front_media,
        roof_media=roof_media,
        roof_layer_count=roof_layer_count,
        width=width,
        gable_height=gable_height,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), 90),
            Rotate((0, 0, 0), (0, 0, 1), 90),
            Translate((
                -35,
                0,
                height - 0.5 * wall_base_media.thickness
            ))
        ]
    )
    panels_v2.add_child_panel_group(
        parent=front_wall,
        child=rafter_holes(
            wall_base_media=wall_base_media,
            transform=[Translate((
                35 - 0.5 * wall_base_media.thickness,
                0.5 * height,
                0
            ))]
        )
    )
    panels_v2.add_child_panel_group(
        parent=back_wall,
        child=rafter_holes(
            wall_base_media=wall_base_media,
            transform=[Translate((
                -(35 - 0.5 * wall_base_media.thickness),
                0.5 * height,
                0
            ))]
        )
    )

    rafter1 = waiting_room_rafter(
        name="rafter1",
        wall_base_media=wall_base_media,
        wall_front_media=wall_front_media,
        roof_media=roof_media,
        roof_layer_count=roof_layer_count,
        width=width,
        gable_height=gable_height,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), 90),
            Rotate((0, 0, 0), (0, 0, 1), 90),
            Translate((
                15,
                0,
                height - 0.5 * wall_base_media.thickness
            ))
        ]
    )
    panels_v2.add_child_panel_group(
        parent=front_wall,
        child=rafter_holes(
            wall_base_media=wall_base_media,
            transform=[Translate((
                -(15 + 0.5 * wall_base_media.thickness),
                0.5 * height,
                0
            ))]
        )
    )
    panels_v2.add_child_panel_group(
        parent=back_wall,
        child=rafter_holes(
            wall_base_media=wall_base_media,
            transform=[Translate((
                15 + 0.5 * wall_base_media.thickness,
                0.5 * height,
                0
            ))]
        )
    )

    rafter_chimney_floor = waiting_room_rafter_chimney_floor(
        base_media=base_media,
        wall_media=wall_media,
        width=50 - wall_base_media.thickness,
        height=30,
        transform=[
            Translate((
                -10 + 0.5 * wall_base_media.thickness,
                0,
                62 - base_media.thickness
            ))
        ]
    )

    roof_angle = math.atan2(gable_height, 0.5 * width) * 180 / math.pi
    gable_length = math.sqrt(0.25 * width * width + gable_height * gable_height)
    roof_height = gable_length + roof_overhang_width
    chimney1_width = 8.44 + 2 * wall_media.thickness
    chimney1_height = 11 + 2 * wall_media.thickness
    chimney2_width = 6.19 + 2 * wall_media.thickness
    chimney2_height = 9 + 2 * wall_media.thickness
    roof_chimney_hole_gap_width = 0.5
    # The gap is set manually to provide enough clearance for the roof layers
    roof_chimney_hole_gap_height = 2.75

    roof_tab_holes = [
        # Left wall with no overhang and wider tabs (open hole at edge
        # of roof)
        {
            "offset_x": -0.5 * length,
            "width": 2 * (wall_base_media.thickness + wall_front_media.thickness)
        },
        # Rafter 0
        {
            "offset_x": -35 + 0.5 * wall_base_media.thickness,
            "width": wall_base_media.thickness
        },
        # Rafter 1
        {
            "offset_x": 15 + 0.5 * wall_base_media.thickness,
            "width": wall_base_media.thickness
        },
        # Right wall
        {
            "offset_x": 0.5 * length - wall_front_media.thickness - 0.5 * wall_base_media.thickness,
            "width": wall_base_media.thickness
        }
    ]
    roof_chimney_holes = [
        # Chimney 1
        {
            "offset_x": -13.5 + 0.5 * chimney1_width,
            "width": chimney1_width + roof_chimney_hole_gap_width,
            "height": chimney1_height + roof_chimney_hole_gap_height
        },
        # Chimney 2
        {
            "offset_x": 85 - 0.5 * chimney2_width,
            "width": chimney2_width + roof_chimney_hole_gap_width,
            "height": chimney2_height + roof_chimney_hole_gap_height
        }
    ]

    back_roof = roof_panels.roof_panel(
        name="back_roof",
        roof_media=roof_media,
        wall_base_media=wall_base_media,
        wall_front_media=wall_front_media,
        house_length=length,
        house_width=width,
        gable_height=gable_height,
        overhang_left=roof_overhang_left,
        overhang_right=roof_overhang_right,
        overhang_width=roof_overhang_width,
        layer_count=roof_layer_count,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), roof_angle),
            Translate((
                0,
                -0.5 * roof_height * math.cos(math.radians(roof_angle)),
                height + gable_height - 0.5 * roof_height * math.sin(math.radians(roof_angle))
            ))
        ],
        tab_holes=roof_tab_holes,
        chimney_holes=roof_chimney_holes,
        reverse_hole_offsets=False
    )

    front_roof = roof_panels.roof_panel(
        name="front_roof",
        roof_media=roof_media,
        wall_base_media=wall_base_media,
        wall_front_media=wall_front_media,
        house_length=length,
        house_width=width,
        gable_height=gable_height,
        overhang_left=roof_overhang_right,
        overhang_right=roof_overhang_left,
        overhang_width=roof_overhang_width,
        layer_count=roof_layer_count,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), roof_angle),
            Rotate((0, 0, 0), (0, 0, 1), 180),
            Translate((
                0,
                0.5 * roof_height * math.cos(math.radians(roof_angle)),
                height + gable_height - 0.5 * roof_height * math.sin(math.radians(roof_angle))
            ))
        ],
        tab_holes=roof_tab_holes,
        chimney_holes=roof_chimney_holes,
        reverse_hole_offsets=True
    )

    center_chimney_height = 27
    chimney1 = chimneys.chimney(
        base_media=media_v2.CARD_169mm,
        wall_media=media_v2.CARD_056mm,
        chimney_width=11,
        core_base_layer_count=4,
        core_wall_layer_count=1,
        shaft_height=center_chimney_height,  # 27
        shaft_base_height=center_chimney_height - 7,  # 20
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), 90),
            Rotate((0, 0, 0), (0, 0, 1), 90),
            # Translate((-13.5, 0, 62))
            Translate((
                -13.5,
                0,
                62  # 15 - base_media.thickness - wall_media.thickness
            ))
        ]
    )

    chimney2 = chimneys.chimney_for_gable_wall(
        base_media=media_v2.CARD_169mm,
        wall_media=media_v2.CARD_056mm,
        chimney_width=9,
        core_base_layer_count=3,
        core_wall_layer_count=0,
        shaft_height=17,  # 27
        shaft_base_height=10,  # 20
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), 90),
            Rotate((0, 0, 0), (0, 0, 1), -90),
            Translate((
                85,  # - 4 * media_v2.CARD_056mm.thickness - 3 * media_v2.CARD_169mm.thickness,
                0,
                72  # 62
            ))  # 77.5
        ]
    )
    
    house = PanelGroup(
        name="house",
        children=[
            floor,
            front_wall,
            back_wall,
            right_wall,
            left_wall,
            rafter0, rafter1, rafter_chimney_floor,
            back_roof,
            front_roof,
            chimney1,
            chimney2
        ]
    )


    # back_wall = panels_v2.get_child_panel_group(
    #     panel_group=house,
    #     name="back_wall"
    # )

    # Waiting room window 1
    panels_v2.add_child_panel_group(
        parent=back_wall,
        child=window_panels.window(
            base_media=wall_base_media,
            media=window_media,
            window_width=11,
            window_height=22,
            sill_width=11 + 3,
            sill_height=2,
            transform=[Translate((-46.5, 8.5, 0))]
        )
    )
    # Waiting room window 2
    panels_v2.add_child_panel_group(
        parent=back_wall,
        child=window_panels.window(
            base_media=wall_base_media,
            media=window_media,
            window_width=11,
            window_height=22,
            sill_width=11 + 3,
            sill_height=2,
            transform=[Translate((-19.5, 8.5, 0))]
        )
    )
    # Waiting room window 3
    panels_v2.add_child_panel_group(
        parent=back_wall,
        child=window_panels.window(
            base_media=wall_base_media,
            media=window_media,
            window_width=11,
            window_height=22,
            sill_width=11 + 3,
            sill_height=2,
            transform=[Translate((28.5, 8.5, 0))]
        )
    )
    # Waiting room window 4
    panels_v2.add_child_panel_group(
        parent=back_wall,
        child=window_panels.window(
            base_media=wall_base_media,
            media=window_media,
            window_width=11,
            window_height=22,
            sill_width=11 + 3,
            sill_height=2,
            transform=[Translate((49.5, 8.5, 0))]
        )
    )

    # Waiting room door 1
    panels_v2.add_child_panel_group(
        parent=back_wall,
        child=door_panels.open_door(
            base_media=wall_base_media,
            media=window_media,
            door_width=13,
            door_height=30.5,
            transform=[Translate((-72, 4.25, 0))]
        )
    )
    # Waiting room door 2
    panels_v2.add_child_panel_group(
        parent=back_wall,
        child=door_panels.open_door(
            base_media=wall_base_media,
            media=window_media,
            door_width=13,
            door_height=30.5,
            transform=[Translate((5, 4.25, 0))]
        )
    )
    # Waiting room door 3
    panels_v2.add_child_panel_group(
        parent=back_wall,
        child=door_panels.open_door(
            base_media=wall_base_media,
            media=window_media,
            door_width=13,
            door_height=30.5,
            transform=[Translate((72.5, 4.25, 0))]
        )
    )

    return house
