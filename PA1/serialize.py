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

from message import Message  # our custom message in native format
import MessageNamespace.Message as msg   # this is the generated code by the flatc compiler

# This is the method we will invoke from our driver program
# Note that if you have have multiple different message types, we could have
# separate such serialize/deserialize methods, or a single method can check what
# type of message it is and accordingly take actions.
def serialize (cm):
    # first obtain the builder object that is used to create an in-memory representation
    # of the serialized object from the custom message
    builder = flatbuffers.Builder(0);

    # create the name string for the name field using
    # the parameter we passed
    content_field = builder.CreateString (cm.content)
    
    # let us create the serialized msg by adding contents to it.
    # Our custom msg consists of a seq num, timestamp, name, and an array of uint32s
    msg.Start (builder)  # serialization starts with the "Start" method
    msg.AddType (builder, cm.type)
    msg.AddContent (builder, content_field)  # serialize the name
    serialized_msg = msg.End (builder)  # get the topic of all these fields

    # end the serialization process
    builder.Finish (serialized_msg)

    # get the serialized buffer
    buf = builder.Output ()

    # return this serialized buffer to the caller
    return buf

# serialize the custom message to iterable frame objects needed by zmq
def serialize_to_frames (cm):
  """ serialize into an interable format """
  # We had to do it this way because the send_serialized method of zmq under the hood
  # relies on send_multipart, which needs a list or sequence of frames. The easiest way
  # to get an iterable out of the serialized buffer is to enclose it inside []
  return [serialize (cm)]
  
  
# deserialize the incoming serialized structure into native data type
def deserialize (buf):
    cm = Message ()
    
    packet = msg.Message.GetRootAs (buf, 0)

    # sequence number
    cm.type = packet.Type ()

    # name received
    cm.content = packet.Content ()

    return cm
    
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
    
