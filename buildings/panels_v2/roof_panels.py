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
    overhang_length: float,
    overhang_width: float,
    layer_count: int,
    transform: Transform,
    name: str = "roof"
) -> PanelGroup:

    tan_a = 2 * gable_height / house_width
    gable_length = math.sqrt(0.25 * house_width * house_width + gable_height * gable_height)
    roof_width = house_length + 2 * overhang_length
    roof_height = gable_length + overhang_width
    roof_angle = math.atan2(gable_height, 0.5 * house_width) * 180 / math.pi
    tab_d = 0.5 * wall_front_media.thickness / math.cos(math.radians(roof_angle))

    panels = []
    for i in range(layer_count):
        panels.append(Panel(
            name=f"p{i}",
            media=roof_media,
            workplane=panels_v2.basic_rect(
                width=roof_width,
                height=roof_height,
                thickness=roof_media.thickness
            ),
            transform=[
                Translate((
                    0,
                    i * roof_media.thickness * tan_a,
                    i * roof_media.thickness
                ))
            ]
        ))

    roof = PanelGroup(
        name=name,
        panels=panels,
        transform=transform
    )

    hole_1 = roof_hole(
        name="roof_hole_1",
        hole_width=wall_base_media.thickness,
        hole_height=20,
        parent_panel_names=[panel.name for panel in panels],
        transform=[Translate((
            -0.5 * house_length + wall_front_media.thickness + 0.5 * wall_base_media.thickness,
            -5 + 0.5 * overhang_width + tab_d,
            0
        ))]
    )
    hole_2 = roof_hole(
        name="roof_hole_2",
        hole_width=wall_base_media.thickness,
        hole_height=20,
        parent_panel_names=[panel.name for panel in panels],
        transform=[Translate((
            0.5 * house_length - wall_front_media.thickness - 0.5 * wall_base_media.thickness,
            -5 + 0.5 * overhang_width + tab_d,
            0
        ))]
    )

    panels_v2.add_child_panel_group(parent=roof, child=hole_1)
    panels_v2.add_child_panel_group(parent=roof, child=hole_2)
    
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
