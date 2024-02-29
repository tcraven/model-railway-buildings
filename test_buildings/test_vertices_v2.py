import unittest
from buildings import vertices_v2


class GetPathEdgesTestCase(unittest.TestCase):

    maxDiff = None

    def test_two_point_path_strings(self):
        path_strings = [
            'M34.5,42.5 L34.5,-42.5 ',
            'M0.0,64.5 L34.5,42.49999999999999 ',
            'M34.5,-42.5 L-34.5,-42.5 ',
            'M-34.5,42.5 L0.0,64.5 '
        ]
        expected_path_edges = [
            ['34.5,42.5', '34.5,-42.5'],
            ['0.0,64.5', '34.5,42.49999999999999'],
            ['34.5,-42.5', '-34.5,-42.5'],
            ['-34.5,42.5', '0.0,64.5']
        ]
        path_edges = vertices_v2._get_path_edges(path_strings=path_strings)
        self.assertEqual(path_edges, expected_path_edges)

    def test_many_point_path_strings(self):
        path_strings = [
            'M34.5,42.5 L34.5,-42.5 ',
            'M0.0,64.5 L34.5,42.49999999999999 ',
            'M4.5,29.0 L4.496052735444863,29.1884404417814 L4.484217866622769,29.37655029499542 L4.464516155915151,29.56399955103937 L4.4369821668172715,29.75045936022246 L4.401664203302125,29.93560260867992 ',
            'M34.5,-42.5 L-34.5,-42.5 ',
            'M-34.5,42.5 L0.0,64.5 '
        ]
        expected_path_edges = [
            ['34.5,42.5', '34.5,-42.5'],
            ['0.0,64.5', '34.5,42.49999999999999'],

            # Multiple points in the path string must result in multiple
            # path edges all connected together
            ['4.5,29.0', '4.496052735444863,29.1884404417814'],            
            ['4.496052735444863,29.1884404417814', '4.484217866622769,29.37655029499542'],
            ['4.484217866622769,29.37655029499542', '4.464516155915151,29.56399955103937'],
            ['4.464516155915151,29.56399955103937', '4.4369821668172715,29.75045936022246'],
            ['4.4369821668172715,29.75045936022246', '4.401664203302125,29.93560260867992'],

            ['34.5,-42.5', '-34.5,-42.5'],
            ['-34.5,42.5', '0.0,64.5']
        ]
        path_edges = vertices_v2._get_path_edges(path_strings=path_strings)
        self.assertEqual(path_edges, expected_path_edges)
