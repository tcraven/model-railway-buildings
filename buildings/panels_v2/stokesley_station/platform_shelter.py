import math
from buildings import media_v2
from buildings import panels_v2
from buildings.panels_v2 import PanelGroup
from buildings.transforms_v2 import Transform, Translate, Rotate
from buildings.panels_v2 import roof_panels, window_panels, chimneys, houses, door_panels


def platform_shelter(
    transform: Transform
) -> PanelGroup:
    length = 182
    width = 32
    height = 50
    gable_height = 8
    roof_overhang_left = 3
    roof_overhang_right = 3
    roof_overhang_bottom = 3.5
    roof_layer_count = 2

    rafter_0_offset_x = 65
    rafter_1_offset_x = -4
    rafter_2_offset_x = -43

    wall_media = media_v2.CARD_056mm
    base_media = media_v2.CARD_169mm

    wall_base_media = media_v2.CARD_2x169mm
    wall_front_media = media_v2.CARD_2x056mm
    wall_back_media = wall_media
    roof_media = wall_media
    window_media = wall_media

    # chimney_depth = 5.06 + 2 * wall_media.thickness
    # chimney_width = 8
    # roof_chimney_hole_gap_width = 0.5
    # roof_chimney_hole_gap_height = 2.75
    roof_chimney_holes = []

    tab_offset_roof = 2
    tab_length_roof = 10

    platform_shelter_pg = houses.basic_house(
        name="platform_shelter",
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
            # Left wall
            {
                "offset_x": -(0.5 * length - wall_front_media.thickness - 0.5 * wall_base_media.thickness),
                "offset_y": tab_offset_roof,
                "width": wall_base_media.thickness,
                "height": tab_length_roof
            },
            # Rafter 0
            {
                "offset_x": rafter_0_offset_x,
                "offset_y": tab_offset_roof,
                "width": wall_base_media.thickness,
                "height": tab_length_roof
            },
            # Rafter 1
            {
                "offset_x": rafter_1_offset_x,
                "offset_y": tab_offset_roof,
                "width": wall_base_media.thickness,
                "height": tab_length_roof
            },
            # Rafter 2
            {
                "offset_x": rafter_2_offset_x,
                "offset_y": tab_offset_roof,
                "width": wall_base_media.thickness,
                "height": tab_length_roof
            },
            # Right wall
            {
                "offset_x": 0.5 * length - wall_front_media.thickness - 0.5 * wall_base_media.thickness,
                "offset_y": tab_offset_roof,
                "width": wall_base_media.thickness,
                "height": tab_length_roof
            }
        ],
        roof_vertical_holes=roof_chimney_holes,
        tab_offset_roof=tab_offset_roof,
        tab_length_roof=tab_length_roof,
        floor_hole=False,
        back_roof_vertical_holes=[
            {
                "offset_x": -61,
                "offset_y": -20,
                "width": 8 + 0.2,
                "height": 7.7
            }
        ],
        tab_length_y=15,
        transform=transform
    )

    front_wall_pg = panels_v2.get_child_panel_group(
        panel_group=platform_shelter_pg,
        name="front_wall"
    )
    back_wall_pg = panels_v2.get_child_panel_group(
        panel_group=platform_shelter_pg,
        name="back_wall"
    )
    right_wall_pg = panels_v2.get_child_panel_group(
        panel_group=platform_shelter_pg,
        name="right_wall"
    )
    left_wall_pg = panels_v2.get_child_panel_group(
        panel_group=platform_shelter_pg,
        name="left_wall"
    )

    # Rafters
    panels_v2.add_child_panel_group(
        parent=platform_shelter_pg,
        child=roof_panels.rafter(
            name="rafter0",
            wall_base_media=wall_base_media,
            wall_front_media=wall_front_media,
            roof_media=roof_media,
            roof_layer_count=roof_layer_count,
            width=width,
            gable_height=gable_height,
            tab_length_roof=tab_length_roof,
            tab_offset_roof=tab_offset_roof,
            transform=[
                Rotate((0, 0, 0), (1, 0, 0), 90),
                Rotate((0, 0, 0), (0, 0, 1), 90),
                Translate((
                    rafter_0_offset_x - 0.5 * wall_base_media.thickness,
                    0,
                    height - 0.5 * wall_base_media.thickness
                ))
            ]
        )
    )
    panels_v2.add_child_panel_group(
        parent=front_wall_pg,
        child=roof_panels.rafter_holes(
            wall_base_media=wall_base_media,
            transform=[Translate((
                -rafter_0_offset_x,
                0.5 * height,
                0
            ))]
        )
    )
    panels_v2.add_child_panel_group(
        parent=back_wall_pg,
        child=roof_panels.rafter_holes(
            wall_base_media=wall_base_media,
            transform=[Translate((
                rafter_0_offset_x,
                0.5 * height,
                0
            ))]
        )
    )

    panels_v2.add_child_panel_group(
        parent=platform_shelter_pg,
        child=roof_panels.rafter(
            name="rafter1",
            wall_base_media=wall_base_media,
            wall_front_media=wall_front_media,
            roof_media=roof_media,
            roof_layer_count=roof_layer_count,
            width=width,
            gable_height=gable_height,
            tab_length_roof=tab_length_roof,
            tab_offset_roof=tab_offset_roof,
            transform=[
                Rotate((0, 0, 0), (1, 0, 0), 90),
                Rotate((0, 0, 0), (0, 0, 1), 90),
                Translate((
                    rafter_1_offset_x - 0.5 * wall_base_media.thickness,
                    0,
                    height - 0.5 * wall_base_media.thickness
                ))
            ]
        )
    )
    panels_v2.add_child_panel_group(
        parent=front_wall_pg,
        child=roof_panels.rafter_holes(
            wall_base_media=wall_base_media,
            transform=[Translate((
                -rafter_1_offset_x,
                0.5 * height,
                0
            ))]
        )
    )
    panels_v2.add_child_panel_group(
        parent=back_wall_pg,
        child=roof_panels.rafter_holes(
            wall_base_media=wall_base_media,
            transform=[Translate((
                rafter_1_offset_x,
                0.5 * height,
                0
            ))]
        )
    )

    panels_v2.add_child_panel_group(
        parent=platform_shelter_pg,
        child=roof_panels.rafter(
            name="rafter2",
            wall_base_media=wall_base_media,
            wall_front_media=wall_front_media,
            roof_media=roof_media,
            roof_layer_count=roof_layer_count,
            width=width,
            gable_height=gable_height,
            tab_length_roof=tab_length_roof,
            tab_offset_roof=tab_offset_roof,
            transform=[
                Rotate((0, 0, 0), (1, 0, 0), 90),
                Rotate((0, 0, 0), (0, 0, 1), 90),
                Translate((
                    rafter_2_offset_x - 0.5 * wall_base_media.thickness,
                    0,
                    height - 0.5 * wall_base_media.thickness
                ))
            ]
        )
    )
    panels_v2.add_child_panel_group(
        parent=front_wall_pg,
        child=roof_panels.rafter_holes(
            wall_base_media=wall_base_media,
            transform=[Translate((
                -rafter_2_offset_x,
                0.5 * height,
                0
            ))]
        )
    )
    panels_v2.add_child_panel_group(
        parent=back_wall_pg,
        child=roof_panels.rafter_holes(
            wall_base_media=wall_base_media,
            transform=[Translate((
                rafter_2_offset_x,
                0.5 * height,
                0
            ))]
        )
    )

    # Door 1 (left)
    panels_v2.add_child_panel_group(
        parent=left_wall_pg,
        child=door_panels.door(
            base_media=wall_base_media,
            media=window_media,
            door_width=11,
            door_height=30.5,
            is_open=False,
            transform=[Translate((-0.5, 30.25 - 0.5 * height, 0))]
        )
    )

    # Window 1 (right)
    panels_v2.add_child_panel_group(
        parent=right_wall_pg,
        child=window_panels.window(
            base_media=wall_base_media,
            media=window_media,
            window_width=7,
            window_height=14,
            sill_width=7 + 3,
            sill_height=2,
            window_margin=2,
            no_vertical_frame=True,
            top_arc_height=0.25,
            transform=[Translate((1.75, 37.25 - 0.5 * height, 0))]
        )
    )

    # Window 2 (front right)
    panels_v2.add_child_panel_group(
        parent=front_wall_pg,
        child=window_panels.window(
            base_media=wall_base_media,
            media=window_media,
            window_width=7,
            window_height=14,
            sill_width=7 + 3,
            sill_height=2,
            window_margin=2,
            no_vertical_frame=True,
            top_arc_height=0.25,
            transform=[Translate((-76, 38 - 0.5 * height, 0))]
        )
    )

    # Window 3 (front left 1)
    panels_v2.add_child_panel_group(
        parent=front_wall_pg,
        child=window_panels.window(
            base_media=wall_base_media,
            media=window_media,
            window_width=7,
            window_height=14,
            sill_width=7 + 3,
            sill_height=2,
            window_margin=2,
            no_vertical_frame=True,
            top_arc_height=0.25,
            transform=[Translate((55, 38 - 0.5 * height, 0))]
        )
    )

    # Window 4 (front left 2)
    panels_v2.add_child_panel_group(
        parent=front_wall_pg,
        child=window_panels.window(
            base_media=wall_base_media,
            media=window_media,
            window_width=7,
            window_height=14,
            sill_width=7 + 3,
            sill_height=2,
            window_margin=2,
            no_vertical_frame=True,
            top_arc_height=0.25,
            transform=[Translate((72, 38 - 0.5 * height, 0))]
        )
    )

    # Door set 1
    panels_v2.add_child_panel_group(
        parent=front_wall_pg,
        child=door_panels.shelter_inset_door_windows(
            base_media=wall_base_media,
            media=window_media,
            width=55,
            height=30.5,
            transform=[Translate((-30.5, 30.25 - 0.5 * height, 0))]
        )
    )

    # Chimney
    panels_v2.add_child_panel_group(
        parent=back_wall_pg,
        child=chimneys.external_chimney(
            base_media=base_media,
            wall_media=wall_media,
            chimney_width=8,
            core_base_layer_count=2,
            core_wall_layer_count=1,
            shaft_height=65.5,
            shaft_middle_height=8,
            shaft_base_height=38,  # 35
            shaft_base_width=24,
            wall_offset=2 * base_media.thickness,
            transform=[
                Translate((-61, -0.5 * height, 0))
            ]
        )
    )

    return platform_shelter_pg
