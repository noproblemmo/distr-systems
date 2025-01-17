"""Replication example."""


class Database:
    """Database prototype."""
    def __init__(self):
        self.__records = {}
        self.__broken = False

    def records_num(self):
        """Number of records."""
        return len(self.__records)

    def add_record(self, r):
        """Add record to database."""
        if r.get_id() in self.__records:
            raise ValueError("Duplicated ID")

        self.__records[r.get_id()] = r

    def get_record(self, record_id):
        """Get record by ID."""
        try:
            return self.__records[record_id]
        except KeyError:
            return None
    
    def get_condition(self):
        return self.__broken

    def get_all(self):
        """Return all records."""
        return self.__records
    
    def broke_db(self):
        self.__broken = True
    
    def fix_db(self):
        self.__broken = False