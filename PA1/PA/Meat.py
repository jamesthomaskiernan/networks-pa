# automatically generated by the FlatBuffers compiler, do not modify

# namespace: PA

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class Meat(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Meat()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsMeat(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # Meat
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Meat
    def Type(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # Meat
    def Quantity(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

def MeatStart(builder):
    builder.StartObject(2)

def Start(builder):
    MeatStart(builder)

def MeatAddType(builder, type):
    builder.PrependInt32Slot(0, type, 0)

def AddType(builder, type):
    MeatAddType(builder, type)

def MeatAddQuantity(builder, quantity):
    builder.PrependFloat32Slot(1, quantity, 0.0)

def AddQuantity(builder, quantity):
    MeatAddQuantity(builder, quantity)

def MeatEnd(builder):
    return builder.EndObject()

def End(builder):
    return MeatEnd(builder)
