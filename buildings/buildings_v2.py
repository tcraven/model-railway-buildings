import subprocess
from buildings import export_v2
from buildings import media_v2
from buildings import panels_v2
from buildings.media_v2 import Media
from buildings.panels_v2 import Panel, PanelGroup, Cutout
from buildings.panels_v2 import houses, wall_panels, window_panels, chimneys
from buildings.transforms_v2 import Transform, Translate, Rotate
from buildings.panels_v2 import pi_camera_stand
from buildings.panels_v2.stokesley_station import main_house
from buildings.panels_v2.stokesley_station import porch_house
from buildings.panels_v2.stokesley_station import side_house
from buildings.panels_v2.stokesley_station import waiting_room


def main():
    wall_base_media = media_v2.CARD_2x169mm
    wall_front_media = media_v2.CARD_2x056mm
    wall_back_media = media_v2.CARD_056mm
    window_media = media_v2.CARD_056mm
    roof_media = media_v2.CARD_056mm

    waiting_room_pg = waiting_room.waiting_room(
        wall_base_media=wall_base_media,
        wall_front_media=wall_front_media,
        wall_back_media=wall_back_media,
        roof_media=roof_media,
        window_media=window_media,
        transform=[]
    )

    side_house_pg = side_house.side_house(
        transform=[
            Translate((-114, 0, 0))
        ]
    )

    main_house_pg = main_house.main_house(
        transform=[
            Rotate((0, 0, 0), (0, 0, 1), -90),
            Translate((-177.5, 38, 0))
        ]
    )

    porch_house_pg = porch_house.porch_house(
        transform=[
            Rotate((0, 0, 0), (0, 0, 1), 180),
            Translate((-220, 38, 0))  # -219.5
        ]
    )

    pg = PanelGroup(
        name="station",
        children=[
            waiting_room_pg,
            side_house_pg,
            main_house_pg,
            porch_house_pg
        ]
    )

    model_name = "stokesley-station"
    # model_name = "stokesley-station-waiting-room"
    # model_name = "chimney-test"
    output_dirpath = export_v2.get_output_dirpath(model_name=model_name)
    export_v2.delete_output_dir(output_dirpath=output_dirpath)
    
    export_v2.export_mesh(
        output_dirpath=output_dirpath,
        panel_group=pg)
    
    subprocess.run(["cp", f"{output_dirpath}/mesh.gltf", "./photo-match-data"])
    
    export_v2.export_svgs(
        panel_group=pg,
        output_dirpath=output_dirpath,
        include_layout_boxes=False)

    print("OK")
