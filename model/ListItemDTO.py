from datetime import datetime

import sirope


class ListItemDTO:
    def __init__(self, parent_oid, content, checked):
        self._parent_oid = parent_oid
        self._creation_time = datetime.now()
        self._content = content
        self._checked = checked
        self._disabled = False

    @property
    def oid(self):
        return self.__oid__.num

    @property
    def creation_time(self):
        return self._creation_time

    @property
    def parent_oid(self):
        return self._parent_oid

    @property
    def content(self):
        return self._content

    @property
    def checked(self):
        return self._checked

    @checked.setter
    def checked(self, value):
        self._checked = value

    @property
    def disabled(self):
        return self._disabled if self._disabled is not None else False

    @disabled.setter
    def disabled(self, value):
        self._disabled = value

    def __str__(self):
        return f'{self.parent_oid}: "{self.content}"'

    @staticmethod
    def find_for_list(sirope: sirope.Sirope, parent_oid: int) -> ["ListItemDTO"]:
        return [
            item
            for item in sirope.filter(ListItemDTO, lambda l: l.parent_oid == parent_oid)
        ]

    @staticmethod
    def find(sirope: sirope.Sirope, oid: int) -> "ListItemDTO":
        return sirope.find_first(ListItemDTO, lambda l: l.oid == oid)
