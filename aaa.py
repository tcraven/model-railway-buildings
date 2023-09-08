from buildings import media_v2
from buildings.panels_v2 import houses
from buildings import panels_v2
from buildings.panels_v2 import window_panels
from buildings.transforms_v2 import Translate

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

a = panels_v2.get_assembly(
    #panel_group=house.children[0]
    panel_group=house
)

show_object(a)
