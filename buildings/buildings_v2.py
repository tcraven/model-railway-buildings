from buildings import export_v2
from buildings import media_v2
from buildings import panels_v2
from buildings.media_v2 import Media
from buildings.panels_v2 import Panel, PanelGroup, Cutout
from buildings.panels_v2 import houses, wall_panels, window_panels
from buildings.transforms_v2 import Transform, Translate, Rotate


def main():
    wall_base_media = media_v2.CARD_2x169mm
    wall_front_media = media_v2.CARD_2x056mm
    wall_back_media = media_v2.CARD_056mm
    window_media = media_v2.CARD_056mm
    roof_media = media_v2.CARD_056mm

    house = houses.house_windows_test(
        wall_base_media=wall_base_media,
        wall_front_media=wall_front_media,
        wall_back_media=wall_back_media,
        roof_media=roof_media,
        window_media=window_media,
        length=90,
        width=60,
        height=50,
        gable_height=23
    )

    model_name = "house-3"
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
