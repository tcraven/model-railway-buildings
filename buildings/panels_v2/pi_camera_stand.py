import math
from typing import Optional
from cadquery import Workplane
from buildings import panels_v2
from buildings.media_v2 import Media
from buildings.panels_v2 import Cutout, Panel, PanelGroup
from buildings.tabs import Tab, TabDirection
from buildings.transforms_v2 import Transform, Translate, Rotate


def pi_camera_stand(media: Media) -> PanelGroup:
    width = 69
    height = 62
    horizontal_tab_offset = 0.5 * (width - 20) - 10 - media.thickness
    
    base_1_width = 30
    base_1_height = 56
    base_1_tab_height = 3
    base_1_x_offset = 3
    base_1_tab_width = 25

    base_1_x = 0.5 * (width - base_1_width) - base_1_tab_height - base_1_x_offset

    base_1 = PanelGroup(
        name="base_1",
        panels=[
            Panel(
                name="base_1",
                media=media,
                workplane=panels_v2.rect(
                    width=base_1_width,
                    height=base_1_height,
                    thickness=media.thickness,
                    tab_left=None,
                    tab_right=Tab(
                        direction=TabDirection.OUT,
                        width=base_1_tab_width,
                        height=base_1_tab_height,
                        thickness=media.thickness
                    ),
                    tab_bottom=None,
                    tab_top=None
                )
            )            
        ],
        transform=[Translate((
            base_1_x,
            0,
            0
        ))]
    )

    base_1_hole = PanelGroup(
        name="base1_hole",
        cutouts=[
            Cutout(
                subtract_from=["base_1"],
                workplane=panels_v2.chamfered_hole(
                    width=width - 2 * (media.thickness + 5),
                    height=height - 2 * (media.thickness + 5)
                )
            )
        ],
        transform=[
            Translate((
                -base_1_x,
                0,
                0
            ))
        ]
    )

    panels_v2.add_child_panel_group(parent=base_1, child=base_1_hole)

    base_2 = PanelGroup(
        name="base_2",
        panels=[
            Panel(
                name="base_2",
                media=media,
                workplane=panels_v2.rect(
                    width=width,
                    height=height,
                    thickness=media.thickness,
                    tab_left=None,
                    tab_right=Tab(
                        direction=TabDirection.IN,
                        width=20,
                        height=media.thickness,
                        thickness=media.thickness
                    ),
                    tab_bottom=Tab(
                        direction=TabDirection.IN,
                        width=20,
                        offset=horizontal_tab_offset,
                        height=media.thickness,
                        thickness=media.thickness
                    ),
                    tab_top=Tab(
                        direction=TabDirection.IN,
                        width=20,
                        offset=-horizontal_tab_offset,
                        height=media.thickness,
                        thickness=media.thickness
                    )
                )
            )            
        ],
        transform=[Translate((0, 0, media.thickness))]
    )

    base_2_hole = PanelGroup(
        name="base2_hole",
        cutouts=[
            Cutout(
                subtract_from=["base_2"],
                workplane=panels_v2.chamfered_hole(
                    width=width - 2 * (media.thickness + 5),
                    height=height - 2 * (media.thickness + 5)
                )
            )
        ]
    )

    hole_2_x = 15
    hole_2_y = -5
    hole_2_width = 9
    hole_2_height = 20

    base_2_hole_2 = PanelGroup(
        name="base_2_hole_2",
        cutouts=[
            Cutout(
                subtract_from=["base_2"],
                workplane=panels_v2.chamfered_hole(
                    width=hole_2_width,
                    height=hole_2_height,
                    chamfer=2
                )
            )
        ],
        transform=[
            Translate((
                -0.5 * width + 0.5 * hole_2_width + hole_2_x,
                0.5 * height - 0.5 * hole_2_height + hole_2_y,
                0
            ))
        ]
    )

    panels_v2.add_child_panel_group(parent=base_2, child=base_2_hole)
    panels_v2.add_child_panel_group(parent=base_2, child=base_2_hole_2)

    tco_x, tco_y = trangle_center_offset(length=40, angle=75)

    front_bracket = bracket(
        name="front_bracket",
        media=media,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), 90),
            Translate((
                tco_x - 20 + horizontal_tab_offset,
                0.5 * 62,
                tco_y + 2 * media.thickness
            ))
        ]
    )

    back_bracket = bracket(
        name="back_bracket",
        media=media,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), 90),
            Translate((
                tco_x - 20 + horizontal_tab_offset,
                -0.5 * 62 + media.thickness,
                tco_y + 2 * media.thickness
            ))
        ]
    )

    # Right
    camera_panel = PanelGroup(
        name="camera_panel",
        panels=[
            Panel(
                name="camera_panel",
                media=media,
                workplane=panels_v2.rect(
                    width=62,
                    height=40,
                    thickness=media.thickness,
                    tab_left=Tab(
                        direction=TabDirection.IN,
                        width=20,
                        height=media.thickness,
                        thickness=media.thickness
                    ),
                    tab_right=Tab(
                        direction=TabDirection.IN,
                        width=20,
                        height=media.thickness,
                        thickness=media.thickness
                    ),
                    tab_bottom=Tab(
                        direction=TabDirection.OUT,
                        width=20,
                        height=media.thickness,
                        thickness=media.thickness
                    ),
                    tab_top=None
                )
            )
        ],
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), 75),
            Rotate((0, 0, 0), (0, 0, 1), 90),
            Translate((
                -0.5 * 40 * math.cos(math.radians(75)) + 0.5 * width - media.thickness,
                0,
                0.5 * 40 * math.sin(math.radians(75)) + 2 * media.thickness
            ))
        ]
    )

    camera_panel_hole = PanelGroup(
        name="camera_panel_hole",
        cutouts=[
            Cutout(
                subtract_from=["camera_panel"],
                workplane=circle(
                    radius=7,
                    thickness=30
                )
            )
        ],
        transform=[Translate((0, 5, -15))]
    )

    panels_v2.add_child_panel_group(parent=camera_panel, child=camera_panel_hole)

    pi_camera_stand = PanelGroup(
        name="pi_camera_stand",
        children=[
            base_1,
            base_2,
            front_bracket,
            back_bracket,
            camera_panel
        ]
    )

    return pi_camera_stand


def bracket(name: str, media: Media, transform: Transform) -> PanelGroup:
    bracket = PanelGroup(
        name=name,
        panels=[
            Panel(
                name="bracket",
                media=media,
                workplane=triangle_with_tabs(
                    length=40,
                    angle=75,
                    thickness=media.thickness,
                    tab_bottom=Tab(
                        direction=TabDirection.OUT,
                        width=20,
                        height=media.thickness,
                        thickness=media.thickness
                    ),
                    tab_right=Tab(
                        direction=TabDirection.OUT,
                        width=20,
                        height=media.thickness,
                        thickness=media.thickness
                    ),
                    tab_left=None
                )
            )
        ],
        transform=transform
    )

    bracket_hole = PanelGroup(
        name="bracket_hole",
        cutouts=[
            Cutout(
                subtract_from=["bracket"],
                workplane=triangle(
                    length=20,
                    angle=75,
                    thickness=30
                )
            )
        ],
        transform=[Translate((0, 0, -15))]
    )

    panels_v2.add_child_panel_group(parent=bracket, child=bracket_hole)

    return bracket


def trangle_center_offset(length: float, angle: float) -> tuple:
    x0 = (0, 0)
    x1 = (length, 0)
    x2 = (
        length * (1 - math.cos(math.radians(angle))),
        length * math.sin(math.radians(angle))
    )
    x3 = (
        length * math.cos(math.radians(angle)),
        length * math.sin(math.radians(angle))
    )
    return (
        (x0[0] + x1[0] + x2[0] + x3[0]) / 4,
        (x0[1] + x1[1] + x2[1] + x3[1]) / 4
    )


def triangle(length: float, angle: float, thickness: float) -> Workplane:
    """
    Creates a triangle workplane with horizontal bottom edge, angle in the
    right vertex, with bottom and right edges having length.
    """
    x0 = (0, 0)
    x1 = (length, 0)
    x2 = (
        length * (1 - math.cos(math.radians(angle))),
        length * math.sin(math.radians(angle))
    )
    x3 = (
        length * math.cos(math.radians(angle)),
        length * math.sin(math.radians(angle))
    )
    cx = (x0[0] + x1[0] + x2[0] + x3[0]) / 4
    cy = (x0[1] + x1[1] + x2[1] + x3[1]) / 4
    xx0 = (x0[0] - cx, x0[1] - cy)
    xx1 = (x1[0] - cx, x1[1] - cy)
    xx2 = (x2[0] - cx, x2[1] - cy)
    xx3 = (x3[0] - cx, x3[1] - cy)
    return (
        Workplane("XY")
        .sketch()
        .polygon(
            [xx0, xx1, xx2, xx3],
            mode="a"
        )
        .finalize()
        .extrude(thickness)
    )


def triangle_with_tabs(
    length: float,
    angle: float,
    thickness: float,
    tab_bottom: Optional[Tab] = None,
    tab_right: Optional[Tab] = None,
    tab_left: Optional[Tab] = None
) -> Workplane:
    tri_wp = triangle(
        length=length,
        angle=angle,
        thickness=thickness)
    
    tri_with_tabs = panels_v2._add_tabs(
        panel_workplane=tri_wp,
        tabs_dict={
            0: tab_bottom, 1: tab_right, 2: None, 3: tab_left
        }
    )

    return tri_with_tabs


def circle(radius: float, thickness: float) -> Workplane:
    return (
        Workplane("XY")
        # .circle(radius)
        .polygon(32, 2 * radius)
        .extrude(thickness)
    )
