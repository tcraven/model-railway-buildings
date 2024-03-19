import math
from cadquery import Workplane
from buildings import media_v2
from buildings.panels_v2.stokesley_station import waiting_room
from buildings.panels_v2.stokesley_station import side_house
from buildings.panels_v2.stokesley_station import main_house
from buildings.panels_v2.stokesley_station import porch_house
from buildings.panels_v2.stokesley_station import back_house
from buildings.tabs import Tab, TabDirection
from buildings import panels_v2
from buildings.panels_v2 import window_panels, roof_panels
from buildings.transforms_v2 import Translate, Rotate
from buildings.panels_v2 import houses, PanelGroup

wall_base_media = media_v2.CARD_2x169mm
wall_front_media = media_v2.CARD_2x056mm
wall_back_media = media_v2.CARD_056mm
window_media = media_v2.CARD_056mm
roof_media = media_v2.CARD_056mm


#side_house_pg = side_house.side_house(
#    transform=[
#        Translate((-114 + 0, 0, 0))
#    ]
#)

#main_house_pg = main_house.main_house(
#    transform=[
#        Rotate((0, 0, 0), (0, 0, 1), -90),
#        Translate((-177.5, 38, 0))
#    ]
#)

back_house_pg = back_house.back_house(
    transform=[
        Rotate((0, 0, 0), (0, 0, 1), 90),
        Translate((-122.5, 70.5, 0))
    ]
)


pg = PanelGroup(
    name="station",
    children=[
        #waiting_room_pg,
        #side_house_pg,
        #main_house_pg,
        #porch_house_pg,
        back_house_pg
    ]
)

a = panels_v2.get_assembly(
    panel_group=pg
)

show_object(a)

