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
        self.__main = Db()
        self.__repls = [Db(), Db()]
        self.__ind = 0

    def get_main(self):
        """Return main DB."""
        return self.__main

    def get_repl(self, ind=0):
        """Return replicated DB."""
        return self.__repls[ind]

    def sync(self):
        """Synchronize system."""
        for r in self.__repls:
            _sync(self.__main, r)

    def records_num(self):
        """Number of records."""
        return self.__main.records_num()

    def add_record(self, r):
        """Add record to database."""
        return self.__main.add_record(r)

    def get_record(self, record_id):
        """Get record by ID."""
        rec = self.__repls[self.__ind].get_record(record_id)
        self.__update_ind()
        if rec:
            return rec
        return self.__main.get_record(record_id)

    def get_all(self):
        """Return all records."""
        res = self.__repls[self.__ind].get_all()
        self.__update_ind()
        return res

    def __update_ind(self):
        self.__ind = (self.__ind + 1) % len(self.__repls)


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


def _sync(src, dst):
    records = src.get_all()
    for id, rec in records.items():
        if not dst.get_record(id):
            dst.add_record(rec)
