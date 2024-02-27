import unittest
from buildings import export_v2
from buildings import media_v2
from buildings.panels_v2 import stokesley_station
from test_buildings import utils

"""
Create all buildings and verify that the exported mesh XML is identical
to the expected mesh XML for each building.
"""


wall_base_media = media_v2.CARD_2x169mm
wall_front_media = media_v2.CARD_2x056mm
wall_back_media = media_v2.CARD_056mm
window_media = media_v2.CARD_056mm
roof_media = media_v2.CARD_056mm


class TestStokesleyStation(unittest.TestCase):

    def test_waiting_room(self):
        pg = stokesley_station.waiting_room(
            wall_base_media=wall_base_media,
            wall_front_media=wall_front_media,
            wall_back_media=wall_back_media,
            roof_media=roof_media,
            window_media=window_media
        )
        mesh_xml_str = export_v2.export_mesh_to_xml_string(panel_group=pg)
        expected_mesh_xml_str = utils.read_mesh_xml(filename="waiting_room_1.xml")
        utils.assert_equal_mesh_xml(
            mesh_xml_str=mesh_xml_str,
            expected_mesh_xml_str=expected_mesh_xml_str)
