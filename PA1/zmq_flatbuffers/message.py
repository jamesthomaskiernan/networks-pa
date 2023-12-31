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
class Cans: 
  coke:int
  beer:int
  pepsi:int
  
  def __init__ (self):
    pass

@dataclass
class Bottles: 
  sprite:int
  fanta:int
  dietcoke:int
  
  def __init__ (self):
    pass

@dataclass
class Drinks: 
  cans:Cans
  bottles:Bottles
  
  def __init__ (self):
    pass

@dataclass
class Veggies:
  tomato:float
  cucumber:float
  broccoli:float
  potato:float
  carrot:float
  
  def __init__ (self):
    pass

class MeatType(IntEnum):
  CHICKEN = 0,
  BEEF = 1,
  PORK = 2,
  TURKEY = 3

@dataclass
class Meat:
  type:MeatType
  quantity:float

  def __init__ (self):
    pass

class MilkType(IntEnum):
  ONEPERCENT = 0, 
  TWOPERCENT = 1, 
  FATFREE = 2, 
  WHOLE = 3, 
  ALMOND = 4, 
  CASHEW = 5, 
  OAT = 6

@dataclass
class Milk:
  type:MilkType
  quantity:float

  def __init__ (self):
    pass

class BreadType(IntEnum):
  WHOLEWHEAT = 0,
  WHITE = 1,
  BUTTERMILK = 2,
  RYE = 3

@dataclass
class Bread:
  type:BreadType
  quantity:int

  def __init__ (self):
    pass

@dataclass
class OrderContents(Contents):
  veggies:Veggies
  drinks:Drinks
  meat:list[Meat]
  milk:list[Milk]
  bread:list[Bread]

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