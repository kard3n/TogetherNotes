from datetime import datetime

import sirope


class InviteDTO:
    def __init__(self, inviter_oid, invitee_oid, list_oid, message):
        self._inviter_oid = inviter_oid
        self._invitee_oid = invitee_oid
        self._list_oid = list_oid
        self._creation_time = datetime.now()
        self._message = message

    @property
    def oid(self):
        return self.__oid__.num

    @property
    def creation_time(self):
        return self._creation_time

    @property
    def inviter_oid(self):
        return self._inviter_oid

    @property
    def invitee_oid(self):
        return self._invitee_oid

    @property
    def list_oid(self):
        return self._list_oid

    @property
    def message(self):
        return self._message

    def __str__(self):
        return f'{self.creation_time}: "{self.list_oid}"'

    @staticmethod
    def find(sirope: sirope.Sirope, oid: int) -> "InviteDTO":
        return sirope.find_first(InviteDTO, lambda l: l.oid == oid)

    def find_for_user(sirope: sirope.Sirope, user_oid: int) -> ["InviteDTO"]:
        return [
            item
            for item in sirope.filter(InviteDTO, lambda l: user_oid == l.invitee_oid)
        ]
