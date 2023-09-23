import os
import sys

# IMPORTANT !
# this is needed to tell python where to find the flatbuffers package
# make sure to change this path to where you have compiled and installed
# flatbuffers.  If the python package is installed in your system wide files
# or virtualenv, then this may not be needed

sys.path.append(os.path.join (os.path.dirname(__file__), '/home/user/Apps/flatbuffers/python')) # UPDATE THIS TO YOUR OWN DIRECTORY!
import flatbuffers    # this is the flatbuffers package we import

import time   # we need this get current time
import numpy as np  # to use in our vector field

import zmq   # we need this for additional constraints provided by the zmq serialization


from message import MessageType
from message import Message
import MessageNamespace.Message as msgCompiled   # this is the generated code by the flatc compiler


def serialize(curmsg):
  builder = flatbuffers.Builder(0)

  # Serialize the content field
  contents_field = builder.CreateString(curmsg.contents)

  # Start building the Message
  msgCompiled.Start(builder)
  msgCompiled.AddType(builder, curmsg.type)
  msgCompiled.AddContents(builder, contents_field)
  serialized_message = msgCompiled.End(builder)

  # Finish building the message
  builder.Finish(serialized_message)

  # Get the serialized buffer
  buf = builder.Output()

  # Return the serialized buffer to the caller
  return buf



# serialize the custom message to iterable frame objects needed by zmq
def serialize_to_frames (cm):
  """ serialize into an interable format """
  # We had to do it this way because the send_serialized method of zmq under the hood
  # relies on send_multipart, which needs a list or sequence of frames. The easiest way
  # to get an iterable out of the serialized buffer is to enclose it inside []
  return [serialize (cm)]
  
  
def deserialize(buf):

  result = Message()
  packet = msgCompiled.Message.GetRootAs(buf, 0)
  
  # Create a native Python Message object and populate it
  result.type = MessageType(packet.Type())
  result.contents = packet.Contents()

  return result

# deserialize from frames
def deserialize_from_frames (recvd_seq):
  """ This is invoked on list of frames by zmq """

  # For this sample code, since we send only one frame, hopefully what
  # comes out is also a single frame. If not some additional complexity will
  # need to be added.
  assert (len (recvd_seq) == 1)
  #print ("type of each elem of received seq is {}".format (type (recvd_seq[i])))
  # print ("received data over the wire = {}".format (recvd_seq[0]))
  cm = deserialize (recvd_seq[0])  # hand it to our deserialize method

  # assuming only one frame in the received sequence, we just send this deserialized
  # custom message
  return cm
    
