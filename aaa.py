from buildings import media_v2
from buildings.panels_v2 import stokesley_station
from buildings.tabs import Tab, TabDirection
from buildings import panels_v2
from buildings.panels_v2 import window_panels
from buildings.transforms_v2 import Translate, Rotate
from buildings.panels_v2 import chimneys

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

#pg = chimneys.chimney(
#    base_media=media_v2.CARD_169mm,
#    wall_media=media_v2.CARD_056mm,
#    chimney_width=9,
#    core_base_layer_count=3,
#    core_wall_layer_count=0,
#    shaft_height=27,
#    shaft_base_height=20,
#    transform=[]
#)

a = panels_v2.get_assembly(
    panel_group=pg  # .children[3]
)

show_object(a)

