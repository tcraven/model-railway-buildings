from buildings import panels_v2
from buildings.media_v2 import Media
from buildings.panels_v2 import Panel, PanelGroup, Cutout
from buildings.transforms_v2 import Transform, Translate
from buildings.tabs import Tab, TabDirection


def floor(
    wall_base_media: Media,
    wall_front_media: Media,
    wall_back_media: Media,
    width: float,
    height: float,
    transform: Transform,
    name: str = "floor",
    tab_length_x: float = 30,
    tab_length_y: float = 30,
    hole: bool = True
) -> PanelGroup:
    base_floor = Panel(
        name="base_floor",
        media=wall_base_media,
        workplane=panels_v2.rect(
            width=width - 2 * (wall_front_media.thickness + wall_base_media.thickness),
            height=height - 2 * (wall_front_media.thickness + wall_base_media.thickness),
            thickness=wall_base_media.thickness,
            tab_left=Tab(
                direction=TabDirection.OUT,
                width=tab_length_y,
                height=wall_base_media.thickness,
                thickness=wall_base_media.thickness
            ),
            tab_right=Tab(
                direction=TabDirection.OUT,
                width=tab_length_y,
                height=wall_base_media.thickness,
                thickness=wall_base_media.thickness
            ),
            tab_bottom=Tab(
                direction=TabDirection.OUT,
                width=tab_length_x,
                height=wall_base_media.thickness,
                thickness=wall_base_media.thickness
            ),
            tab_top=Tab(
                direction=TabDirection.OUT,
                width=tab_length_x,
                height=wall_base_media.thickness,
                thickness=wall_base_media.thickness
            )
        )
    )
    inside_floor = Panel(
        name="inside_floor",
        media=wall_back_media,
        workplane=panels_v2.basic_rect(
            width=width - 2 * (wall_front_media.thickness + wall_base_media.thickness + wall_back_media.thickness + 0.25),
            height=height - 2 * (wall_front_media.thickness + wall_base_media.thickness + wall_back_media.thickness + 0.25),
            thickness=wall_back_media.thickness
        ),
        transform=[Translate((0, 0, -wall_back_media.thickness))]
    )
    floor = PanelGroup(
        name=name,
        panels=[base_floor, inside_floor],
        transform=transform
    )

    if hole:
        floor_hole = PanelGroup(
            name="floor_hole",
            cutouts=[
                Cutout(
                    subtract_from=["base_floor", "inside_floor"],
                    workplane=panels_v2.chamfered_hole(
                        width=width - 2 * wall_front_media.thickness - 20,
                        height=height - 2 * wall_front_media.thickness - 20
                    )
                )
            ]
        )
        panels_v2.add_child_panel_group(parent=floor, child=floor_hole)
    
    return floor
