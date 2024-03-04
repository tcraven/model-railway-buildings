import math
from cadquery import Workplane
from buildings import panels_v2
from buildings.media_v2 import Media
from buildings.panels_v2 import Cutout, Panel, PanelGroup
from buildings.tabs import Tab, TabDirection
from buildings.transforms_v2 import Transform, Translate, Rotate


def roof_panel(
    roof_media: Media,
    wall_front_media: Media,
    wall_base_media: Media,
    house_length: float,
    house_width: float,
    gable_height: float,
    overhang_left: float,
    overhang_right: float,
    overhang_width: float,
    layer_count: int,
    transform: Transform,
    tab_holes: list[dict],
    chimney_holes: list[dict],
    reverse_hole_offsets: bool,
    name: str = "roof",
    end_taper: bool = True,
    top_layer_no_tabs: bool = True
) -> PanelGroup:

    tan_a = 2 * gable_height / house_width
    gable_length = math.sqrt(0.25 * house_width * house_width + gable_height * gable_height)
    # roof_width = house_length + 2 * overhang_length
    roof_width = house_length + overhang_left + overhang_right
    roof_height = gable_length + overhang_width
    roof_angle = math.atan2(gable_height, 0.5 * house_width) * 180 / math.pi
    tab_d = 0.5 * wall_front_media.thickness / math.cos(math.radians(roof_angle))
    roof_offset_x = 0.5 * (overhang_right - overhang_left)
    roof_overhang_d = 0.75 * wall_front_media.thickness / math.sin(math.radians(roof_angle))
    offset_c = -1 if reverse_hole_offsets else 1

    panels = []
    for i in range(layer_count):
        if end_taper and layer_count - i > 3:
            dh = roof_overhang_d * (layer_count - i - 3)
            height = roof_height - dh
            offset_y = 0.5 * dh
        else:
            height = roof_height
            offset_y = 0

        roof_wp0 = panels_v2.basic_rect(
            width=roof_width,
            height=height,
            thickness=roof_media.thickness
        )
        roof_wp = roof_wp0
        for chimney_hole in chimney_holes:
            hole_wp = panels_v2.basic_rect(
                width=chimney_hole["width"],
                height=chimney_hole["height"],
                thickness=20
            ).translate((
                offset_c * chimney_hole["offset_x"] - roof_offset_x,
                0.5 * roof_height - offset_y,
                -5
            ))
            roof_wp = roof_wp - hole_wp

        panels.append(Panel(
            name=f"p{i}",
            media=roof_media,
            workplane=roof_wp,
            transform=[
                Translate((
                    roof_offset_x,
                    i * roof_media.thickness * tan_a + offset_y,
                    i * roof_media.thickness
                ))
            ]
        ))

    roof = PanelGroup(
        name=name,
        panels=panels,
        transform=transform
    )

    for index, tab_hole in enumerate(tab_holes):
        hole_height = tab_hole.get("height") or 20
        offset_y = tab_hole.get("offset_y") or 5

        if top_layer_no_tabs:
            tab_hole_count = layer_count - 1
        else:
            tab_hole_count = layer_count

        parent_panel_names = []
        for i in range(tab_hole_count):
            parent_panel_names.append(panels[i].name)

        hole_pg = roof_hole(
            name=f"roof_hole_{index}",
            hole_width=tab_hole["width"],
            hole_height=hole_height,
            parent_panel_names=parent_panel_names,
            transform=[Translate((
                offset_c * tab_hole["offset_x"],
                -offset_y + 0.5 * overhang_width + tab_d,
                0
            ))]
        )
        panels_v2.add_child_panel_group(parent=roof, child=hole_pg)
    
    return roof


def roof_hole(
    hole_width: float,
    hole_height: float,
    parent_panel_names: list[str],
    transform: Transform,
    name: str = "roof_hole"
) -> PanelGroup:

    return PanelGroup(
        name=name,
        cutouts=[
            Cutout(
                subtract_from=parent_panel_names,
                workplane=(
                    Workplane("XY")
                    .box(hole_width, hole_height, 100)
                )
            )
        ],
        transform=transform
    )


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


def rafter(
    wall_base_media: Media,
    wall_front_media: Media,
    roof_media: Media,
    roof_layer_count: int,
    width: float,
    gable_height: float,
    transform: Transform,
    name: str = "rafter",
    chimney_floor_hole: bool = False,
    roof_top_layer_no_tabs: bool = True
) -> PanelGroup:
    height=wall_base_media.thickness
    base_wall_width = width - 2 * wall_front_media.thickness
    gable_height_d = 2 * wall_front_media.thickness / width
    base_wall_gable_height = gable_height * (1 - gable_height_d)
    base_wall_height = height + gable_height * gable_height_d
    bottom_tab_width = base_wall_width - 2 * wall_base_media.thickness
    height_d = gable_height * gable_height_d
    if roof_top_layer_no_tabs:
        tab_top_height = (roof_layer_count - 1) * roof_media.thickness - 0.1
    else:
        tab_top_height = roof_layer_count * roof_media.thickness - 0.2

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
            height=tab_top_height,
            thickness=wall_base_media.thickness
        ),
        tab_top_right=Tab(
            direction=TabDirection.OUT,
            width=20,
            offset=-5,
            height=tab_top_height,
            thickness=wall_base_media.thickness
        )
    )

    base_wp = base_wp0

    if chimney_floor_hole:
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
