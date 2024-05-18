from datetime import datetime

import sirope


class ListItemEditDTO:
    def __init__(self, parent_oid, user_oid, action, before=None, after=None):
        """

        :param parent_oid: oid of the parent ListItem
        :param user_oid: oid of the user that executed the action
        :param action: the action that was performed (add, remove, edit, check, uncheck
        :param before: The value of the item before it was changed. Optional
        :param after: The value of the item after it was changed. Optional
        """
        self._parent_oid = parent_oid
        self._creation_time = datetime.now()
        self._user_oid = user_oid
        self._action = action
        self._before = before
        self._after = after

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
    def user_oid(self):
        return self._user_oid

    @property
    def action(self):
        return self._action

    @property
    def before(self):
        return self._before

    @property
    def after(self):
        return self._after

    def __str__(self):
        return f'{self.parent_oid}: "{self.user_oid}"'

    @staticmethod
    def find_for_item(sirope: sirope.Sirope, parent_oid: int) -> ["ListItemEditDTO"]:
        """
        Returns all edits for the item with the specified oid (parent_oid)
        :param sirope:
        :param parent_oid:
        :return:
        """
        return [
            item
            for item in sirope.filter(
                ListItemEditDTO, lambda l: l.parent_oid == parent_oid
            )
        ]

    @staticmethod
    def delete_for_item(sirope: sirope.Sirope, item_oid: int):
        """
        Deleted all edits for the item with oid "item_oid
        :param sirope:
        :param oid:
        :return:
        """
        edit_list = [
            item
            for item in sirope.filter(
                ListItemEditDTO, lambda l: l.parent_oid == item_oid
            )
        ]

        for item in edit_list:
            sirope.delete(item.__oid__)

    @staticmethod
    def find(sirope: sirope.Sirope, oid: int) -> "ListItemEditDTO":
        return sirope.find_first(ListItemEditDTO, lambda l: l.oid == oid)
