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


# manual python representation
from message import MessageType
from message import Message
from message import ResponseContents, HealthContents, OrderContents
from message import Code

# flatbuffer compiled representation
import PA.Message as pamsg   # this is the generated code by the flatc compiler
import PA.HealthContents as pahcontents
import PA.OrderContents as paocontents
import PA.ResponseContents as parcontents

def serialize(curmsg):
  builder = flatbuffers.Builder(0)

  ser_contents = None
  
  # IF RESPONSE MESSAGE
  if curmsg.type == MessageType.RESPONSE:
    
    contents_field = builder.CreateString(curmsg.contents.contents) # contents is string
    # Serialize response contents
    parcontents.Start (builder)
    parcontents.AddCode(builder, curmsg.contents.code)
    parcontents.AddContents(builder, contents_field)
    ser_contents = parcontents.End (builder)
  
  # IF HEALTH MESSAGE
  elif curmsg.type == MessageType.HEALTH:
    contents_field = builder.CreateString(curmsg.contents.contents) # contents is string
    # Serialize response contents
    pahcontents.Start (builder)
    pahcontents.AddSensorStatus(builder, curmsg.contents.sensor_status)
    pahcontents.AddDispenser(builder, curmsg.contents.dispenser)
    pahcontents.AddContents(builder, contents_field)
    ser_contents = pahcontents.End (builder)

  # IF ORDER MESSAGE
  elif curmsg.type == MessageType.ORDER:
    contents_field = builder.CreateString(curmsg.contents.contents) # contents is string
    # Serialize response contents
    paocontents.Start (builder)
    paocontents.AddContents(builder, contents_field)
    ser_contents = paocontents.End (builder)

  # Start building the Message
  pamsg.Start(builder)
  pamsg.AddType(builder, curmsg.type)
  pamsg.AddContents(builder, ser_contents)
  serialized_message = pamsg.End(builder)

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
  
  
def deserialize (buf):
    # Native format
    result = Message()
    
    # Flatbuf formatted message from serialized buffer
    deser_msg = pamsg.Message.GetRootAs(buf, 0)

    # Message type
    result.type = deser_msg.Type()

    # RESPONSE MESSAGE
    if deser_msg.Type() == MessageType.RESPONSE:

      # Apparently you have to initialize a flatbuffer object from nested tables to get 
      # the inner attributes
      deser_rcontents = parcontents.ResponseContents()
      deser_rcontents.Init(deser_msg.Contents().Bytes, deser_msg.Contents().Pos)

      result.contents = ResponseContents()
      result.contents.code = deser_rcontents.Code()
      result.contents.contents = deser_rcontents.Contents()
    
    # HEALTH MESSAGE
    elif deser_msg.Type() == MessageType.HEALTH:
      deser_hcontents = pahcontents.HealthContents()
      deser_hcontents.Init(deser_msg.Contents().Bytes, deser_msg.Contents().Pos)
      
      result.contents = HealthContents()
      result.contents.contents = deser_hcontents.Contents()
      result.contents.sensor_status = deser_hcontents.SensorStatus()
      result.contents.dispenser = deser_hcontents.Dispenser()


    # ORDER MESSAGE
    elif deser_msg.Type() == MessageType.ORDER:
      deser_ocontents = paocontents.OrderContents()
      deser_ocontents.Init(deser_msg.Contents().Bytes, deser_msg.Contents().Pos)

      result.contents = OrderContents()
      result.contents.contents = deser_ocontents.Contents()

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
    
