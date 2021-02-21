from enum import Enum


class Status(Enum):
    RESPONSE = 'response'
    REQUEST = 'request'
    MESSAGE = 'mess'

    def __get__(self, instance, owner):
        return self.value
