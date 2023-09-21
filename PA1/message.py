from dataclasses import dataclass
from enum import Enum
import json

@dataclass
class Message:
  type: int  # type of message (ORDER = 0, HEALTH = 1, RESPONSE = 2)
  content: str # content of message

  def __init__ (self):
    pass
  
  def dump (self):
    print ("Dumping contents of message:")
    print("type: " + str(self.type))
    print ("content: " + str(self.content))