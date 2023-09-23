from dataclasses import dataclass
from enum import IntEnum

class Code (IntEnum):
  OK = 0,
  BAD_REQUEST = 1

@dataclass
class Contents:
  def __init__ (self):
    pass


@dataclass
class ResponseContents(Contents):
  contents: str # content of message
  code: Code
  def __init__ (self):
    pass


@dataclass
class HealthContents(Contents):
  contents: str # content of message

  def __init__ (self):
    pass


@dataclass
class OrderContents(Contents):
  contents: str # content of message

  def __init__ (self):
    pass


class MessageType (IntEnum):
  ORDER = 0,
  HEALTH = 1
  RESPONSE = 2

@dataclass
class Message:
  type: MessageType  # type of message (ORDER = 0, HEALTH = 1, RESPONSE = 2)
  contents: Contents

  def __init__ (self):
    self.contents = ResponseContents()
    self.type = MessageType.RESPONSE
  
  def dump(self):
    print("Dumping contents of message:")
    print("MessageType: {}".format(self.type))
    print("Content: ", self.contents)
    
    
    # if self.type == MessageType.RESPONSE:
    #     print("Content: {}".format(self.contents.contents))

    # elif self.type == MessageType.HEALTH:
    #     print("Content: {}".format(self.contents.contents))

    # elif self.type == MessageType.ORDER:
    #     print("Content: {}".format(self.contents.contents))