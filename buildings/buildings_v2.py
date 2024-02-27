import subprocess
from buildings import export_v2
from buildings import media_v2
from buildings import panels_v2
from buildings.media_v2 import Media
from buildings.panels_v2 import Panel, PanelGroup, Cutout
from buildings.panels_v2 import houses, wall_panels, window_panels, chimneys
from buildings.transforms_v2 import Transform, Translate, Rotate
from buildings.panels_v2 import pi_camera_stand
from buildings.panels_v2 import stokesley_station


def main():
    wall_base_media = media_v2.CARD_2x169mm
    wall_front_media = media_v2.CARD_2x056mm
    wall_back_media = media_v2.CARD_056mm
    window_media = media_v2.CARD_056mm
    roof_media = media_v2.CARD_056mm

    pg = stokesley_station.waiting_room(
        wall_base_media=wall_base_media,
        wall_front_media=wall_front_media,
        wall_back_media=wall_back_media,
        roof_media=roof_media,
        window_media=window_media
    )

    # pg = chimneys.chimney(
    #     base_media=media_v2.CARD_169mm,
    #     wall_media=media_v2.CARD_056mm,
    #     chimney_width=9,
    #     core_base_layer_count=3,
    #     core_wall_layer_count=0,
    #     shaft_height=27,
    #     shaft_base_height=20,
    #     transform=[]
    # )

    model_name = "stokesley-station-waiting-room"
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
