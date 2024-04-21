import math
from buildings import media_v2
from buildings import panels_v2
from buildings.panels_v2 import PanelGroup
from buildings.transforms_v2 import Transform, Translate, Rotate
from buildings.panels_v2 import roof_panels, window_panels, chimneys, houses, door_panels


def signal_box(
    transform: Transform
) -> PanelGroup:
    length = 73
    width = 43
    height = 54
    gable_height = 18
    roof_overhang_left = 3
    roof_overhang_right = 3
    roof_overhang_bottom = 3
    roof_layer_count = 5

    rafter_0_offset_x = 65
    rafter_1_offset_x = -4
    rafter_2_offset_x = -43

    wall_media = media_v2.CARD_056mm
    base_media = media_v2.CARD_169mm

    wall_base_media = media_v2.CARD_2x169mm
    wall_front_media = wall_media  # media_v2.CARD_2x056mm
    wall_back_media = wall_media
    roof_media = wall_media
    window_media = wall_media

    tab_offset_roof = 2
    tab_length_roof = 10

    signal_box_pg = houses.basic_house(
        name="signal_box",
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
            # Right wall
            {
                "offset_x": 0.5 * length - wall_front_media.thickness - 0.5 * wall_base_media.thickness,
                "offset_y": tab_offset_roof,
                "width": wall_base_media.thickness,
                "height": tab_length_roof
            }
        ],
        roof_vertical_holes=[],
        tab_offset_roof=tab_offset_roof,
        tab_length_roof=tab_length_roof,
        # floor_hole=False,
        tab_length_y=15,
        transform=transform
    )

    front_wall_pg = panels_v2.get_child_panel_group(
        panel_group=signal_box_pg,
        name="front_wall"
    )
    right_wall_pg = panels_v2.get_child_panel_group(
        panel_group=signal_box_pg,
        name="right_wall"
    )
    left_wall_pg = panels_v2.get_child_panel_group(
        panel_group=signal_box_pg,
        name="left_wall"
    )

    # # Door 1 (left)
    # panels_v2.add_child_panel_group(
    #     parent=left_wall_pg,
    #     child=door_panels.door(
    #         base_media=wall_base_media,
    #         media=window_media,
    #         door_width=11,
    #         door_height=30.5,
    #         is_open=True,
    #         transform=[Translate((
    #             0.5 * width - wall_front_media.thickness - wall_base_media.thickness - 0.5 * 11 - 1,
    #             35.75 - 0.5 * height,
    #             0
    #         ))]
    #     )
    # )

    # # Left window set
    # panels_v2.add_child_panel_group(
    #     parent=left_wall_pg,
    #     child=window_panels.signal_box_left_window_set(
    #         base_media=wall_base_media,
    #         media=window_media,
    #         window_width=31,
    #         window_height=24,
    #         sill_width=31 + 1,
    #         sill_height=1,
    #         sill_offset=0.5,
    #         window_margin=2,
    #         transform=[Translate((
    #             -0.5 * width + 0.5 * 31,
    #             39 - 0.5 * height,
    #             0
    #         ))]
    #     )
    # )

    # Right window set
    # TO DO:
    # - Better to recalculate everything by hand to ensure that it
    #   is exactly correct!
    # - It looks like the side window frame thickness is different
    # - The side window pane size might be different too (surely not!?)
    panels_v2.add_child_panel_group(
        parent=right_wall_pg,
        child=window_panels.signal_box_right_window_set(
            base_media=wall_base_media,
            media=window_media,
            front_window_width=length - 2 * window_media.thickness,
            window_height=21,
            # sill_width=length + 2 * wall_front_media.thickness,
            sill_height=1,
            window_margin=2,
            transform=[Translate((
                -14.85 - 0.56,
                0.5 * height - 10.5 - 3,
                0
            ))]
        )
    )

    # Front window set
    panels_v2.add_child_panel_group(
        parent=front_wall_pg,
        child=window_panels.signal_box_front_window_set(
            base_media=wall_base_media,
            media=window_media,
            window_width=length - 2 * window_media.thickness,
            window_height=21,
            sill_width=length + 2 * wall_front_media.thickness,
            sill_height=1,
            window_margin=2,
            transform=[Translate((0, 0.5 * height - 10.5 - 3, 0))]
        )
    )

    return signal_box_pg
