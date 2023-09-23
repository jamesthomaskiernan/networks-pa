from dataclasses import dataclass
from enum import IntEnum

class MessageType (IntEnum):
  ORDER = 0,
  HEALTH = 1
  RESPONSE = 2

@dataclass
class Message:
  type: MessageType  # type of message (ORDER = 0, HEALTH = 1, RESPONSE = 2)
  contents: str # content of message

  def __init__ (self):
    pass
  
  def dump (self):
    print ("Dumping contents of message:")
    print ("MessageType: {}".format (self.type))
    print ("Content: {}".format (self.contents))