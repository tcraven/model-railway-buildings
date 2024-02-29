from cadquery import Workplane
from buildings import media_v2
from buildings.panels_v2.stokesley_station import waiting_room
from buildings.panels_v2.stokesley_station import side_house
from buildings.panels_v2.stokesley_station import main_house
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

#pg = waiting_room.waiting_room(
#    wall_base_media=wall_base_media,
#    wall_front_media=wall_front_media,
#    wall_back_media=wall_back_media,
#    roof_media=roof_media,
#    window_media=window_media,
#    transform=[]
#)

#pg = side_house.side_house(transform=[])

pg = main_house.main_house(transform=[])

a = panels_v2.get_assembly(
    panel_group=pg  # .children[3]
)

show_object(a)

