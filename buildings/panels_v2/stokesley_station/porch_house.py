import math
from buildings import media_v2
from buildings import panels_v2
from buildings.panels_v2 import PanelGroup
from buildings.transforms_v2 import Transform, Translate, Rotate
from buildings.panels_v2 import door_panels, houses
from buildings.panels_v2.stokesley_station import waiting_room


def porch_house(
    transform: Transform
) -> PanelGroup:
    length = 16  # 15
    width = 34
    height = 35.5  # 36.5
    gable_height = 13.5
    roof_overhang_left = 0
    roof_overhang_right = 4  # 5
    roof_overhang_width = 4.8  # 6
    roof_layer_count = 4

    wall_media = media_v2.CARD_056mm
    base_media = media_v2.CARD_169mm

    wall_base_media = media_v2.CARD_2x169mm
    wall_front_media = media_v2.CARD_2x056mm
    wall_back_media = wall_media
    roof_media = wall_media
    window_media = wall_media

    porch_house_pg = houses.bare_end_house(
        name="porch_house",
        wall_base_media=base_media,  # wall_base_media,
        wall_front_media=wall_front_media,
        wall_back_media=wall_back_media,
        roof_media=roof_media,
        length=length,
        width=width,
        height=height,
        gable_height=gable_height,
        roof_overhang_width=roof_overhang_width,
        roof_overhang_left=roof_overhang_left,
        roof_overhang_right=roof_overhang_right,
        roof_layer_count=roof_layer_count,
        roof_end_taper=False,
        tab_length_x=5,
        tab_length_y=15,
        tab_length_z=20,
        tab_length_roof=10,
        tab_offset_roof=1,
        roof_tab_holes=[
            # Left wall with no overhang (open hole at edge of roof)
            {
                "offset_x": -0.5 * length,
                "width": 2 * base_media.thickness,
                "height": 10,
                "offset_y": 1
            },
            # Right wall
            {
                "offset_x": 0.5 * length - wall_front_media.thickness - 0.5 * base_media.thickness,
                "width": base_media.thickness,
                "height": 10,
                "offset_y": 1
            }
        ],
        floor_hole=False,
        transform=transform
    )

    right_wall_pg = panels_v2.get_child_panel_group(
        panel_group=porch_house_pg,
        name="right_wall"
    )

    # Porch house door
    panels_v2.add_child_panel_group(
        parent=right_wall_pg,
        child=door_panels.front_door(
            base_media=base_media,
            media=window_media,
            width=13,
            height=35.5,
            transform=[Translate((0, 6.5, 0))]
        )
    )

    return porch_house_pg
