from unittest import TestCase

import inctyper_lib as lib


class TestIncTyperLib(TestCase):

    def test_overlapping(self):
        match1 = {'qstart': 1, 'qend': 100}
        match2 = {'qstart': 75, 'qend': 200}
        self.assertTrue(lib.overlapping(match1, match2, 20))

        self.assertTrue(lib.overlapping(match2, match1, 20))

        match3 = {'qstart': 82, 'qend': 150}
        self.assertTrue(not lib.overlapping(match1, match3, 20))

        self.assertTrue(lib.overlapping(match1, match1, 20))

    def test_select_matches(self):
        match1 = {'qstart': 1, 'qend': 100, 'pid': 100.0}
        match2 = {'qstart': 75, 'qend': 200, 'pid': 99.0}
        match3 = {'qstart': 82, 'qend': 200, 'pid': 99.0}

        input = [match2, match3, match1]
        expected = [match1, match3]

        self.assertEqual(expected, lib.select_matches(input))
