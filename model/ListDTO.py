from datetime import datetime

import sirope


class ListDTO:
    def __init__(self, name, owner_oid, description):
        self._name = name
        self._owner_oid = owner_oid
        self._creation_time = datetime.now()
        self._users_with_access = [owner_oid]
        self._description = description

    @property
    def oid(self):
        return self.__oid__.num

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

    @property
    def description(self):
        return self._description

    def __str__(self):
        return f'{self.creation_time}: "{self.name}"'

    @staticmethod
    def find(sirope: sirope.Sirope, oid: int) -> "ListDTO":
        return sirope.find_first(ListDTO, lambda l: l.__oid__.num == oid)

    def find_for_user(sirope: sirope.Sirope, user_oid: int) -> ["ListDTO"]:
        return [
            item
            for item in sirope.filter(
                ListDTO, lambda l: user_oid in l.users_with_access
            )
        ]
