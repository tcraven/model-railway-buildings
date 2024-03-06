import math
from buildings import media_v2
from buildings import panels_v2
from buildings.panels_v2 import PanelGroup
from buildings.transforms_v2 import Transform, Translate, Rotate
from buildings.panels_v2 import chimneys, window_panels, wall_panels, houses
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

    chimney_width = 8.44 + 2 * wall_media.thickness
    chimney_height = 11 + 2 * wall_media.thickness
    roof_chimney_hole_gap_width = 0.5
    roof_chimney_hole_gap_height = 2.75
    roof_chimney_holes = [
        {
            "offset_x": -23 - 0.5 * chimney_width,
            "width": chimney_width + roof_chimney_hole_gap_width,
            "height": chimney_height + roof_chimney_hole_gap_height
        }
    ]

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
                "offset_x": -(0.5 * length - 0.5 * wall_base_media.thickness),
                "width": wall_base_media.thickness
            },
            # Right wall
            {
                "offset_x": 0.5 * length - wall_front_media.thickness - 0.5 * wall_base_media.thickness,
                "width": wall_base_media.thickness
            }
        ],
        roof_chimney_holes=roof_chimney_holes,
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

    left_wall_pg = panels_v2.get_child_panel_group(
        panel_group=side_house_pg,
        name="left_wall"
    )

    # Connector slots and pins
    # Pin height is the thickness of the side house wall plus the thickness of
    # the front and base wall of the main house, minus a small margin
    connector_offset_y = -0.5 * height + 40
    pin_height = (
        wall_base_media.thickness + wall_base_media.thickness +
        wall_front_media.thickness - 0.2
    )
    panels_v2.add_child_panel_group(
        parent=left_wall_pg,
        child=wall_panels.connector_slots(
            base_media=wall_base_media,
            hole_spacing=40,
            pin_width=40,
            include_pins=True,
            pin_height=pin_height,
            transform=[Translate((0, connector_offset_y, 0))]
        )
    )

    chimney_z = 72 + 33 - 10

    # Chimney
    panels_v2.add_child_panel_group(
        parent=side_house_pg,
        child=chimneys.chimney(
            base_media=media_v2.CARD_169mm,
            wall_media=media_v2.CARD_056mm,
            chimney_width=11,
            core_base_layer_count=4,
            core_wall_layer_count=1,
            shaft_height=27,  # 27
            shaft_base_height=20,  # 20
            transform=[
                Rotate((0, 0, 0), (1, 0, 0), 90),
                Rotate((0, 0, 0), (0, 0, 1), -90),
                Translate((
                    -23,
                    0,
                    chimney_z
                ))
            ]
        )
    )
    panels_v2.add_child_panel_group(
        parent=left_wall_pg,
        child=wall_panels.chimney_hole(
            wall_media=media_v2.CARD_056mm,
            chimney_width=11,
            transform=[
                Translate((0, chimney_z - 0.5 * height, 0))
            ]
        )
    )

    return side_house_pg
