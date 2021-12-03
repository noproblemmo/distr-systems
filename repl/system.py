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
        return self.__main.add_record(rec)

    def get_record(self, record_id):
        """If main DB is broken then change this with repl"""
        cond = self.__main.get_condition()
        if(cond == True):
            swap_main_db()
        """Get record by ID."""
        rec = self.__repls[self.__ind].get_record(record_id)
        self.__stats['repl'][self.__ind] += 1
        self.__update_ind()
        if rec:
            return rec
        self.sync()
        return self.__main.get_record(record_id)

    def get_all(self):
        """Return all records."""
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
        for repl in self.__repls:
            if (repl.get_condition == False):
                self.__main, repl = repl, self.__main
                break
                
        raise ValueError("There are no working DB")
               
def _sync(src, dst):
    if dst.get_condition == True:
        return 0
    records = src.get_all()
    for rec_id, rec in records.items():
        if not dst.get_record(rec_id):
            dst.add_record(rec)
