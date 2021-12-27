"""System with shardication."""
from db import Database


class System:
    """System with shardication."""
    def __init__(self, shards_num=1):
        if shards_num < 1:
            raise ValueError("slaves_num must be positive")

        self.__main = Database()
        self.__shard = []
        self.__brokenShards = []
        for _ in range(shards_num):
            self.__shard.append(Database())
        
        #Contains a number of 
        
        self.__stats = {
            'main': 0,
            'shard': [],
            'broken': []
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
        
    def get_all_shards(self):
        return self.__shard
    
    def get_num_shards(self):
        return len(self.__shard)
        
    def get_broken_shard(self, ind=0):
        """Return shardicated DB."""
        return self.__brokenShards[ind]
        
    def get_all_broken_shards(self):
        return self.__brokenShards
        
    def remove_broken_shard(self, ind):
        #Save shard in buffer
        buf1 = self.get_shard(ind) #Get DB
        buf2 = self.stats()['shard'][ind] #Get stats of DB
        
        #Remove from shards DB
        self.get_all_shards().pop(ind)
        self.stats()['shard'].pop(ind)
        
        #Add in list of brokens
        self.get_all_broken_shards().append(buf1)
        self.stats()['broken'].append(buf2)
        
        self.redistributiondDB()

    def add_record(self, rec):
        """Add record to database."""
        """If main DB is not valid, then swap"""
        
        #Check for valid DB

        ind = rec.get_id() % len(self.__shard)
        
        shard = self.get_shard(ind)
        cond = shard.get_condition()
        """
        if(cond):
            self.remove_broken_shard(ind)
            ind = rec.get_id() % len(self.__shard)
        """     
        
        #Remove all invalid shards
        while(self.__shard[ind].get_condition() == True):
            self.remove_broken_shard(ind)
            ind = rec.get_id() % len(self.__shard)
            if(self.get_all_shards() == None):
                break
                #raise ValueError("slaves_num must be positive")
           
        if self.__shard[ind]:
            self.__shard[ind].add_record(rec)
    
    #Swap records of shards with new rules of sharding 
    
    def redistributiondDB(self):
        
        for ind in range(len(self.get_all_shards())):
            buffer = {}
            shardDB = self.get_shard(ind).get_all()
            for rec in shardDB: #Rec is id of record
                if(rec % len(self.get_all_shards()) != ind):
                    self.get_shard(rec % len(self.get_all_shards())).add_record(self.get_shard(ind).get_record(rec))
                else:
                    buffer[rec] = self.get_shard(ind).get_record(rec)
        
            self.get_shard(ind).import_DB(buffer)
            buffer.clear()
            
    """   
        for db in self.get_all_shards():
            shardIndex = 0
            shardRecords = db.get_all()
            buffer = {}
            for rec in shardRecords:
                if(shardRecords[rec].get_id() % len(self.__shard) != shardIndex):
                    #Add element in correct shard
                    ind = shardRecords[rec].get_id() % len(self.__shard)
                    self.__shard[ind].add_record(shardRecords[rec])
                    #Remove from incorrect shard
                else:
                    buffer[shardRecords[rec].get_id()] = shardRecords[rec]
                    
            self.__shard[shardIndex] = buffer
            buffer.clear()
            
            shardIndex += 1
    """     

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
"""
    def __update_ind(self):
        self.__ind = (self.__ind + 1) % len(self.__shard)
    
    #Swap swap Main DB with first working shard
    
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
"""          