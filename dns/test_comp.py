import unittest
from nice import *


class TestComp(unittest.TestCase):
    def test_no_ping(self):
        comp = compsys.Comp()
        ans = comp.iface().ping("1.2.3.4")
        self.assertEqual(ans, "No network")
