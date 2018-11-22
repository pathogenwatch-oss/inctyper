from unittest import TestCase

import inctyper_lib as lib


class TestOverlapping(TestCase):

    def test_overlapping(self):
        match1 = {'qstart': 1, 'qend': 100}
        match2 = {'qstart': 75, 'qend': 200}
        self.assertTrue(lib.overlapping(match1, match2, 20))

        self.assertTrue(lib.overlapping(match2, match1, 20))

        match3 = {'qstart': 82, 'qend': 150}
        self.assertTrue(not lib.overlapping(match1, match3, 20))

        self.assertTrue(lib.overlapping(match1, match1, 20))
