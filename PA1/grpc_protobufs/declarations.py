from enum import Enum


# using this enum when sending a message doesn't seem to work
class MessageType(Enum):
    ORDER = 0
    HEALTH = 1
    RESPONSE = 2
