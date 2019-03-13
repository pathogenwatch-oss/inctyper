import sys
from unittest import TestCase

import inctyper_lib as lib


class TestIncTyperLib(TestCase):

    def test_overlapping(self):
        match1 = {'qstart': 1, 'qend': 100}
        match2 = {'qstart': 75, 'qend': 200}
        match3 = {'qstart': 82, 'qend': 150}
        match4 = {'qstart': 100, 'qend': 200}

        print("Checking normal overlap", file=sys.stderr)
        self.assertTrue(lib.overlapping(match1, match2, 20))

        print("Checking overlap unaffected by argument order", file=sys.stderr)
        self.assertTrue(lib.overlapping(match2, match1, 20))

        print("Checking not overlapping", file=sys.stderr)
        self.assertTrue(not lib.overlapping(match1, match3, 20))

        print("Checking exactly identical matches are filtered", file=sys.stderr)
        self.assertTrue(lib.overlapping(match1, match1, 20))

        print("Checking for off-by-one errors on overlaps (1)", file=sys.stderr)
        self.assertTrue(lib.overlapping(match1, match4, 0))
        self.assertTrue(lib.overlapping(match4, match1, 0))
        self.assertTrue(lib.overlapping(match1, match2, 25))

        print("Checking for off-by-one errors on overlaps (2)", file=sys.stderr)
        self.assertTrue(not lib.overlapping(match1, match4, 1))
        self.assertTrue(not lib.overlapping(match4, match1, 1))
        self.assertTrue(not lib.overlapping(match1, match2, 26))

    def test_select_matches(self):
        match1 = {'qstart': 1, 'qend': 100, 'pid': 100.0}
        match2 = {'qstart': 75, 'qend': 200, 'pid': 99.0}
        match3 = {'qstart': 82, 'qend': 200, 'pid': 99.0}

        input = [match2, match3, match1]
        expected = [match1, match3]

        self.assertEqual(expected, lib.select_matches(input))
