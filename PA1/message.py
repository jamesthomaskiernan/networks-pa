from dataclasses import dataclass
from enum import IntEnum
import json

@dataclass
class Contents:
  def __init__ (self):
    pass

class Code (IntEnum):
  OK = 0,
  BAD_REQUEST = 1

@dataclass
class ResponseContents(Contents):
  code: Code  # type of message (ORDER = 0, HEALTH = 1, RESPONSE = 2)
  contents: str # content of message

  def __init__ (self):
    pass


class MessageType (IntEnum):
  ORDER = 0, 
  HEALTH = 1, 
  RESPONSE = 2 

@dataclass
class Message:
  type: MessageType  # type of message (ORDER = 0, HEALTH = 1, RESPONSE = 2)
  contents: Contents # content of message

  def __init__ (self):
    pass
  
  def dump (self):
    print ("Dumping contents of message:")
    print("type:", self.type)
    print ("content:", self.contents)