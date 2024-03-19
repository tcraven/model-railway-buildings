import math
from buildings import media_v2
from buildings import panels_v2
from buildings.panels_v2 import PanelGroup
from buildings.transforms_v2 import Transform, Translate, Rotate
from buildings.panels_v2 import chimneys, window_panels, wall_panels, houses
from buildings.panels_v2.stokesley_station import waiting_room


def back_house(
    transform: Transform
) -> PanelGroup:
    length = 72
    width = 53
    height = 85
    gable_height = 53 * (22 / 69)
    roof_overhang_left = 0
    roof_overhang_right = 5
    roof_overhang_bottom = 6
    roof_layer_count = 5

    wall_media = media_v2.CARD_056mm
    base_media = media_v2.CARD_169mm

    wall_base_media = media_v2.CARD_2x169mm
    wall_front_media = media_v2.CARD_2x056mm
    wall_back_media = wall_media
    roof_media = wall_media
    window_media = wall_media

    chimney_width = 7.88 + 2 * wall_media.thickness
    chimney_height = 10 + 2 * wall_media.thickness
    roof_chimney_hole_gap_width = 0.5
    roof_chimney_hole_gap_height = 2.75
    back_roof_vertical_holes = [
        {
            "offset_x": 8.5,
            "offset_y": -24.5,
            "width": chimney_height + roof_chimney_hole_gap_width,
            "height": chimney_width + roof_chimney_hole_gap_height
        }
    ]

    back_house_pg = houses.bare_end_house(
        name="back_house",
        wall_base_media=wall_base_media,
        wall_front_media=wall_front_media,
        wall_back_media=wall_back_media,
        roof_media=roof_media,
        length=length,
        width=width,
        height=height,
        gable_height=gable_height,
        roof_overhang_bottom=roof_overhang_bottom,
        roof_overhang_left=roof_overhang_left,
        roof_overhang_right=roof_overhang_right,
        roof_layer_count=roof_layer_count,
        roof_tab_holes=[
            # Left wall with no overhang (open hole at edge of roof)
            {
                "offset_x": -(0.5 * length - 0.5 * wall_base_media.thickness),
                "offset_y": 0,
                "width": wall_base_media.thickness,
                "height": 15
            },
            # Right wall
            {
                "offset_x": 0.5 * length - wall_front_media.thickness - 0.5 * wall_base_media.thickness,
                "offset_y": 0,
                "width": wall_base_media.thickness,
                "height": 15
            }
        ],
        roof_vertical_holes=[],
        roof_left_stepped_triangle={},
        tab_offset_roof=0,
        tab_length_roof=15,
        front_roof_overlap_height=9.6,
        no_front_wall=True,
        back_roof_vertical_holes=back_roof_vertical_holes,
        transform=transform
    )

    floor_pg = panels_v2.get_child_panel_group(
        panel_group=back_house_pg,
        name="floor"
    )
    left_wall_pg = panels_v2.get_child_panel_group(
        panel_group=back_house_pg,
        name="left_wall"
    )
    right_wall_pg = panels_v2.get_child_panel_group(
        panel_group=back_house_pg,
        name="right_wall"
    )
    back_wall_pg = panels_v2.get_child_panel_group(
        panel_group=back_house_pg,
        name="back_wall"
    )

    # # Back wall window offsets have half of the front wall media thickness
    # # added because the house has a bare end
    ox = 0.5 * wall_front_media.thickness

    hole_offset = 30.5

    # Floor hole (to fit against main house)
    panels_v2.add_child_panel_group(
        parent=floor_pg,
        child=wall_panels.hole(
            hole_width=100,
            hole_height=20,
            transform=[Translate((0, -hole_offset, 0))]  # -30
        )
    )

    # Left wall hole (to fit against main house)
    panels_v2.add_child_panel_group(
        parent=left_wall_pg,
        child=wall_panels.hole(
            hole_width=20,
            hole_height=height,
            transform=[Translate((-hole_offset, 0, 0))]
        )
    )
    panels_v2.add_child_panel_group(
        parent=left_wall_pg,
        child=wall_panels.hole(
            hole_width=20,
            hole_height=2 * height,
            transform=[Translate((-hole_offset - 2, 0, 0))]
        )
    )

    # Right wall hole (to fit against main house)
    panels_v2.add_child_panel_group(
        parent=right_wall_pg,
        child=wall_panels.hole(
            hole_width=20,
            hole_height=height,
            transform=[Translate((hole_offset, 0, 0))]
        )
    )
    panels_v2.add_child_panel_group(
        parent=right_wall_pg,
        child=wall_panels.hole(
            hole_width=20,
            hole_height=2 * height,
            transform=[Translate((hole_offset + 2, 0, 0))]
        )
    )



    chimney_z = 72 + 33 - 31

    # Chimney 10 x 7.5 (4,0 7.88)
    panels_v2.add_child_panel_group(
        parent=back_house_pg,
        child=chimneys.chimney(
            base_media=media_v2.CARD_169mm,
            wall_media=media_v2.CARD_056mm,
            chimney_width=10,
            core_base_layer_count=4,
            core_wall_layer_count=0,
            shaft_height=37,
            shaft_base_height=24,
            transform=[
                Rotate((0, 0, 0), (1, 0, 0), 90),
                Rotate((0, 0, 0), (0, 0, 1), -180),
                Translate((
                    8.5,
                    -(0.5 * width - wall_front_media.thickness),
                    chimney_z
                ))
            ]
        )
    )
    panels_v2.add_child_panel_group(
        parent=back_wall_pg,
        child=wall_panels.chimney_hole(
            wall_media=media_v2.CARD_056mm,
            chimney_width=10,
            transform=[
                Translate((
                    8.5 + ox,
                    chimney_z - 0.5 * height,
                    0
                ))
            ]
        )
    )

    return back_house_pg
