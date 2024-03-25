import math
from typing import Optional
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
    roof_top_layer_no_tabs: bool = True,
    tab_offset_roof: float = 5,
    tab_length_roof: float = 20
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


def roof_v2(
    media: Media,
    wall_front_media: Media,
    house_length: float,
    house_width: float,
    gable_height: float,
    overhang_left: float,
    overhang_right: float,
    overhang_bottom: float,
    layer_count: int,
    mirror: bool,
    trapezoid: Optional[dict],
    left_stepped_triangle: Optional[dict],
    vertical_holes: list[dict],
    tab_holes: list[dict],
    transform: Transform,
    top_layer_no_tabs: bool = True,
    end_taper: bool = True,
    name: str = "roof",
    roof_overlap_height: float = 0
):
    tri_margin_x = 0.4
    bottom_step_margin = 0.1

    gable_length = math.sqrt(0.25 * house_width * house_width + gable_height * gable_height)
    overhang_d = 0.5 * overhang_bottom * house_width / gable_length

    # New, closer to flat bottom (original used 1.5 factor)
    roof_overhang_d = 1.25 * media.thickness * gable_length / gable_height

    roof_width = house_length
    roof_height = gable_length
    
    tri_width = 0.5 * house_width + overhang_d
    tri_height = gable_length + overhang_bottom

    roof_angle = math.atan2(gable_height, 0.5 * house_width) * 180 / math.pi
    # tab_d = wall_front_media.thickness / math.sin(math.radians(roof_angle))
    tab_d = 2 * wall_front_media.thickness * gable_length / house_width

    overlap_angle = 90 - roof_angle
    overlap_d = media.thickness / math.sin(math.radians(overlap_angle)) * 0.95
    
    panels = []
    for i in range(layer_count):
        if left_stepped_triangle is not None:
            middle_step = 1.25 * (layer_count - i) - 0.35  # TO DO: Give name
            stepped_tri_width = (tri_width / tri_height) * (tri_height - middle_step)
            overhang_left = 0.5 * house_width - tri_margin_x - (tri_width - stepped_tri_width)
        
        if roof_overlap_height > 0:
            end_taper_offset = (layer_count - i) * overlap_d
        elif end_taper and layer_count - i > 3:
            end_taper_offset = roof_overhang_d * (layer_count - i - 3)
        else:
            end_taper_offset = 0

        roof_wp0 = panels_v2.roof_rect(
            width=roof_width,
            height=roof_height - roof_overlap_height,
            overhang_left=overhang_left,
            overhang_right=overhang_right,
            overhang_bottom=overhang_bottom - end_taper_offset,
            thickness=media.thickness
        )

        roof_wp = roof_wp0

        if left_stepped_triangle is not None:
            tri_wp = panels_v2.stepped_right_triangle(
                tri_width=tri_width,
                height=tri_height,
                # bottom_step=overhang_bottom - bottom_step_margin,
                bottom_step=2 * overhang_bottom - bottom_step_margin,
                middle_step=middle_step,
                thickness=10
            ).translate((
                -0.5 * roof_width - overhang_left,
                0,
                -2
            ))
            roof_wp -= tri_wp
        
        if trapezoid is not None:
            tz_bottom_width = trapezoid["house_width"] + 2 * overhang_d + 2 * tri_margin_x
            tz_top_width = trapezoid["house_width"] - 2 * overhang_d + 2 * tri_margin_x
            tz_height = 2 * overhang_bottom
            
            trapezoid_wp = (
                panels_v2.trapezoid(
                    top_width=tz_top_width,
                    bottom_width=tz_bottom_width,
                    height=tz_height,
                    thickness=10
                )
                .translate((
                    trapezoid["offset_x"],
                    -(roof_height + overhang_bottom),
                    -2
                ))
            )
            roof_wp -= trapezoid_wp
        
        for vertical_hole in vertical_holes:
            hole_wp = panels_v2.basic_rect(
                width=vertical_hole["width"],
                height=vertical_hole["height"],
                thickness=20
            ).translate((
                vertical_hole["offset_x"],
                vertical_hole["offset_y"],
                -5
            ))
            roof_wp -= hole_wp
        
        tan_a = 2 * gable_height / house_width
        tab_layer_offset_y = -i * media.thickness * tan_a
        is_top_layer = (i == layer_count - 1)
        # Offset to account for the base gable wall being narrower than the
        # house width, and to start from the center of the gable roof edge
        tab_center_offset_y = -0.5 * (gable_length - tab_d)
        if not (top_layer_no_tabs and is_top_layer):
            for tab_hole in tab_holes:
                tab_height = tab_hole["height"] if "height" in tab_hole else 20
                tab_offset_y = tab_hole["offset_y"] if "offset_y" in tab_hole else 5
                hole_wp = panels_v2.basic_rect(
                    width=tab_hole["width"],
                    height=tab_height,
                    thickness=20
                ).translate((
                    tab_hole["offset_x"],
                    -tab_offset_y + tab_layer_offset_y + tab_center_offset_y,
                    -5
                ))
                roof_wp -= hole_wp

        if mirror:
            roof_wp = roof_wp.mirror("XZ", (0, 0, 0))

        offset_y_sign = -1 if mirror else 1
        layer_offset_y = i * media.thickness * tan_a * offset_y_sign

        panels.append(Panel(
            name=f"roof_layer_{i}",
            media=media,
            workplane=roof_wp,
            transform=[
                Translate((
                    0,
                    layer_offset_y,
                    i * media.thickness
                ))
            ]
        ))

    return PanelGroup(
        name=name,
        panels=panels,
        transform=transform
    )


def test_roof_complex_overlap(
    roof_media,
    house_length,
    house_width,
    gable_height,
    overhang_left,
    overhang_right,
    overhang_bottom
):
    theta = math.atan2(gable_height, 0.5 * house_width) * 180 / math.pi
    layer_count = 5

    pg0 = roof_v2(
        media=roof_media,
        house_length=2 * house_length,
        house_width=house_width,
        gable_height=gable_height,
        overhang_left=overhang_left,
        overhang_right=overhang_right,
        overhang_bottom=overhang_bottom,
        mirror=False,
        trapezoid={
            "offset_x": -30,
            "house_width": house_width
        },
        left_stepped_triangle=None,
        vertical_holes=[],
        tab_holes=[],
        layer_count=layer_count,
        top_layer_no_tabs=True,
        end_taper=True,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), theta)
        ]
    )

    pg1 = roof_v2(
        media=roof_media,
        house_length=house_length,
        house_width=house_width,
        gable_height=gable_height,
        overhang_left=overhang_left,
        overhang_right=overhang_right,
        overhang_bottom=overhang_bottom,
        mirror=True,
        trapezoid=None,
        left_stepped_triangle={},
        vertical_holes=[
            {"width": 10, "height": 20, "offset_x": 10, "offset_y": -20}
        ],
        tab_holes=[
            {"width": 5, "height": 15, "offset_x": 30, "offset_y": -20}
        ],
        layer_count=layer_count,
        top_layer_no_tabs=True,
        end_taper=True,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), -theta),
            Rotate((0, 0, 0), (0, 0, 1), -90),
            Translate((
                -30,  # -0.5 * house_length - 0.5 * house_width,
                -0.5 * house_length - 0.5 * house_width,
                0
            ))
        ]
    )
    pg2 = roof_v2(
        media=roof_media,
        house_length=house_length,
        house_width=house_width,
        gable_height=gable_height,
        overhang_left=overhang_left,
        overhang_right=overhang_right,
        overhang_bottom=overhang_bottom,
        mirror=False,
        trapezoid=None,
        left_stepped_triangle={},
        vertical_holes=[
            {"width": 10, "height": 20, "offset_x": 10, "offset_y": -20}
        ],
        tab_holes=[
            {"width": 5, "height": 15, "offset_x": 30, "offset_y": -20}
        ],
        layer_count=layer_count,
        top_layer_no_tabs=True,
        end_taper=True,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), theta),
            Rotate((0, 0, 0), (0, 0, 1), -90),
            Translate((
                -30,  # -0.5 * house_length - 0.5 * house_width,
                -0.5 * house_length - 0.5 * house_width,
                0
            ))
        ]
    )

    pg = PanelGroup(
        name="test_two_roof_left_tris",
        children=[pg0, pg1, pg2]
    )

    return pg
