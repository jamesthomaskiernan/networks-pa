from dataclasses import dataclass
from enum import IntEnum


@dataclass
class Contents:
  def __init__ (self):
    pass

# RESPONSE

class Code(IntEnum):
  OK = 0,
  BAD_REQUEST = 1

@dataclass
class ResponseContents(Contents):
  code: Code
  contents: str # content of message
  
  def __init__ (self):
    pass

# HEALTH

class Status(IntEnum):
  GOOD = 0,
  BAD = 1

class Dispenser(IntEnum):
  OPTIMAL = 0,
  PARTIAL = 1,
  BLOCKAGE = 2

@dataclass
class HealthContents(Contents):
  dispenser: Dispenser
  icemaker: int
  lightbulb: Status
  fridge_temp: int
  freezer_temp: int
  sensor_status: Status

  def __init__ (self):
    pass

# ORDER

@dataclass
class OrderContents(Contents):
  contents: str # content of message

  def __init__ (self):
    pass

# MESSAGE (ROOT)

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