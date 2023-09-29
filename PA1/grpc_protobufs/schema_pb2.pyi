from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Code(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    OK: _ClassVar[Code]
    BAD_REQUEST: _ClassVar[Code]

class MilkType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    ONEPERCENT: _ClassVar[MilkType]
    TWOPERCENT: _ClassVar[MilkType]
    FATFREE: _ClassVar[MilkType]
    WHOLE: _ClassVar[MilkType]
    ALMOND: _ClassVar[MilkType]
    CASHEW: _ClassVar[MilkType]
    OAT: _ClassVar[MilkType]

class BreadType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    WHOLEWHEAT: _ClassVar[BreadType]
    WHITE: _ClassVar[BreadType]
    BUTTERMILK: _ClassVar[BreadType]
    RYE: _ClassVar[BreadType]

class MeatType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    CHICKEN: _ClassVar[MeatType]
    BEEF: _ClassVar[MeatType]
    PORK: _ClassVar[MeatType]
    TURKEY: _ClassVar[MeatType]

class Dispenser(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    OPTIMAL: _ClassVar[Dispenser]
    PARTIAL: _ClassVar[Dispenser]
    BLOCKAGE: _ClassVar[Dispenser]

class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    GOOD: _ClassVar[Status]
    BAD: _ClassVar[Status]

class MessageType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    ORDER: _ClassVar[MessageType]
    HEALTH: _ClassVar[MessageType]
    RESPONSE: _ClassVar[MessageType]
OK: Code
BAD_REQUEST: Code
ONEPERCENT: MilkType
TWOPERCENT: MilkType
FATFREE: MilkType
WHOLE: MilkType
ALMOND: MilkType
CASHEW: MilkType
OAT: MilkType
WHOLEWHEAT: BreadType
WHITE: BreadType
BUTTERMILK: BreadType
RYE: BreadType
CHICKEN: MeatType
BEEF: MeatType
PORK: MeatType
TURKEY: MeatType
OPTIMAL: Dispenser
PARTIAL: Dispenser
BLOCKAGE: Dispenser
GOOD: Status
BAD: Status
ORDER: MessageType
HEALTH: MessageType
RESPONSE: MessageType

class ResponseContents(_message.Message):
    __slots__ = ["code", "contents"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    CONTENTS_FIELD_NUMBER: _ClassVar[int]
    code: Code
    contents: str
    def __init__(self, code: _Optional[_Union[Code, str]] = ..., contents: _Optional[str] = ...) -> None: ...

class Veggies(_message.Message):
    __slots__ = ["tomato", "cucumber", "broccoli", "potato", "carrot"]
    TOMATO_FIELD_NUMBER: _ClassVar[int]
    CUCUMBER_FIELD_NUMBER: _ClassVar[int]
    BROCCOLI_FIELD_NUMBER: _ClassVar[int]
    POTATO_FIELD_NUMBER: _ClassVar[int]
    CARROT_FIELD_NUMBER: _ClassVar[int]
    tomato: float
    cucumber: float
    broccoli: float
    potato: float
    carrot: float
    def __init__(self, tomato: _Optional[float] = ..., cucumber: _Optional[float] = ..., broccoli: _Optional[float] = ..., potato: _Optional[float] = ..., carrot: _Optional[float] = ...) -> None: ...

class Cans(_message.Message):
    __slots__ = ["coke", "beer", "pepsi"]
    COKE_FIELD_NUMBER: _ClassVar[int]
    BEER_FIELD_NUMBER: _ClassVar[int]
    PEPSI_FIELD_NUMBER: _ClassVar[int]
    coke: int
    beer: int
    pepsi: int
    def __init__(self, coke: _Optional[int] = ..., beer: _Optional[int] = ..., pepsi: _Optional[int] = ...) -> None: ...

class Bottles(_message.Message):
    __slots__ = ["sprite", "fanta", "dietcoke"]
    SPRITE_FIELD_NUMBER: _ClassVar[int]
    FANTA_FIELD_NUMBER: _ClassVar[int]
    DIETCOKE_FIELD_NUMBER: _ClassVar[int]
    sprite: int
    fanta: int
    dietcoke: int
    def __init__(self, sprite: _Optional[int] = ..., fanta: _Optional[int] = ..., dietcoke: _Optional[int] = ...) -> None: ...

class Drinks(_message.Message):
    __slots__ = ["cans", "bottles"]
    CANS_FIELD_NUMBER: _ClassVar[int]
    BOTTLES_FIELD_NUMBER: _ClassVar[int]
    cans: Cans
    bottles: Bottles
    def __init__(self, cans: _Optional[_Union[Cans, _Mapping]] = ..., bottles: _Optional[_Union[Bottles, _Mapping]] = ...) -> None: ...

class Milk(_message.Message):
    __slots__ = ["type", "quantity"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    type: MilkType
    quantity: float
    def __init__(self, type: _Optional[_Union[MilkType, str]] = ..., quantity: _Optional[float] = ...) -> None: ...

class Bread(_message.Message):
    __slots__ = ["type", "quantity"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    type: BreadType
    quantity: int
    def __init__(self, type: _Optional[_Union[BreadType, str]] = ..., quantity: _Optional[int] = ...) -> None: ...

class Meat(_message.Message):
    __slots__ = ["type", "quantity"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    type: MeatType
    quantity: float
    def __init__(self, type: _Optional[_Union[MeatType, str]] = ..., quantity: _Optional[float] = ...) -> None: ...

class OrderContents(_message.Message):
    __slots__ = ["veggies", "drinks", "milk", "bread", "meat"]
    VEGGIES_FIELD_NUMBER: _ClassVar[int]
    DRINKS_FIELD_NUMBER: _ClassVar[int]
    MILK_FIELD_NUMBER: _ClassVar[int]
    BREAD_FIELD_NUMBER: _ClassVar[int]
    MEAT_FIELD_NUMBER: _ClassVar[int]
    veggies: Veggies
    drinks: Drinks
    milk: _containers.RepeatedCompositeFieldContainer[Milk]
    bread: _containers.RepeatedCompositeFieldContainer[Bread]
    meat: _containers.RepeatedCompositeFieldContainer[Meat]
    def __init__(self, veggies: _Optional[_Union[Veggies, _Mapping]] = ..., drinks: _Optional[_Union[Drinks, _Mapping]] = ..., milk: _Optional[_Iterable[_Union[Milk, _Mapping]]] = ..., bread: _Optional[_Iterable[_Union[Bread, _Mapping]]] = ..., meat: _Optional[_Iterable[_Union[Meat, _Mapping]]] = ...) -> None: ...

class HealthContents(_message.Message):
    __slots__ = ["dispenser", "icemaker", "lightbulb", "fridge_temp", "freezer_temp", "sensor_status"]
    DISPENSER_FIELD_NUMBER: _ClassVar[int]
    ICEMAKER_FIELD_NUMBER: _ClassVar[int]
    LIGHTBULB_FIELD_NUMBER: _ClassVar[int]
    FRIDGE_TEMP_FIELD_NUMBER: _ClassVar[int]
    FREEZER_TEMP_FIELD_NUMBER: _ClassVar[int]
    SENSOR_STATUS_FIELD_NUMBER: _ClassVar[int]
    dispenser: Dispenser
    icemaker: int
    lightbulb: Status
    fridge_temp: int
    freezer_temp: int
    sensor_status: Status
    def __init__(self, dispenser: _Optional[_Union[Dispenser, str]] = ..., icemaker: _Optional[int] = ..., lightbulb: _Optional[_Union[Status, str]] = ..., fridge_temp: _Optional[int] = ..., freezer_temp: _Optional[int] = ..., sensor_status: _Optional[_Union[Status, str]] = ...) -> None: ...

class Message(_message.Message):
    __slots__ = ["type", "health_contents", "order_contents", "response_contents"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    HEALTH_CONTENTS_FIELD_NUMBER: _ClassVar[int]
    ORDER_CONTENTS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_CONTENTS_FIELD_NUMBER: _ClassVar[int]
    type: MessageType
    health_contents: HealthContents
    order_contents: OrderContents
    response_contents: ResponseContents
    def __init__(self, type: _Optional[_Union[MessageType, str]] = ..., health_contents: _Optional[_Union[HealthContents, _Mapping]] = ..., order_contents: _Optional[_Union[OrderContents, _Mapping]] = ..., response_contents: _Optional[_Union[ResponseContents, _Mapping]] = ...) -> None: ...
