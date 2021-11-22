"""Replication example."""


class Record:
    """Record in database."""
    def __init__(self, record_id):
        self.__id = record_id

    def get_id(self):
        """Return record ID."""
        return self.__id


class DistrDb:
    """Database with replication."""
    def __init__(self):
        self.__db = Db()

    def records_num(self):
        """Number of records."""
        return self.__db.records_num()

    def add_record(self, r):
        """Add record to database."""
        return self.__db.add_record(r)

    def get_record(self, record_id):
        """Get record by ID."""
        return self.__db.get_record(record_id)

    def get_all(self):
        """Return all records."""
        return self.__db.get_all()


class Db:
    """Database prototype."""
    def __init__(self):
        self.__records = {}

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

    def get_all(self):
        """Return all records."""
        return self.__records
