import unittest
from comp import Comp
from net import Net


class TestNet(unittest.TestCase):
    def test_empty(self):
        net = Net()
        ans = net.ping("", "1.2.3.4")
        self.assertEqual(ans, "Unknown host")

    def test_ping_host_exists(self):
        net = Net()
        comp1 = Comp()
        comp2 = Comp()
        net.add_host(comp1, "1.2.3.4")
        net.add_host(comp2, "2.3.4.5")
        ans = comp1.ping("2.3.4.5")
        self.assertEqual(
            ans, "ping from 1.2.3.4 to 2.3.4.5")

        ans = comp2.ping("1.2.3.4")
        self.assertEqual(
            ans, "ping from 2.3.4.5 to 1.2.3.4")

        ans = comp1.ping("3.4.5.6")
        self.assertEqual(ans, "Unknown host")
