"""shardication example."""


class Database:
    """Database prototype."""
    def __init__(self):
        self.__records = {}
        self.__broken = False #False - not broken

    def records_num(self):
        """Number of records."""
        return len(self.__records)

    def add_record(self, r):
        """Add record to database."""
        flag = True
        #Don't insert copy of right records
        if r.get_id() in self.__records:
            flag = False
            #raise ValueError("Duplicated ID")
        if(flag):    
            self.__records[r.get_id()] = r

    def get_record(self, record_id):
        """Get record by ID."""
        try:
            return self.__records[record_id]
        except KeyError:
            return None
            
    def import_DB(self, database):
        self.__records = database
    
    def get_condition(self):
        return self.__broken

    def get_all(self):
        """Return all records."""
        return self.__records
    
    def broke_db(self):
        self.__broken = True
    
    def fix_db(self):
        self.__broken = False
        
    def test(self):
        print("test")