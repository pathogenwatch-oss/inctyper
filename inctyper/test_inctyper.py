from unittest import TestCase
import inctyper_lib as il


class TestInctyper(TestCase):
    def test_resolve_inctype(self):

        self.assertEqual("IncHI1B(CIT)_1", il.resolve_inctype("IncHI1B(CIT)_1_pNDM-CIT_JX182975"))
        self.assertEqual("IncB/O/K/Z_2", il.resolve_inctype("IncB/O/K/Z_2__GU256641"))
