import unittest
from repl import Record, Db
from repl import DistrDb


class TestDb(unittest.TestCase):
    def test_empty(self):
        db = Db()
        self.assertEqual(db.records_num(), 0)

    def test_add_records(self):
        db = Db()
        db.add_record(Record(1))
        self.assertEqual(db.records_num(), 1)

    def test_add_same_record_twice(self):
        db = Db()
        db.add_record(Record(1))
        with self.assertRaises(ValueError):
            db.add_record(Record(1))

    def test_get_record_exists(self):
        db = Db()
        db.add_record(Record(1))
        self.assertIsNotNone(db.get_record(1))

    def test_get_record_not_exists(self):
        db = Db()
        db.add_record(Record(1))
        self.assertIsNone(db.get_record(2))

    def test_get_all(self):
        db = Db()
        db.add_record(Record(1))
        db.add_record(Record(2))
        db.add_record(Record(3))
        db.add_record(Record(4))
        self.assertEqual(len(db.get_all()), 4)


class TestDistrDb(unittest.TestCase):
    def test_touch_methods(self):
        db = DistrDb()
        db.add_record(Record(1))
        db.add_record(Record(2))
        self.assertEqual(db.records_num(), 2)
        self.assertEqual(len(db.get_all()), 2)
        self.assertIsNotNone(db.get_record(1))
        self.assertIsNone(db.get_record(3))
