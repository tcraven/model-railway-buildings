import math
from buildings import media_v2
from buildings import panels_v2
from buildings.panels_v2 import PanelGroup
from buildings.transforms_v2 import Transform, Translate, Rotate
from buildings.panels_v2 import roof_panels, window_panels, floor_panels, houses
from buildings.panels_v2.stokesley_station import waiting_room


def side_house(
    transform: Transform
) -> PanelGroup:
    length = 58
    width = 69
    height = 85
    gable_height = 22
    roof_overhang_left = 0
    roof_overhang_right = 5
    roof_overhang_width = 6
    roof_layer_count = 5

    wall_media = media_v2.CARD_056mm
    base_media = media_v2.CARD_169mm

    wall_base_media = media_v2.CARD_2x169mm
    wall_front_media = media_v2.CARD_2x056mm
    wall_back_media = wall_media
    roof_media = wall_media
    window_media = wall_media

    side_house_pg = houses.bare_end_house(
        name="side_house",
        wall_base_media=wall_base_media,
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
        roof_tab_holes=[
            # Left wall with no overhang (open hole at edge of roof)
            {
                "offset_x": -0.5 * length,
                "width": 2 * wall_base_media.thickness
            },
            # Right wall
            {
                "offset_x": 0.5 * length - wall_front_media.thickness - 0.5 * wall_base_media.thickness,
                "width": wall_base_media.thickness
            }
        ],
        transform=transform
    )

    back_wall_pg = panels_v2.get_child_panel_group(
        panel_group=side_house_pg,
        name="back_wall"
    )

    # Back wall window offsets have half of the front wall media thickness
    # added because the house has a bare end
    ox = 0.5 * wall_front_media.thickness

    # Side house window 1
    panels_v2.add_child_panel_group(
        parent=back_wall_pg,
        child=window_panels.window(
            base_media=wall_base_media,
            media=window_media,
            window_width=11.5,
            window_height=22,
            sill_width=11.5 + 3,
            sill_height=2,
            window_margin=2,
            transform=[Translate((ox + 15.25, -8, 0))]
        )
    )
    # Side house window 2
    panels_v2.add_child_panel_group(
        parent=back_wall_pg,
        child=window_panels.window(
            base_media=wall_base_media,
            media=window_media,
            window_width=11.5,
            window_height=22,
            sill_width=11.5 + 3,
            sill_height=2,
            window_margin=2,
            transform=[Translate((ox - 11, -8, 0))]
        )
    )
    # Side house window 3
    panels_v2.add_child_panel_group(
        parent=back_wall_pg,
        child=window_panels.window(
            base_media=wall_base_media,
            media=window_media,
            window_width=13,
            window_height=20,
            sill_width=13 + 3,
            sill_height=2,
            window_margin=2,
            transform=[Translate((ox + 0.5, 29, 0))]
        )
    )


    return side_house_pg
