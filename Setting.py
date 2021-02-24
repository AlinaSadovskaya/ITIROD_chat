from enum import Enum


class Status(Enum):
    RESPONSE = 'response'
    REQUEST = 'request'
    MESSAGE = 'mess'
    HISTORY = 'history'

    def __get__(self, instance, owner):
        return self.value
