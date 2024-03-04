import math
from buildings import media_v2
from buildings import panels_v2
from buildings.panels_v2 import PanelGroup
from buildings.transforms_v2 import Transform, Translate, Rotate
from buildings.panels_v2 import roof_panels, window_panels, floor_panels, houses


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

    return main_house_pg
