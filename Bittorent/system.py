"""System with shardication."""
from db import Database


class System:
    """System with shardication."""
    def __init__(self, shards_num=1):
        if shards_num < 1:
            raise ValueError("slaves_num must be positive")

        self.__main = Database()
        self.__shard = []
        for _ in range(shards_num):
            self.__shard.append(Database())

        self.__stats = {
            'main': 0,
            'shard': [],
        }
        for _ in range(shards_num):
            self.__stats['shard'].append(0)
        
        self.__ind = 0 

    def get_main(self):
        """Return main DB."""
        return self.__main

    def get_shard(self, ind=0):
        """Return shardicated DB."""
        return self.__shard[ind]

    def add_record(self, rec):
        """Add record to database."""
        """If main DB is not valid, then swap"""

        ind = rec.get_id() % len(self.__shard)
        
        self.__shard[ind].add_record(rec)

    def get_record(self, record_id):
        """If main DB is broken then change this with shard"""

        """Get record by ID."""
        
        ind = record_id % len(self.__shard)
        
        rec = self.__shard[ind].get_record(record_id)
        
        if rec:
            self.__stats['shard'][ind] += 1
            return rec

    def get_all(self, ind):

        res = self.__shard[ind].get_all()
        self.__stats['shard'][ind] += 1
        return res
        
    def get_all_db(self):
        
        res = {}
        
        for i in self.__shard:
            res = res | i.get_all() 
            
        return res

    def stats(self):
        """Return statistics of readings."""
        return self.__stats

    def __update_ind(self):
        self.__ind = (self.__ind + 1) % len(self.__shard)
    
    def swap_main_db(self):
        count = 0
        for i in range(len(self.__shard)):
            
            if (self.__shard[i].get_condition() == False):
                buf = self.__main
                self.__main = self.__shard[i]
                self.__shard[i] = buf
                
                buf = self.__stats['main']
                self.__stats['main'] = self.__stats['shard'][count]
                self.__stats['shard'][count] = buf
                
                break
            count += 1
            
           