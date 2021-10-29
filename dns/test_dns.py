import unittest
from dns import Comp
from dns import Net
from dns import DnsDb, Record
# TODO: extract modules


class TestComp(unittest.TestCase):
    def test_no_ping(self):
        comp = Comp()
        ans = comp.ping("1.2.3.4")
        self.assertEqual(ans, "No network")


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


class TestDnsDb(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(DnsDb().num_records(), 0)

    def test_add_record(self):
        db = DnsDb()
        db.add_record(Record("narfu.ru", "1.2.3.4"))
        self.assertEqual(db.num_records(), 1)

    def test_get_addr_known(self):
        db = DnsDb()
        db.add_record(Record("narfu.ru", "1.2.3.4"))
        addr = db.resolve("narfu.ru")
        self.assertEqual(addr, "1.2.3.4")

    def test_get_addr_known_2(self):
        # TODO test, ref: merge with prev
        db = DnsDb()
        db.add_record(Record("narfu.ru", "2.3.4.5"))
        addr = db.resolve("narfu.ru")
        self.assertEqual(addr, "2.3.4.5")

    def test_get_addr_unknown(self):
        # TODO: implement
        db = DnsDb()
        db.add_record(Record("narfu.ru", "2.3.4.5"))
        db.add_record(Record("29.ru", "3.4.5.6"))
        addr = db.resolve("narfu.com")
        self.assertIsNone(addr)

    def test_same_addresses_differ_names(self):
        db = DnsDb()
        db.add_record(Record("narfu.ru", "2.3.4.5"))

        raised = False
        try:
            db.add_record(Record("29.ru", "2.3.4.5"))
        except ValueError:
            raised = True

        self.assertTrue(raised)


class TestDns(unittest.TestCase):
    def test_no_addr(self):
        comp = Comp()
        ans = comp.resolve("narfu.ru")
        self.assertEqual(ans, None)  # TODO ref: use standard error

    def test_answer_in_local_db(self):
        comp = Comp()
        db = DnsDb()
        db.add_record(Record("narfu.ru", "1.2.3.4"))
        comp.set_dns_db(db)
        ans = comp.resolve("narfu.ru")
        self.assertEqual(ans, "1.2.3.4")

    def test_answer_from_dns_server(self):
        comp = Comp()
        local_db = DnsDb()
        local_db.add_record(Record("narfu.ru", "1.2.3.4"))
        comp.set_dns_db(local_db)
        # TODO ref: comp: set_dns_server: replace to network interface
        comp.set_dns_server("10.20.30.40")
        # TODO test: no such host (dns server)

        server = Comp()
        server_db = DnsDb()
        server_db.add_record(Record("ya.ru", "2.3.4.5"))
        server.set_dns_db(server_db)

        net = Net()
        net.add_host(comp, "11.12.13.14")
        net.add_host(server, "10.20.30.40")

        ans = comp.resolve("maps.ya.ru")
        self.assertEqual(ans, "2.3.4.5")

    # TODO test: comp: local db: resolve unknown name
    # TODO feat: comp: ping name
