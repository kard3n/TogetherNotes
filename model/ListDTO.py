from datetime import datetime


class ListDTO:
    def __init__(self, oid, name, owner_oid):
        self._name = name
        self._oid = oid
        self._owner_oid = owner_oid
        self._creation_time = datetime.now()
        self._users_with_access = [owner_oid]

    @property
    def oid(self):
        return self._oid

    @property
    def name(self):
        return self._name

    @property
    def creation_time(self):
        return self._creation_time

    @property
    def owner_oid(self):
        return self._owner_oid

    @property
    def users_with_access(self):
        return self._users_with_access

    def __str__(self):
        return f'{self.creation_time}: "{self.name}"'
