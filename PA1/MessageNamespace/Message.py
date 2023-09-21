# automatically generated by the FlatBuffers compiler, do not modify

# namespace: MessageNamespace

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class Message(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Message()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsMessage(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # Message
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Message
    def Type(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int8Flags, o + self._tab.Pos)
        return 0

    # Message
    def ContentsType(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, o + self._tab.Pos)
        return 0

    # Message
    def Contents(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            from flatbuffers.table import Table
            obj = Table(bytearray(), 0)
            self._tab.Union(obj, o)
            return obj
        return None

def MessageStart(builder):
    builder.StartObject(3)

def Start(builder):
    MessageStart(builder)

def MessageAddType(builder, type):
    builder.PrependInt8Slot(0, type, 0)

def AddType(builder, type):
    MessageAddType(builder, type)

def MessageAddContentsType(builder, contentsType):
    builder.PrependUint8Slot(1, contentsType, 0)

def AddContentsType(builder, contentsType):
    MessageAddContentsType(builder, contentsType)

def MessageAddContents(builder, contents):
    builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(contents), 0)

def AddContents(builder, contents):
    MessageAddContents(builder, contents)

def MessageEnd(builder):
    return builder.EndObject()

def End(builder):
    return MessageEnd(builder)
