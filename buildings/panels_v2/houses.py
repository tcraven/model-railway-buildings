import math
from buildings import panels_v2
from buildings.media_v2 import Media
from buildings.panels_v2 import Panel, PanelGroup
from buildings.panels_v2 import roof_panels, wall_panels, floor_panels
from buildings.transforms_v2 import Transform, Translate, Rotate
from buildings.tabs import Tab, TabDirection


def basic_house(
    name: str,
    wall_base_media: Media,
    wall_front_media: Media,
    wall_back_media: Media,
    roof_media: Media,
    length: float,
    width: float,
    height: float,
    gable_height: float,
    transform: Transform,
    roof_tab_holes: list[dict],
    roof_overhang_width: float = 6,
    roof_overhang_left: float = 6,
    roof_overhang_right: float = 6,
    roof_layer_count: int = 5
) -> PanelGroup:

    floor = floor_panels.floor(
        name="floor",
        wall_base_media=wall_base_media,
        wall_front_media=wall_front_media,
        wall_back_media=wall_back_media,
        width=length,
        height=width,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), 180),
            Translate((0, 0, wall_base_media.thickness))
        ]
    )
    front_wall = wall_panels.wall(
        name="front_wall",
        wall_base_media=wall_base_media,
        wall_front_media=wall_front_media,
        wall_back_media=wall_back_media,
        width=length,
        height=height,
        left_right_tab_direction=TabDirection.OUT,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), 90),
            Rotate((0, 0, 0), (0, 0, 1), 180),
            Translate((0, 0.5 * width - wall_base_media.thickness - wall_front_media.thickness, 0.5 * height))
        ]
    )
    back_wall = wall_panels.wall(
        name="back_wall",
        wall_base_media=wall_base_media,
        wall_front_media=wall_front_media,
        wall_back_media=wall_back_media,
        width=length,
        height=height,
        left_right_tab_direction=TabDirection.OUT,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), 90),
            Rotate((0, 0, 0), (0, 0, 1), 0),
            Translate((0, -0.5 * width + wall_base_media.thickness + wall_front_media.thickness, 0.5 * height))
        ]
    )
    right_wall = wall_panels.gable_wall(
        name="right_wall",
        wall_base_media=wall_base_media,
        wall_front_media=wall_front_media,
        wall_back_media=wall_back_media,
        roof_media=roof_media,
        roof_layer_count=roof_layer_count,
        width=width,
        height=height,
        gable_height=gable_height,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), 90),
            Rotate((0, 0, 0), (0, 0, 1), 90),
            Translate((
                0.5 * length - wall_base_media.thickness - wall_front_media.thickness,
                0,
                0.5 * height))
        ]
    )
    left_wall = wall_panels.gable_wall(
        name="left_wall",
        wall_base_media=wall_base_media,
        wall_front_media=wall_front_media,
        wall_back_media=wall_back_media,
        roof_media=roof_media,
        roof_layer_count=roof_layer_count,
        width=width,
        height=height,
        gable_height=gable_height,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), 90),
            Rotate((0, 0, 0), (0, 0, 1), -90),
            Translate((
                -0.5 * length + wall_base_media.thickness + wall_front_media.thickness,
                0,
                0.5 * height
            ))
        ]
    )

    roof_angle = math.atan2(gable_height, 0.5 * width) * 180 / math.pi
    gable_length = math.sqrt(0.25 * width * width + gable_height * gable_height)
    roof_height = gable_length + roof_overhang_width

    back_roof = roof_panels.roof_panel(
        name="back_roof",
        roof_media=roof_media,
        wall_base_media=wall_base_media,
        wall_front_media=wall_front_media,
        house_length=length,
        house_width=width,
        gable_height=gable_height,
        overhang_left=roof_overhang_left,
        overhang_right=roof_overhang_right,
        overhang_width=roof_overhang_width,
        layer_count=roof_layer_count,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), roof_angle),
            Translate((
                0,
                -0.5 * roof_height * math.cos(math.radians(roof_angle)),
                height + gable_height - 0.5 * roof_height * math.sin(math.radians(roof_angle))
            ))
        ],
        tab_holes=roof_tab_holes,
        chimney_holes=[],
        reverse_hole_offsets=False
    )
    front_roof = roof_panels.roof_panel(
        name="front_roof",
        roof_media=roof_media,
        wall_base_media=wall_base_media,
        wall_front_media=wall_front_media,
        house_length=length,
        house_width=width,
        gable_height=gable_height,
        overhang_left=roof_overhang_right,
        overhang_right=roof_overhang_left,
        overhang_width=roof_overhang_width,
        layer_count=roof_layer_count,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), roof_angle),
            Rotate((0, 0, 0), (0, 0, 1), 180),
            Translate((
                0,
                0.5 * roof_height * math.cos(math.radians(roof_angle)),
                height + gable_height - 0.5 * roof_height * math.sin(math.radians(roof_angle))
            ))
        ],
        tab_holes=roof_tab_holes,
        chimney_holes=[],
        reverse_hole_offsets=True
    )
    
    house = PanelGroup(
        name=name,
        children=[
            floor, front_wall, back_wall, right_wall, left_wall,
            back_roof, front_roof
        ],
        transform=transform
    )
    
    return house


def bare_end_house(
    name: str,
    wall_base_media: Media,
    wall_front_media: Media,
    wall_back_media: Media,
    roof_media: Media,
    length: float,
    width: float,
    height: float,
    gable_height: float,
    transform: Transform,
    roof_tab_holes: list[dict],
    roof_overhang_width: float = 6,
    roof_overhang_left: float = 6,
    roof_overhang_right: float = 6,
    roof_layer_count: int = 5,
    roof_end_taper: bool = True,
    tab_length_x: float = 30,
    tab_length_y: float = 30,
    tab_length_z: float = 30,
    tab_length_roof: float = 20,
    tab_offset_roof: float = 5,
    floor_hole: bool = True
) -> PanelGroup:
    
    original_length = length
    length += wall_front_media.thickness
    offset_x = -0.5 * wall_front_media.thickness

    floor = floor_panels.floor(
        name="floor",
        wall_base_media=wall_base_media,
        wall_front_media=wall_front_media,
        wall_back_media=wall_back_media,
        width=length,
        height=width,
        tab_length_x=tab_length_x,
        tab_length_y=tab_length_y,
        hole=floor_hole,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), 180),
            Translate((
                offset_x,
                0,
                wall_base_media.thickness
            ))
        ]
    )

    front_wall = wall_panels.wall(
        name="front_wall",
        wall_base_media=wall_base_media,
        wall_front_media=wall_front_media,
        wall_back_media=wall_back_media,
        width=length,
        height=height,
        left_right_tab_direction=TabDirection.OUT,
        tab_length_x=tab_length_x,
        tab_length_y=tab_length_z,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), 90),
            Rotate((0, 0, 0), (0, 0, 1), 180),
            Translate((
                offset_x,
                0.5 * width - wall_base_media.thickness - wall_front_media.thickness,
                0.5 * height
            ))
        ]
    )
    back_wall = wall_panels.wall(
        name="back_wall",
        wall_base_media=wall_base_media,
        wall_front_media=wall_front_media,
        wall_back_media=wall_back_media,
        width=length,
        height=height,
        left_right_tab_direction=TabDirection.OUT,
        tab_length_x=tab_length_x,
        tab_length_y=tab_length_z,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), 90),
            Rotate((0, 0, 0), (0, 0, 1), 0),
            Translate((
                offset_x,
                -0.5 * width + wall_base_media.thickness + wall_front_media.thickness,
                0.5 * height
            ))
        ]
    )
    right_wall = wall_panels.gable_wall(
        name="right_wall",
        wall_base_media=wall_base_media,
        wall_front_media=wall_front_media,
        wall_back_media=wall_back_media,
        roof_media=roof_media,
        roof_layer_count=roof_layer_count,
        width=width,
        height=height,
        gable_height=gable_height,
        tab_length_x=tab_length_y,
        tab_length_y=tab_length_z,
        tab_length_roof=tab_length_roof,
        tab_offset_roof=tab_offset_roof,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), 90),
            Rotate((0, 0, 0), (0, 0, 1), 90),
            Translate((
                offset_x + 0.5 * length - wall_base_media.thickness - wall_front_media.thickness,
                0,
                0.5 * height))
        ]
    )
    left_wall = wall_panels.bare_gable_wall(
        name="left_wall",
        wall_base_media=wall_base_media,
        wall_front_media=wall_front_media,
        wall_back_media=wall_back_media,
        roof_media=roof_media,
        roof_layer_count=roof_layer_count,
        width=width,
        height=height,
        gable_height=gable_height,
        tab_length_x=tab_length_y,
        tab_length_y=tab_length_z,
        tab_length_roof=tab_length_roof,
        tab_offset_roof=tab_offset_roof,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), 90),
            Rotate((0, 0, 0), (0, 0, 1), -90),
            Translate((
                offset_x - 0.5 * length + wall_base_media.thickness + wall_front_media.thickness,
                0,
                0.5 * height
            ))
        ]
    )

    roof_angle = math.atan2(gable_height, 0.5 * width) * 180 / math.pi
    gable_length = math.sqrt(0.25 * width * width + gable_height * gable_height)
    roof_height = gable_length + roof_overhang_width

    back_roof = roof_panels.roof_panel(
        name="back_roof",
        roof_media=roof_media,
        wall_base_media=wall_base_media,
        wall_front_media=wall_front_media,
        house_length=original_length,
        house_width=width,
        gable_height=gable_height,
        overhang_left=roof_overhang_left,
        overhang_right=roof_overhang_right,
        overhang_width=roof_overhang_width,
        layer_count=roof_layer_count,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), roof_angle),
            Translate((
                0,
                -0.5 * roof_height * math.cos(math.radians(roof_angle)),
                height + gable_height - 0.5 * roof_height * math.sin(math.radians(roof_angle))
            ))
        ],
        tab_holes=roof_tab_holes,
        chimney_holes=[],
        reverse_hole_offsets=False,
        end_taper=roof_end_taper
    )
    front_roof = roof_panels.roof_panel(
        name="front_roof",
        roof_media=roof_media,
        wall_base_media=wall_base_media,
        wall_front_media=wall_front_media,
        house_length=original_length,
        house_width=width,
        gable_height=gable_height,
        overhang_left=roof_overhang_right,
        overhang_right=roof_overhang_left,
        overhang_width=roof_overhang_width,
        layer_count=roof_layer_count,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), roof_angle),
            Rotate((0, 0, 0), (0, 0, 1), 180),
            Translate((
                0,
                0.5 * roof_height * math.cos(math.radians(roof_angle)),
                height + gable_height - 0.5 * roof_height * math.sin(math.radians(roof_angle))
            ))
        ],
        tab_holes=roof_tab_holes,
        chimney_holes=[],
        reverse_hole_offsets=True,
        end_taper=roof_end_taper
    )
    
    house = PanelGroup(
        name=name,
        children=[
            floor, front_wall, back_wall, right_wall,
            left_wall,
            back_roof, front_roof
        ],
        transform=transform
    )
    
    return house
