from cadquery import Workplane
from buildings import panels_v2
from buildings.media_v2 import Media
from buildings.panels_v2 import Cutout, Panel, PanelGroup
from buildings.panels_v2 import window_panels
from buildings.transforms_v2 import Transform, Translate, Rotate
from buildings.tabs import Tab, TabDirection


def wall_with_windows(
    base_media: Media,
    front_media: Media,
    back_media: Media,
    window_media: Media,
    transform: Transform
) -> PanelGroup:
    wall0 = basic_wall(
        base_media=base_media,
        front_media=front_media,
        back_media=back_media,
        transform=transform
    )

    window1 = window_panels.window(
        base_media=base_media,
        media=window_media,
        transform=[Translate((-20, 0, 0))]
    )
    window2 = window_panels.window(
        base_media=base_media,
        media=window_media,
        transform=[
            Translate((20, 0, 0))
        ]
    )

    panels_v2.add_child_panel_group(parent=wall0, child=window1)
    panels_v2.add_child_panel_group(parent=wall0, child=window2)

    return wall0


def basic_wall(
    base_media: Media,
    front_media: Media,
    back_media: Media,
    transform: Transform
) -> PanelGroup:
    base = Panel(
        name="base_wall",
        media=base_media,
        workplane=panels_v2.basic_rect(
            width=90,
            height=50,
            thickness=base_media.thickness
        )
    )
    front = Panel(
        name="front_wall",
        media=front_media,
        workplane=panels_v2.basic_rect(
            width=90,
            height=50,
            thickness=front_media.thickness
        ),
        transform=[Translate((0, 0, base_media.thickness))]
    )
    back = Panel(
        name="back_wall",
        media=back_media,
        workplane=panels_v2.basic_rect(
            width=90,
            height=50,
            thickness=back_media.thickness
        ),
        transform=[Translate((0, 0, -back_media.thickness))]
    )
    return PanelGroup(
        name="wall",
        panels=[base, front, back],
        transform=transform
    )


def floor(
    wall_base_media: Media,
    wall_front_media: Media,
    wall_back_media: Media,
    width: float,
    height: float,
    transform: Transform,
    name: str = "floor"
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
                width=30,
                height=wall_base_media.thickness,
                thickness=wall_base_media.thickness
            ),
            tab_right=Tab(
                direction=TabDirection.OUT,
                width=30,
                height=wall_base_media.thickness,
                thickness=wall_base_media.thickness
            ),
            tab_bottom=Tab(
                direction=TabDirection.OUT,
                width=30,
                height=wall_base_media.thickness,
                thickness=wall_base_media.thickness
            ),
            tab_top=Tab(
                direction=TabDirection.OUT,
                width=30,
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
    floor_hole = PanelGroup(
        name="floor_hole",
        cutouts=[
            Cutout(
                subtract_from=["base_floor", "inside_floor"],
                workplane=chamfered_hole(
                    width=width - 2 * wall_front_media.thickness - 20,
                    height=height - 2 * wall_front_media.thickness - 20
                )
            )
        ]
    )

    panels_v2.add_child_panel_group(parent=floor, child=floor_hole)
    
    return floor


def chamfered_hole(width: float, height: float) -> Workplane:
    return (
        Workplane("XY")
        .sketch()
        .rect(width, height)
        .vertices()
        .chamfer(5)
        .finalize()
        .extrude(100)
    )


def wall(
    wall_base_media: Media,
    wall_front_media: Media,
    wall_back_media: Media,
    width: float,
    height: float,
    left_right_tab_direction: str,
    transform: Transform,
    name: str = "wall"
) -> PanelGroup:
    if left_right_tab_direction == TabDirection.IN:
        base_wall_width = width - 2 * wall_front_media.thickness
    else:
        base_wall_width = width - 2 * (wall_front_media.thickness + wall_base_media.thickness)

    base_wall = Panel(
        name="base_wall",
        media=wall_base_media,
        workplane=panels_v2.rect(
            width=base_wall_width,
            height=height,
            thickness=wall_base_media.thickness,
            tab_left=Tab(
                direction=left_right_tab_direction,
                width=30,
                height=wall_base_media.thickness,
                thickness=wall_base_media.thickness
            ),
            tab_right=Tab(
                direction=left_right_tab_direction,
                width=30,
                height=wall_base_media.thickness,
                thickness=wall_base_media.thickness
            ),
            tab_bottom=Tab(
                direction=TabDirection.IN,
                width=30,
                height=wall_base_media.thickness,
                thickness=wall_base_media.thickness
            ),
            tab_top=Tab(
                direction=TabDirection.IN,
                width=30,
                height=wall_base_media.thickness,
                thickness=wall_base_media.thickness
            )
        )
    )
    if left_right_tab_direction == TabDirection.IN:
        inside_wall_width = base_wall_width - 2 * (wall_base_media.thickness + 0.25)
    else:
        inside_wall_width = base_wall_width - 2 * (wall_back_media.thickness + 0.25)

    inside_wall = Panel(
        name="inside_wall",
        media=wall_back_media,
        workplane=panels_v2.basic_rect(
            width=inside_wall_width,
            height=height - 2 * (wall_base_media.thickness + 0.25),
            thickness=wall_back_media.thickness
        ),
        transform=[Translate((0, 0, -wall_back_media.thickness))]
    )
    
    if left_right_tab_direction == TabDirection.IN:
        outside_wall_width = width
    else:
        outside_wall_width = width - 2 * wall_front_media.thickness

    outside_wall = Panel(
        name="outside_wall",
        media=wall_front_media,
        workplane=panels_v2.basic_rect(
            width=outside_wall_width,
            height=height,
            thickness=wall_front_media.thickness
        ),
        transform=[Translate((0, 0, wall_base_media.thickness))]
    )
    wall = PanelGroup(
        name=name,
        panels=[base_wall, outside_wall, inside_wall],
        transform=transform
    )
    return wall
