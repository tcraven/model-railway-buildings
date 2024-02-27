import math
from cadquery import Workplane
from buildings import panels_v2
from buildings.media_v2 import Media
from buildings.panels_v2 import Cutout, Panel, PanelGroup
from buildings.panels_v2 import window_panels
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
    name: str = "roof"
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
        if layer_count - i > 3:
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
        hole_pg = roof_hole(
            name=f"roof_hole_{index}",
            hole_width=tab_hole["width"],
            hole_height=20,
            parent_panel_names=[panel.name for panel in panels],
            transform=[Translate((
                offset_c * tab_hole["offset_x"],
                -5 + 0.5 * overhang_width + tab_d,
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
                # panels_v2.basic_rect(
                #     width=hole_width,
                #     height=hole_height,
                #     thickness=100
                # )
            )
        ],
        transform=transform
    )
