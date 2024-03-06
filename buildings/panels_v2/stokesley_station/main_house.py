import math
from buildings import media_v2
from buildings import panels_v2
from buildings.panels_v2 import PanelGroup
from buildings.transforms_v2 import Transform, Translate, Rotate
from buildings.panels_v2 import roof_panels, window_panels, chimneys, houses, wall_panels


def main_house(
    transform: Transform
) -> PanelGroup:
    length = 156
    width = 69
    height = 85
    gable_height = 22
    roof_overhang_left = 5
    roof_overhang_right = 5
    roof_overhang_width = 6
    roof_layer_count = 5

    rafter_offset_x = 26

    wall_media = media_v2.CARD_056mm
    base_media = media_v2.CARD_169mm

    wall_base_media = media_v2.CARD_2x169mm
    wall_front_media = media_v2.CARD_2x056mm
    wall_back_media = wall_media
    roof_media = wall_media
    window_media = wall_media

    chimney_width = 7.31 + 2 * wall_media.thickness
    chimney_height = 10.5 + 2 * wall_media.thickness
    roof_chimney_hole_gap_width = 0.5
    roof_chimney_hole_gap_height = 2.75
    roof_chimney_holes = [
        # Chimney 1
        {
            "offset_x": 78 - wall_front_media.thickness - 0.5 * chimney_width,
            "width": chimney_width + roof_chimney_hole_gap_width,
            "height": chimney_height + roof_chimney_hole_gap_height
        },
        # Chimney 2
        {
            "offset_x": -(78 - wall_front_media.thickness - 0.5 * chimney_width),
            "width": chimney_width + roof_chimney_hole_gap_width,
            "height": chimney_height + roof_chimney_hole_gap_height
        }
    ]

    main_house_pg = houses.basic_house(
        name="main_house",
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
            # Left wall
            {
                "offset_x": -(0.5 * length - wall_front_media.thickness - 0.5 * wall_base_media.thickness),
                "width": wall_base_media.thickness
            },
            # Rafter 0
            {
                "offset_x": -rafter_offset_x,  # + 0.5 * wall_base_media.thickness,
                "width": wall_base_media.thickness
            },
            # Rafter 1
            {
                "offset_x": rafter_offset_x,  # + 0.5 * wall_base_media.thickness,
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

    front_wall_pg = panels_v2.get_child_panel_group(
        panel_group=main_house_pg,
        name="front_wall"
    )
    back_wall_pg = panels_v2.get_child_panel_group(
        panel_group=main_house_pg,
        name="back_wall"
    )
    right_wall_pg = panels_v2.get_child_panel_group(
        panel_group=main_house_pg,
        name="right_wall"
    )
    left_wall_pg = panels_v2.get_child_panel_group(
        panel_group=main_house_pg,
        name="left_wall"
    )

    # Rafters
    panels_v2.add_child_panel_group(
        parent=main_house_pg,
        child=roof_panels.rafter(
            name="rafter0",
            wall_base_media=wall_base_media,
            wall_front_media=wall_front_media,
            roof_media=roof_media,
            roof_layer_count=roof_layer_count,
            width=width,
            gable_height=gable_height,
            transform=[
                Rotate((0, 0, 0), (1, 0, 0), 90),
                Rotate((0, 0, 0), (0, 0, 1), 90),
                Translate((
                    -rafter_offset_x - 0.5 * wall_base_media.thickness,
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
                rafter_offset_x,
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
                -rafter_offset_x,
                0.5 * height,
                0
            ))]
        )
    )

    panels_v2.add_child_panel_group(
        parent=main_house_pg,
        child=roof_panels.rafter(
            name="rafter1",
            wall_base_media=wall_base_media,
            wall_front_media=wall_front_media,
            roof_media=roof_media,
            roof_layer_count=roof_layer_count,
            width=width,
            gable_height=gable_height,
            transform=[
                Rotate((0, 0, 0), (1, 0, 0), 90),
                Rotate((0, 0, 0), (0, 0, 1), 90),
                Translate((
                    rafter_offset_x - 0.5 * wall_base_media.thickness,
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
                -rafter_offset_x,
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
                rafter_offset_x,
                0.5 * height,
                0
            ))]
        )
    )

    # Main house window 1
    panels_v2.add_child_panel_group(
        parent=right_wall_pg,
        child=window_panels.window(
            base_media=wall_base_media,
            media=window_media,
            window_width=10,
            window_height=22,
            sill_width=10 + 3,
            sill_height=2,
            window_margin=2,
            transform=[Translate((15.75, -8, 0))]
        )
    )
    # Main house window 2
    panels_v2.add_child_panel_group(
        parent=right_wall_pg,
        child=window_panels.window(
            base_media=wall_base_media,
            media=window_media,
            window_width=10,
            window_height=22,
            sill_width=10 + 3,
            sill_height=2,
            window_margin=2,
            transform=[Translate((-15.5, -8, 0))]
        )
    )
    # Main house arch window
    panels_v2.add_child_panel_group(
        parent=right_wall_pg,
        child=window_panels.arch_faux_window(
            base_media=wall_base_media,
            media=window_media,
            window_width=9,
            window_height=13,
            sill_width=9 + 1.5,
            sill_height=2,
            window_margin=2,
            transform=[Translate((0, 27, 0))]
        )
    )

    # Main house window 3
    panels_v2.add_child_panel_group(
        parent=back_wall_pg,
        child=window_panels.window(
            base_media=wall_base_media,
            media=window_media,
            window_width=14,
            window_height=22,
            sill_width=14 + 3,
            sill_height=2,
            window_margin=2,
            transform=[Translate((44, 26.5, 0))]
        )
    )
    # Main house window 4
    panels_v2.add_child_panel_group(
        parent=back_wall_pg,
        child=window_panels.window(
            base_media=wall_base_media,
            media=window_media,
            window_width=10.5,
            window_height=22,
            sill_width=10.5 + 3,
            sill_height=2,
            window_margin=2,
            transform=[Translate((0, 26.5, 0))]
        )
    )
    # Main house window 5
    panels_v2.add_child_panel_group(
        parent=back_wall_pg,
        child=window_panels.window(
            base_media=wall_base_media,
            media=window_media,
            window_width=14,
            window_height=22,
            sill_width=14 + 3,
            sill_height=2,
            window_margin=2,
            transform=[Translate((-44, 26.5, 0))]
        )
    )
    # Main house window 6
    panels_v2.add_child_panel_group(
        parent=back_wall_pg,
        child=window_panels.window(
            base_media=wall_base_media,
            media=window_media,
            window_width=14,
            window_height=22,
            sill_width=14 + 3,
            sill_height=2,
            window_margin=2,
            transform=[Translate((44, -14, 0))]
        )
    )
    # Main house window 7
    panels_v2.add_child_panel_group(
        parent=back_wall_pg,
        child=window_panels.window(
            base_media=wall_base_media,
            media=window_media,
            window_width=14,
            window_height=22,
            sill_width=14 + 3,
            sill_height=2,
            window_margin=2,
            transform=[Translate((-44, -14, 0))]
        )
    )

    # Porch house connector slots
    porch_connector_offset_y = -0.5 * height + 20
    panels_v2.add_child_panel_group(
        parent=back_wall_pg,
        child=wall_panels.connector_slots(
            base_media=base_media,
            hole_spacing=20,
            pin_width=20,
            include_pins=False,
            transform=[Translate((0, porch_connector_offset_y, 0))]
        )
    )

    # Side house connector slots
    connector_offset_x = -38
    connector_offset_y = -0.5 * height + 40
    panels_v2.add_child_panel_group(
        parent=front_wall_pg,
        child=wall_panels.connector_slots(
            base_media=wall_base_media,
            hole_spacing=40,
            pin_width=40,
            include_pins=False,
            transform=[Translate((connector_offset_x, connector_offset_y, 0))]
        )
    )

    chimney_z = 72 + 33 - 10

    # Chimney 1
    panels_v2.add_child_panel_group(
        parent=main_house_pg,
        child=chimneys.chimney(
            base_media=media_v2.CARD_169mm,
            wall_media=media_v2.CARD_056mm,
            chimney_width=10.5,
            core_base_layer_count=3,
            core_wall_layer_count=2,
            shaft_height=27,  # 27
            shaft_base_height=20,  # 20
            transform=[
                Rotate((0, 0, 0), (1, 0, 0), 90),
                Rotate((0, 0, 0), (0, 0, 1), -90),
                Translate((
                    78 - wall_front_media.thickness,
                    0,
                    chimney_z
                ))
            ]
        )
    )
    panels_v2.add_child_panel_group(
        parent=right_wall_pg,
        child=wall_panels.chimney_hole(
            wall_media=media_v2.CARD_056mm,
            chimney_width=10.5,
            transform=[
                Translate((0, chimney_z - 0.5 * height, 0))
            ]
        )
    )

    # Chimney 2
    panels_v2.add_child_panel_group(
        parent=main_house_pg,
        child=chimneys.chimney(
            base_media=media_v2.CARD_169mm,
            wall_media=media_v2.CARD_056mm,
            chimney_width=10.5,
            core_base_layer_count=3,
            core_wall_layer_count=2,
            shaft_height=27,  # 27
            shaft_base_height=20,  # 20
            transform=[
                Rotate((0, 0, 0), (1, 0, 0), 90),
                Rotate((0, 0, 0), (0, 0, 1), 90),
                Translate((
                    -78 + wall_front_media.thickness,
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
            chimney_width=10.5,
            transform=[
                Translate((0, chimney_z - 0.5 * height, 0))
            ]
        )
    )

    return main_house_pg
