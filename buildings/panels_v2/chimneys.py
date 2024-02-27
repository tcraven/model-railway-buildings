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
    transform: Transform
) -> PanelGroup:
    
    panels = []
    z = 0

    # Layer 0
    for i in range(2):
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
    for i in range(3):  # 4
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
    for i in range(1):  # 1
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
    for i in range(1):  # 1
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
