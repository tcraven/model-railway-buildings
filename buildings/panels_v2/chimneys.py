import math
from buildings import panels_v2
from buildings.media_v2 import Media
from buildings.panels_v2 import Cutout, Panel, PanelGroup
from buildings.tabs import Tab, TabDirection
from buildings.transforms_v2 import Transform, Translate, Rotate

# Extra clearance distance for each edge of holes to ensure that
# pieces fit together easily after being cut out
HOLE_CLEARANCE = 0.025


def four_walls(
    wall_media: Media,
    inside_width: float,
    inside_depth: float,
    height: float,
    transform: Transform,
    skip_back_wall: bool = False
) -> PanelGroup:
    
    depth = inside_depth + 2 * wall_media.thickness

    panels = []

    # Right wall
    panels.append(
        Panel(
            name="right_wall",
            media=wall_media,
            workplane=panels_v2.basic_rect(
                width=depth,
                height=height,
                thickness=wall_media.thickness
            ),
            transform=[
                Rotate((0, 0, 0), (0, 1, 0), 90),
                Translate((0.5 * inside_width, 0, 0.5 * depth))
            ]  # .extend(transform)
        )
    )

    # Left wall
    panels.append(
        Panel(
            name="left_wall",
            media=wall_media,
            workplane=panels_v2.basic_rect(
                width=depth,
                height=height,
                thickness=wall_media.thickness
            ),
            transform=[
                Rotate((0, 0, 0), (0, 1, 0), -90),
                Translate((-0.5 * inside_width, 0, 0.5 * depth))
            ]  # .extend(transform)
        )
    )

    # Back wall
    if not skip_back_wall:
        panels.append(
            Panel(
                name="back_wall",
                media=wall_media,
                workplane=panels_v2.basic_rect(
                    width=inside_width,
                    height=height,
                    thickness=wall_media.thickness
                ),
                transform=[Translate((0, 0, 0))]  # .extend(transform)
            )
        )
    
    # Front wall
    panels.append(
        Panel(
            name="front_wall",
            media=wall_media,
            workplane=panels_v2.basic_rect(
                width=inside_width,
                height=height,
                thickness=wall_media.thickness
            ),
            transform=[Translate((0, 0, depth - wall_media.thickness))]  # .extend(transform)
        )
    )

    return PanelGroup(
        name="four_walls",
        panels=panels,
        transform=transform
    )


def core(
    base_media: Media,
    wall_media: Media,
    core_width: float,
    base_layer_count: int,
    wall_layer_count: int,
    height: float,
    top_height: float,
    top_hole_width: float,
    transform: Transform,
    skip_first_two_layers: bool = False
) -> PanelGroup:
    
    panels = []
    z = 0

    top_hole_height = base_media.thickness
    top_hole_offset_y = 0.5 * (
        wall_layer_count * wall_media.thickness +
        (base_layer_count - 3) * base_media.thickness
    )
    
    # Chimney core base layers
    for i in range(base_layer_count):
        if i == 1:
            tab_top = Tab(
                direction=TabDirection.OUT,
                width=top_hole_width,
                height=top_height - 2 * HOLE_CLEARANCE,
                thickness=base_media.thickness
            )
        else:
            tab_top = None

        if (not skip_first_two_layers or i >= 2):
            panels.append(
                Panel(
                    name=f"core_base_layer_{i}",
                    media=base_media,
                    workplane=panels_v2.rect(
                        width=core_width,
                        height=height,
                        thickness=base_media.thickness,
                        tab_left=None,
                        tab_right=None,
                        tab_bottom=None,
                        tab_top=tab_top
                    ),
                    transform=[Translate((0, 0, z))]
                )
            )

        z += base_media.thickness
    
    # Chimney core wall layers
    for i in range(wall_layer_count):
        panels.append(
            Panel(
                name=f"core_wall_layer_{i}",
                media=wall_media,
                workplane=panels_v2.basic_rect(
                    width=core_width,
                    height=height,
                    thickness=wall_media.thickness
                ),
                transform=[Translate((0, 0, z))]
            )
        )
        z += wall_media.thickness
    
    pg = PanelGroup(
        name="core",
        panels=panels,
        transform=transform
    )
    return pg, top_hole_height, top_hole_offset_y


def top(
    wall_media: Media,
    chimney_width: float,
    chimney_depth: float,
    hole_width: float,
    hole_height: float,
    hole_offset_x: float,
    hole_offset_y: float,
    transform: Transform,
    layer_0_count: int = 2,
    layer_1_count: int = 3,
    layer_2_count: int = 1,
    layer_3_count: int = 1
) -> PanelGroup:
    
    panels = []
    z = 0

    # Layer 0
    for i in range(layer_0_count):
        panels.append(
            Panel(
                name=f"top_0_{i}",
                media=wall_media,
                workplane=panels_v2.basic_rect_with_hole(
                    width=chimney_width + 1,
                    height=chimney_depth + 1,
                    thickness=wall_media.thickness,
                    hole_width=hole_width,
                    hole_height=hole_height,
                    hole_offset_x=hole_offset_x,
                    hole_offset_y=hole_offset_y
                ),
                transform=[Translate((0, 0, z))]
            )
        )
        z += wall_media.thickness
    
    # Layer 1
    for i in range(layer_1_count):  # 4
        panels.append(
            Panel(
                name=f"top_1_{i}",
                media=wall_media,
                workplane=panels_v2.basic_rect_with_hole(
                    width=chimney_width + 3,
                    height=chimney_depth + 3,
                    thickness=wall_media.thickness,
                    hole_width=hole_width,
                    hole_height=hole_height,
                    hole_offset_x=hole_offset_x,
                    hole_offset_y=hole_offset_y
                ),
                transform=[Translate((0, 0, z))]
            )
        )
        z += wall_media.thickness
    
    # Layer 2
    for i in range(layer_2_count):  # 1
        panels.append(
            Panel(
                name=f"top_2_{i}",
                media=wall_media,
                workplane=panels_v2.basic_rect_with_hole(
                    width=chimney_width + 1,
                    height=chimney_depth + 1,
                    thickness=wall_media.thickness,
                    hole_width=hole_width,
                    hole_height=hole_height,
                    hole_offset_x=hole_offset_x,
                    hole_offset_y=hole_offset_y
                ),
                transform=[Translate((0, 0, z))]
            )
        )
        z += wall_media.thickness
    
    # Layer 3
    for i in range(layer_3_count):  # 1
        panels.append(
            Panel(
                name=f"top_3_{i}",
                media=wall_media,
                workplane=panels_v2.basic_rect_with_hole(
                    width=chimney_width,
                    height=chimney_depth,
                    thickness=wall_media.thickness,
                    hole_width=hole_width,
                    hole_height=hole_height,
                    hole_offset_x=hole_offset_x,
                    hole_offset_y=hole_offset_y
                ),
                transform=[Translate((0, 0, z))]
            )
        )
        z += wall_media.thickness
    
    return PanelGroup(
        name="top",
        panels=panels,
        transform=transform
    )


def chimney(
    base_media: Media,  # Single layer 1.69
    wall_media: Media,  # Single layer 0.56
    chimney_width: float,
    core_base_layer_count: int,
    core_wall_layer_count: int,
    shaft_height: float,
    shaft_base_height: float,
    transform: Transform
) -> PanelGroup:

    # Chimney is laying flat on the xy plane, shaft runs in y-direction

    # chimney_width = 9
    # core_base_layer_count = 3
    # core_wall_layer_count = 0
    # shaft_height = 17
    # shaft_base_height = 10

    inside_width = chimney_width - 2 * wall_media.thickness
    inside_depth = \
        core_wall_layer_count * wall_media.thickness + \
        core_base_layer_count * base_media.thickness
    chimney_depth = inside_depth + 2 * wall_media.thickness
    chimney_base_depth = chimney_depth + 2 * wall_media.thickness

    panels = []
    y = 0.5 * shaft_height
    z = 2 * wall_media.thickness
    core_width = chimney_width - 2 * wall_media.thickness
    top_height = 7 * wall_media.thickness
    top_hole_width = 4

    # Chimney walls
    walls_pg = four_walls(
        wall_media=wall_media,
        inside_width=inside_width,
        inside_depth=inside_depth,
        height=shaft_height,
        transform=[Translate((0, 0.5 * shaft_height, wall_media.thickness))]
    )

    # Chimney base walls
    base_walls_pg = four_walls(
        wall_media=wall_media,
        inside_width=chimney_width,
        inside_depth=chimney_depth,
        height=shaft_base_height,
        transform=[Translate((0, 0.5 * shaft_base_height, 0))]
    )

    # Chimney core
    core_pg, top_hole_height, top_hole_offset_y = core(
        base_media=base_media,
        wall_media=wall_media,
        core_width=core_width,
        base_layer_count=core_base_layer_count,
        wall_layer_count=core_wall_layer_count,
        height=shaft_height,
        top_height=top_height,
        top_hole_width=top_hole_width,
        transform=[Translate((0, 0.5 * shaft_height, 2 * wall_media.thickness))]
    )

    # Chimney top slabs
    top_pg = top(
        wall_media=wall_media,
        chimney_width=chimney_width,
        chimney_depth=chimney_depth,
        hole_width=top_hole_width + 2 * HOLE_CLEARANCE,
        hole_height=top_hole_height + 2 * HOLE_CLEARANCE,
        hole_offset_x=0,
        hole_offset_y=top_hole_offset_y,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), -90),
            Translate((0, shaft_height, 0.5 * chimney_base_depth))
        ]
    )

    return PanelGroup(
        name="chimney",
        panels=panels,
        children=[core_pg, walls_pg, base_walls_pg, top_pg],
        transform=transform
    )


def chimney_for_gable_wall(
    base_media: Media,  # Single layer 1.69
    wall_media: Media,  # Single layer 0.56
    chimney_width: float,
    core_base_layer_count: int,
    core_wall_layer_count: int,
    shaft_height: float,
    shaft_base_height: float,
    transform: Transform
) -> PanelGroup:

    # Chimney is laying flat on the xy plane, shaft runs in y-direction

    # chimney_width = 9
    # core_base_layer_count = 3
    # core_wall_layer_count = 0
    # shaft_height = 17
    # shaft_base_height = 10

    inside_width = chimney_width - 2 * wall_media.thickness
    inside_depth = \
        core_wall_layer_count * wall_media.thickness + \
        core_base_layer_count * base_media.thickness
    chimney_depth = inside_depth + 2 * wall_media.thickness
    chimney_base_depth = chimney_depth + 2 * wall_media.thickness

    panels = []
    y = 0.5 * shaft_height
    z = 2 * wall_media.thickness
    core_width = chimney_width - 2 * wall_media.thickness
    top_height = 7 * wall_media.thickness
    top_hole_width = 4

    # Chimney walls
    walls_pg = four_walls(
        wall_media=wall_media,
        inside_width=inside_width,
        inside_depth=inside_depth,
        height=shaft_height,
        transform=[Translate((0, 0.5 * shaft_height, wall_media.thickness))],
        skip_back_wall=True
    )

    # Chimney base walls
    base_walls_pg = four_walls(
        wall_media=wall_media,
        inside_width=chimney_width,
        inside_depth=chimney_depth,
        height=shaft_base_height,
        transform=[Translate((0, 0.5 * shaft_base_height, 0))],
        skip_back_wall=True
    )

    # Chimney core
    core_pg, top_hole_height, top_hole_offset_y = core(
        base_media=base_media,
        wall_media=wall_media,
        core_width=core_width,
        base_layer_count=core_base_layer_count,
        wall_layer_count=core_wall_layer_count,
        height=shaft_height,
        top_height=top_height,
        top_hole_width=top_hole_width,
        transform=[Translate((0, 0.5 * shaft_height, 2 * wall_media.thickness))],
        skip_first_two_layers=True
    )

    # Chimney top slabs
    top_pg = top(
        wall_media=wall_media,
        chimney_width=chimney_width,
        chimney_depth=chimney_depth,
        hole_width=top_hole_width + 2 * HOLE_CLEARANCE,
        hole_height=top_hole_height + 2 * HOLE_CLEARANCE,
        hole_offset_x=0,
        hole_offset_y=top_hole_offset_y,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), -90),
            Translate((0, shaft_height, 0.5 * chimney_base_depth))
        ]
    )

    return PanelGroup(
        name="chimney",
        panels=panels,
        children=[
            core_pg,
            walls_pg,
            base_walls_pg,
            top_pg
        ],
        transform=transform
    )


def _external_core(
    base_media: Media,  # Single layer 1.69
    wall_media: Media,  # Single layer 0.56
    chimney_width: float,
    core_base_layer_count: int,
    core_wall_layer_count: int,
    shaft_height: float,
    shaft_middle_height,
    shaft_base_height: float,
    shaft_base_width: float,
    tab_width: float,
    tab_height: float,
    transform: Transform
) -> PanelGroup:
    panels = []

    z = 0
    panels.append(
        Panel(
            name=f"core_inside_wall",
            media=wall_media,
            workplane=panels_v2.external_chimney_shape(
                width=shaft_base_width,
                height=shaft_height,
                top_width=chimney_width,
                base_height=shaft_base_height,
                middle_height=shaft_middle_height,
                shrink_delta=0,
                thickness=wall_media.thickness
            ),
            transform=[Translate((0, 0, z))]
        )
    )
    z += wall_media.thickness

    for i in range(core_base_layer_count):
        wp = panels_v2.external_chimney_shape(
            width=shaft_base_width,
            height=shaft_height,
            top_width=chimney_width,
            base_height=shaft_base_height,
            middle_height=shaft_middle_height,
            shrink_delta=wall_media.thickness,
            thickness=base_media.thickness
        )
        if i == 1:
            wp += (
                panels_v2.basic_rect(
                    width=tab_width,
                    height=2 * tab_height,
                    thickness=base_media.thickness
                )
                .translate((0, shaft_height, 0))
            )

        panels.append(
            Panel(
                name=f"core_base_{i}",
                media=base_media,
                workplane=wp,
                transform=[Translate((0, 0, z))]
            )
        )
        z += base_media.thickness
    
    for i in range(core_wall_layer_count):
        panels.append(
            Panel(
                name=f"core_wall_{i}",
                media=wall_media,
                workplane=panels_v2.external_chimney_shape(
                    width=shaft_base_width,
                    height=shaft_height,
                    top_width=chimney_width,
                    base_height=shaft_base_height,
                    middle_height=shaft_middle_height,
                    shrink_delta=wall_media.thickness,
                    thickness=wall_media.thickness
                ),
                transform=[Translate((0, 0, z))]
            )
        )
        z += wall_media.thickness
    
    panels.append(
        Panel(
            name=f"core_outside_wall",
            media=wall_media,
            workplane=panels_v2.external_chimney_shape(
                width=shaft_base_width,
                height=shaft_height,
                top_width=chimney_width,
                base_height=shaft_base_height,
                middle_height=shaft_middle_height,
                shrink_delta=0,
                thickness=wall_media.thickness
            ),
            transform=[Translate((0, 0, z))]
        )
    )

    # Side walls for chimney
    core_depth = (
        core_base_layer_count * base_media.thickness +
        core_wall_layer_count * wall_media.thickness
    )
    chimney_depth = core_depth + 2 * wall_media.thickness
    top_height = shaft_height - shaft_middle_height - shaft_base_height
    top_wall_x = 0.5 * chimney_width - wall_media.thickness
    top_wall_y = shaft_height - 0.5 * top_height
    bottom_wall_x = 0.5 * shaft_base_width - wall_media.thickness
    bottom_wall_y = 0.5 * shaft_base_height
    middle_wall_x = 0.5 * chimney_width + 0.25 * (shaft_base_width - chimney_width)
    middle_wall_y = shaft_base_height + 0.5 * shaft_middle_height
    middle_width = 0.5 * (shaft_base_width - chimney_width)
    middle_wall_a = math.atan2(shaft_middle_height, middle_width) * 180 / math.pi
    middle_wall_length = (
        math.sqrt(
            shaft_middle_height * shaft_middle_height +
            middle_width * middle_width)
        - 0.5
    )
    middle_wall_offset = 0.2
    wall_z = 0.5 * chimney_depth

    top_side_wp = panels_v2.basic_rect(
        width=core_depth,
        height=top_height,
        thickness=wall_media.thickness
    )
    bottom_side_wp = panels_v2.basic_rect(
        width=core_depth,
        height=shaft_base_height,
        thickness=wall_media.thickness
    )
    middle_side_wp = panels_v2.basic_rect(
        width=core_depth,
        height=middle_wall_length,
        thickness=wall_media.thickness
    )

    panels.extend([
        Panel(
            name=f"core_top_side_wall_left",
            media=wall_media,
            workplane=top_side_wp,
            transform=[
                Rotate((0, 0, 0), (0, 1, 0), -90),
                Translate((
                    -top_wall_x,
                    top_wall_y,
                    wall_z
                ))
            ]
        ),
        Panel(
            name=f"core_top_side_wall_right",
            media=wall_media,
            workplane=top_side_wp,
            transform=[
                Rotate((0, 0, 0), (0, 1, 0), 90),
                Translate((
                    top_wall_x,
                    top_wall_y,
                    wall_z
                ))
            ]
        ),
        Panel(
            name=f"core_bottom_side_wall_left",
            media=wall_media,
            workplane=bottom_side_wp,
            transform=[
                Rotate((0, 0, 0), (0, 1, 0), -90),
                Translate((
                    -bottom_wall_x,
                    bottom_wall_y,
                    wall_z
                ))
            ]
        ),
        Panel(
            name=f"core_bottom_side_wall_right",
            media=wall_media,
            workplane=bottom_side_wp,
            transform=[
                Rotate((0, 0, 0), (0, 1, 0), 90),
                Translate((
                    bottom_wall_x,
                    bottom_wall_y,
                    wall_z
                ))
            ]
        ),
        Panel(
            name=f"core_middle_side_wall_left",
            media=wall_media,
            workplane=middle_side_wp,
            transform=[
                Translate((0, -middle_wall_offset, 0)),
                Rotate((0, 0, 0), (0, 1, 0), -90),
                Rotate((0, 0, 0), (0, 0, 1), 180 - middle_wall_a),
                Translate((
                    -middle_wall_x,
                    middle_wall_y,
                    wall_z
                ))
            ]
        ),
        Panel(
            name=f"core_middle_side_wall_right",
            media=wall_media,
            workplane=middle_side_wp,
            transform=[
                Translate((0, middle_wall_offset, 0)),
                Rotate((0, 0, 0), (0, 1, 0), -90),
                Rotate((0, 0, 0), (0, 0, 1), middle_wall_a),
                Translate((
                    middle_wall_x,
                    middle_wall_y,
                    wall_z
                ))
            ]
        )
    ])

    return PanelGroup(
        name="external_core",
        panels=panels,
        transform=transform
    )


def external_chimney(
    base_media: Media,  # Single layer 1.69
    wall_media: Media,  # Single layer 0.56
    chimney_width: float,
    core_base_layer_count: int,
    core_wall_layer_count: int,
    shaft_height: float,
    shaft_middle_height,
    shaft_base_height: float,
    shaft_base_width: float,
    wall_offset: float,
    transform: Transform
) -> PanelGroup:
    
    top_tab_width = 4
    top_tab_height = 7 * wall_media.thickness
    
    chimney_depth = (
        core_base_layer_count * base_media.thickness +
        (core_wall_layer_count + 2) * wall_media.thickness
    )
    
    core_pg = _external_core(
        base_media=base_media,
        wall_media=wall_media,
        chimney_width=chimney_width,
        core_base_layer_count=core_base_layer_count,
        core_wall_layer_count=core_wall_layer_count,
        shaft_height=shaft_height,
        shaft_middle_height=shaft_middle_height,
        shaft_base_height=shaft_base_height,
        shaft_base_width=shaft_base_width,
        tab_width=top_tab_width,
        tab_height=top_tab_height,
        transform=[Translate((0, 0, wall_offset))]
    )

    top_pg = top(
        wall_media=wall_media,
        chimney_width=chimney_width,
        chimney_depth=chimney_depth,
        hole_width=top_tab_width + 2 * HOLE_CLEARANCE,
        hole_height=base_media.thickness + 2 * HOLE_CLEARANCE,
        hole_offset_x=0,
        hole_offset_y=0.5 * chimney_depth - (wall_media.thickness + 1.5 * base_media.thickness),
        layer_0_count=1,
        layer_1_count=2,
        layer_2_count=0,
        layer_3_count=4,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), -90),
            Translate((0, shaft_height, 0.5 * chimney_depth + wall_offset))
        ]
    )

    hole_cu = Cutout(
        transform=[
            Translate((0, 0, -50))
        ],
        subtract_from=["outside_wall"],
        workplane=panels_v2.external_chimney_shape(
            width=shaft_base_width,
            height=shaft_height,
            top_width=chimney_width,
            base_height=shaft_base_height,
            middle_height=shaft_middle_height,
            shrink_delta=-0.1,
            thickness=100
        )
    )

    return PanelGroup(
        name="external_chimney",
        cutouts=[hole_cu],
        children=[core_pg, top_pg],
        transform=transform
    )
