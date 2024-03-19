import unittest
from buildings import export_v2
from buildings import media_v2
from buildings.panels_v2.stokesley_station import back_house
from buildings.panels_v2.stokesley_station import main_house
from buildings.panels_v2.stokesley_station import porch_house
from buildings.panels_v2.stokesley_station import side_house
from buildings.panels_v2.stokesley_station import waiting_room
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


class StokesleyStationTestCase(unittest.TestCase):

    def test_waiting_room(self):
        pg = waiting_room.waiting_room(
            wall_base_media=wall_base_media,
            wall_front_media=wall_front_media,
            wall_back_media=wall_back_media,
            roof_media=roof_media,
            window_media=window_media,
            transform=[]
        )
        mesh_xml_str = export_v2.export_mesh_to_xml_string(panel_group=pg)
        expected_mesh_xml_str = utils.read_mesh_xml(filename="waiting_room_1.xml")
        utils.assert_equal_mesh_xml(
            mesh_xml_str=mesh_xml_str,
            expected_mesh_xml_str=expected_mesh_xml_str)
    
    def test_main_house(self):
        pg = main_house.main_house(transform=[])
        mesh_xml_str = export_v2.export_mesh_to_xml_string(panel_group=pg)
        expected_mesh_xml_str = utils.read_mesh_xml(filename="main_house_1.xml")
        utils.assert_equal_mesh_xml(
            mesh_xml_str=mesh_xml_str,
            expected_mesh_xml_str=expected_mesh_xml_str)
    
    def test_side_house(self):
        pg = side_house.side_house(transform=[])
        mesh_xml_str = export_v2.export_mesh_to_xml_string(panel_group=pg)
        expected_mesh_xml_str = utils.read_mesh_xml(filename="side_house_1.xml")
        utils.assert_equal_mesh_xml(
            mesh_xml_str=mesh_xml_str,
            expected_mesh_xml_str=expected_mesh_xml_str)
    
    def test_back_house(self):
        pg = back_house.back_house(transform=[])
        mesh_xml_str = export_v2.export_mesh_to_xml_string(panel_group=pg)
        expected_mesh_xml_str = utils.read_mesh_xml(filename="back_house_1.xml")
        utils.assert_equal_mesh_xml(
            mesh_xml_str=mesh_xml_str,
            expected_mesh_xml_str=expected_mesh_xml_str)
    
    def test_porch_house(self):
        pg = porch_house.porch_house(transform=[])
        mesh_xml_str = export_v2.export_mesh_to_xml_string(panel_group=pg)
        expected_mesh_xml_str = utils.read_mesh_xml(filename="porch_house_1.xml")
        utils.assert_equal_mesh_xml(
            mesh_xml_str=mesh_xml_str,
            expected_mesh_xml_str=expected_mesh_xml_str)

    # def test_write_file(self):
    #     pg = porch_house.porch_house(transform=[])
    #     mesh_xml_str = export_v2.export_mesh_to_xml_string(panel_group=pg)
    #     utils.write_mesh_xml(filename="porch_house_1.xml", xml_str=mesh_xml_str)
