from enum import Enum


class Setting(Enum):
    HEADER_SIZE = 8
    PACKAGE_SIZE = 40
    SET_NAME = 1
    SET_CHAT_NAME = 2
    MESSAGE = 3
    
    def __get__(self, instance, owner):
        return int('%s' % self.value)
