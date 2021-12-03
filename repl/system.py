"""System with replication."""
from db import Database


class System:
    """System with replication."""
    def __init__(self, repls_num=1):
        if repls_num < 1:
            raise ValueError("repls_num must be positive")

        self.__main = Database()
        self.__repls = []
        for _ in range(repls_num):
            self.__repls.append(Database())

        self.__stats = {
            'main': 0,
            'repl': [],
        }
        for _ in range(repls_num):
            self.__stats['repl'].append(0)

        self.__ind = 0

    def get_main(self):
        """Return main DB."""
        return self.__main

    def get_repl(self, ind=0):
        """Return replicated DB."""
        return self.__repls[ind]

    def sync(self):
        """Synchronize system."""
        for repl in self.__repls:
            _sync(self.__main, repl)

    def add_record(self, rec):
        """Add record to database."""
        """If main DB is not valid, then swap"""
        if(self.__main.get_condition() == True):
            self.swap_main_db()
            
        return self.__main.add_record(rec)

    def get_record(self, record_id):
        """If main DB is broken then change this with repl"""
        if(self.__main.get_condition() == True):
            self.swap_main_db()
        """Get record by ID."""
        '''
        unvalid_count = 0
        for i in range(len(self.__repls)):
            if(self.__repls[self.__ind].get_condition() == False):
                break
            else: 
                self.__update_ind()
                unvalid_count += 1
            if(unvalid_count == len(self.__repls)):
                raise "There are no valid DB"
        '''
        count = 0
        while(True):
            if(self.__repls[self.__ind].get_condition() == True):
                self.__update_ind()
            else:
                break
            count += 1
            if(count > len(self.__repls)):
                break
            
        rec = self.__repls[self.__ind].get_record(record_id)
        self.__stats['repl'][self.__ind] += 1
        self.__update_ind()
        if rec:
            return rec
        self.sync()
        return self.__main.get_record(record_id)

    def get_all(self):
        """Return all records."""
        '''
        unvalid_count = 0
        for i in range(len(self.__repls)):
            if(self.__repls[self.__ind].get_condition() == False):
                break
            else: 
                self.__update_ind()
                unvalid_count += 1
            if(unvalid_count == len(self.__repls)):
                raise "There are no valid DB"
        '''
        res = self.__repls[self.__ind].get_all()
        self.__stats['repl'][self.__ind] += 1
        self.__update_ind()
        return res

    def stats(self):
        """Return statistics of readings."""
        return self.__stats

    def __update_ind(self):
        self.__ind = (self.__ind + 1) % len(self.__repls)
    
    def swap_main_db(self):
        count = 0
        for i in range(len(self.__repls)):
            
            if (self.__repls[i].get_condition() == False):
                buf = self.__main
                self.__main = self.__repls[i]
                self.__repls[i] = buf
                
                buf = self.__stats['main']
                self.__stats['main'] = self.__stats['repl'][count]
                self.__stats['repl'][count] = buf
                
                break
            count += 1
        
        #TODO REF: Maybe it doesn't work 
        #raise ValueError("There are no working DB")
        #return None        
                

               
def _sync(src, dst):
    if dst.get_condition == True:
        return 0
    records = src.get_all()
    for rec_id, rec in records.items():
        if not dst.get_record(rec_id):
            dst.add_record(rec)
