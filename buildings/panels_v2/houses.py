from buildings import panels_v2
from buildings.media_v2 import Media
from buildings.panels_v2 import Panel, PanelGroup
from buildings.panels_v2 import wall_panels, window_panels
from buildings.transforms_v2 import Transform, Translate, Rotate
from buildings.tabs import Tab, TabDirection


def basic_house(
    wall_base_media: Media,
    wall_front_media: Media,
    wall_back_media: Media,
    window_media: Media,
    length: float,
    width: float,
    height: float,
    gable_height: float
) -> PanelGroup:
    
    floor = wall_panels.floor(
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
    right_wall = wall_panels.wall(
        name="right_wall",
        wall_base_media=wall_base_media,
        wall_front_media=wall_front_media,
        wall_back_media=wall_back_media,
        width=width,
        height=height,
        left_right_tab_direction=TabDirection.IN,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), 90),
            Rotate((0, 0, 0), (0, 0, 1), 90),
            Translate((0.5 * length - wall_base_media.thickness - wall_front_media.thickness, 0, 0.5 * height))
        ]
    )
    left_wall = wall_panels.wall(
        name="left_wall",
        wall_base_media=wall_base_media,
        wall_front_media=wall_front_media,
        wall_back_media=wall_back_media,
        width=width,
        height=height,
        left_right_tab_direction=TabDirection.IN,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), 90),
            Rotate((0, 0, 0), (0, 0, 1), -90),
            Translate((-0.5 * length + wall_base_media.thickness + wall_front_media.thickness, 0, 0.5 * height))
        ]
    )
    
    house = PanelGroup(
        name="house",
        children=[floor, front_wall, back_wall, right_wall, left_wall]
    )
    
    return house


def house_windows_test(
    wall_base_media: Media,
    wall_front_media: Media,
    wall_back_media: Media,
    window_media: Media,
    length: float,
    width: float,
    height: float,
    gable_height: float
) -> PanelGroup:

    house = basic_house(
        wall_base_media=wall_base_media,
        wall_front_media=wall_front_media,
        wall_back_media=wall_back_media,
        window_media=window_media,
        length=length,
        width=width,
        height=height,
        gable_height=gable_height
    )

    front_wall = panels_v2.get_child_panel_group(
        panel_group=house,
        name="front_wall"
    )
    panels_v2.add_child_panel_group(
        parent=front_wall,
        child=window_panels.window(
            base_media=wall_base_media,
            media=window_media,
            transform=[Translate((-20, 0, 0))]
        )
    )
    panels_v2.add_child_panel_group(
        parent=front_wall,
        child=window_panels.window(
            base_media=wall_base_media,
            media=window_media,
            transform=[Translate((20, 0, 0))]
        )
    )

    back_wall = panels_v2.get_child_panel_group(
        panel_group=house,
        name="back_wall"
    )
    panels_v2.add_child_panel_group(
        parent=back_wall,
        child=window_panels.window(
            base_media=wall_base_media,
            media=window_media,
            transform=[Translate((-20, 0, 0))]
        )
    )
    panels_v2.add_child_panel_group(
        parent=back_wall,
        child=window_panels.window(
            base_media=wall_base_media,
            media=window_media,
            transform=[Translate((20, 0, 0))]
        )
    )

    panels_v2.add_child_panel_group(
        parent=panels_v2.get_child_panel_group(
            panel_group=house,
            name="right_wall"
        ),
        child=window_panels.window(
            base_media=wall_base_media,
            media=window_media,
            transform=[Translate((0, 0, 0))]
        )
    )

    return house


def house_two_walls_test(
    wall_base_media: Media,
    wall_front_media: Media,
    wall_back_media: Media,
    window_media: Media
) -> PanelGroup:
    w0 = wall_panels.wall_with_windows(
        base_media=wall_base_media,
        front_media=wall_front_media,
        back_media=wall_back_media,
        window_media=window_media,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), 90),
            Translate((0, 0, 25))
        ]
    )
    w1 = wall_panels.wall_with_windows(
        base_media=wall_base_media,
        front_media=wall_front_media,
        back_media=wall_back_media,
        window_media=window_media,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), 90),
            Rotate((0, 0, 0), (0, 0, 1), 180),
            Translate((0, 50, 25))
        ]
    )
    house = PanelGroup(
        name="house",
        children=[w0, w1]
    )
    
    return house
