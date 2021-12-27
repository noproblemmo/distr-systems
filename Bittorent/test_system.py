import unittest
from record import Record
from system import System
from db import *


class TestSystem(unittest.TestCase):
    def test_touch_methods(self):
        system = System(50)
        system.add_record(Record(1))
        system.add_record(Record(2))
        system.add_record(Record(75))
        self.assertEqual(len(system.get_all_db()), 3)
        self.assertIsNotNone(system.get_record(1))
        self.assertIsNone(system.get_record(3))

    def test_get_databases(self):
        system = System()
        self.assertIsNotNone(system.get_main())
        self.assertIsNotNone(system.get_shard())

    def test_add_record(self):
        system = System(5)
        system.add_record(Record(1))
        self.assertEqual(system.get_shard(0).records_num(), 0)
        self.assertEqual(system.get_shard(1).records_num(), 1)
        
    def test_get_record(self):
        system = System(5)
        system.add_record(Record(1))
        system.add_record(Record(11))
        system.add_record(Record(99))
        self.assertEqual(len(system.get_all(1)), 2)
        
       

class TestSystem_SetNumberOfshardics(unittest.TestCase):
    def test_1(self):
        system = System(1)
        system.get_shard(0)
        with self.assertRaises(IndexError):
            system.get_shard(1)

    def test_2(self):
        system = System(2)
        system.get_shard(0)
        system.get_shard(1)
        with self.assertRaises(IndexError):
            system.get_shard(2)

    def test_wrong_number(self):
        with self.assertRaises(ValueError):
            System(0)


class TestSystem_Stats(unittest.TestCase):
    def test_empty_2_shards(self):
        system = System(2)
        stats = system.stats()
        self.assertEqual(stats['main'], 0)
        self.assertEqual(stats['shard'], [0, 0])

    def test_empty_3_shards(self):
        system = System(3)
        stats = system.stats()
        self.assertEqual(stats['main'], 0)
        self.assertEqual(stats['shard'], [0, 0, 0])

    def test_read_data_once(self):
        system = System(2)
        system.add_record(Record(1))
        system.get_record(1)
        stats = system.stats()
        self.assertEqual(stats['main'], 0)
        self.assertEqual(stats['shard'], [0, 1])

    def test_read_data_many_times(self):
        system = System(2)
        system.add_record(Record(1))
        for _ in range(10):
            system.get_record(1)
        stats = system.stats()
        self.assertEqual(stats['main'], 0)
        self.assertEqual(stats['shard'], [0, 10])
    
    def test_read_data_many_times1(self):
        system = System(5)
        
        for i in range(10):
            system.add_record(Record(i))
            
        for i in range(10):
            system.get_record(i)
        
        stats = system.stats()
        self.assertEqual(stats['shard'], [2, 2, 2, 2, 2])