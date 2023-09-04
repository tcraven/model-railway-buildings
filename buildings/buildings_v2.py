from buildings import export_v2
from buildings import media_v2
from buildings import panels_v2
from buildings.media_v2 import Media
from buildings.panels_v2 import Panel, PanelGroup, Cutout
from buildings.panels_v2 import wall_panels, window_panels
from buildings.transforms_v2 import Transform, Translate, Rotate


def create_wall_with_windows(
    base_media: Media,
    front_media: Media,
    back_media: Media,
    window_media: Media,
    transform: Transform
) -> PanelGroup:
    wall = wall_panels.wall(
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

    panels_v2.add_child_panel_group(parent=wall, child=window1)
    panels_v2.add_child_panel_group(parent=wall, child=window2)

    return wall


def main():
    wall_base_media = media_v2.CARD_2x169mm
    wall_front_media = media_v2.CARD_2x056mm
    wall_back_media = media_v2.CARD_056mm
    window_media = media_v2.CARD_056mm

    w0 = create_wall_with_windows(
        base_media=wall_base_media,
        front_media=wall_front_media,
        back_media=wall_back_media,
        window_media=window_media,
        transform=[
            Rotate((0, 0, 0), (1, 0, 0), 90),
            Translate((0, 0, 25))
        ]
    )
    w1 = create_wall_with_windows(
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
        children=[w0, w1],
        transform=[])

    model_name = "house-2"
    output_dirpath = export_v2.get_output_dirpath(model_name=model_name)
    export_v2.delete_output_dir(output_dirpath=output_dirpath)
    
    export_v2.export_mesh(
        output_dirpath=output_dirpath,
        panel_group=house)
    
    export_v2.export_svgs(
        panel_group=house,
        output_dirpath=output_dirpath,
        include_layout_boxes=False)

    print("OK")
