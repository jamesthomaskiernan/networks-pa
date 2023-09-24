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
from message import Veggies, Cans, Drinks, Bottles, Meat, Milk, Bread

# flatbuffer compiled representation
import PA.Message as pamsg   # this is the generated code by the flatc compiler
import PA.HealthContents as pahcontents
import PA.OrderContents as paocontents
import PA.ResponseContents as parcontents
import PA.Veggies as paveggies
import PA.Drinks as padrinks
import PA.Bottles as pabottles
import PA.Cans as pacans
import PA.Meat as pameat
import PA.Milk as pamilk
import PA.Bread as pabread

def serialize(curmsg):
  builder = flatbuffers.Builder(0)

  ser_contents = None
  
  # ----response message----
  if curmsg.type == MessageType.RESPONSE:
    
    # first make content string
    contents_field = builder.CreateString(curmsg.contents.contents) # contents is string
    
    # then add all fields
    parcontents.Start (builder)
    parcontents.AddCode(builder, curmsg.contents.code)
    parcontents.AddContents(builder, contents_field)
    ser_contents = parcontents.End (builder)
  
  # ----health message----
  elif curmsg.type == MessageType.HEALTH:
    pahcontents.Start (builder)
    pahcontents.AddDispenser(builder, curmsg.contents.dispenser)
    pahcontents.AddIcemaker(builder, curmsg.contents.icemaker)
    pahcontents.AddLightbulb(builder, curmsg.contents.lightbulb)
    pahcontents.AddFridgeTemp(builder, curmsg.contents.fridge_temp)
    pahcontents.AddFreezerTemp(builder, curmsg.contents.freezer_temp)
    pahcontents.AddSensorStatus(builder, curmsg.contents.sensor_status)
    ser_contents = pahcontents.End (builder)

  # ----order message----
  elif curmsg.type == MessageType.ORDER:
    
    # serialize veggies
    paveggies.Start(builder)
    paveggies.AddTomato(builder, curmsg.contents.veggies.tomato)
    paveggies.AddCucumber(builder, curmsg.contents.veggies.cucumber)
    paveggies.AddBroccoli(builder, curmsg.contents.veggies.broccoli)
    paveggies.AddPotato(builder, curmsg.contents.veggies.potato)
    paveggies.AddCarrot(builder, curmsg.contents.veggies.carrot)
    ser_veggies = paveggies.End(builder)
    
    # serialize cans
    pacans.Start(builder)
    pacans.AddBeer(builder, curmsg.contents.drinks.cans.beer)
    pacans.AddCoke(builder, curmsg.contents.drinks.cans.coke)
    pacans.AddPepsi(builder, curmsg.contents.drinks.cans.pepsi)
    ser_cans = pacans.End(builder)

    # serialize bottles
    pabottles.Start(builder)
    pabottles.AddDietcoke(builder, curmsg.contents.drinks.bottles.dietcoke)
    pabottles.AddFanta(builder, curmsg.contents.drinks.bottles.fanta)
    pabottles.AddSprite(builder, curmsg.contents.drinks.bottles.sprite)
    ser_bottles = pabottles.End(builder)

    # serialize drinks
    padrinks.Start(builder)
    padrinks.AddBottles(builder, ser_bottles)
    padrinks.AddCans(builder, ser_cans)
    ser_drinks = padrinks.End(builder)

    # Meat

    # serialize each meat, and put it into an array
    ser_meat = []
    for i in range(len(curmsg.contents.meat)):
      pameat.Start(builder)
      pameat.AddQuantity(builder, curmsg.contents.meat[i].quantity)
      pameat.AddType(builder, curmsg.contents.meat[i].type)
      ser_meat.append(pameat.End(builder))

    # serialize meat list and add it to contents
    paocontents.StartMeatVector(builder, len (curmsg.contents.meat))
    for i in reversed (range (len (curmsg.contents.meat))):
      builder.PrependUOffsetTRelative(ser_meat[i])
    ser_meat_list = builder.EndVector()

    # Milk

    # serialize each milk, and put it into an array
    ser_milk = []
    for i in range(len(curmsg.contents.milk)):
      pamilk.Start(builder)
      pamilk.AddQuantity(builder, curmsg.contents.milk[i].quantity)
      pamilk.AddType(builder, curmsg.contents.milk[i].type)
      ser_milk.append(pamilk.End(builder))

    # serialize milk list and add it to contents
    paocontents.StartMilkVector(builder, len (curmsg.contents.milk))
    for i in reversed (range (len (curmsg.contents.milk))):
      builder.PrependUOffsetTRelative(ser_milk[i])
    ser_milk_list = builder.EndVector()

    # Bread

    # serialize each bread, and put it into an array
    ser_bread = []
    for i in range(len(curmsg.contents.bread)):
      pabread.Start(builder)
      pabread.AddQuantity(builder, curmsg.contents.bread[i].quantity)
      pabread.AddType(builder, curmsg.contents.bread[i].type)
      ser_bread.append(pabread.End(builder))

    # serialize bread list and add it to contents
    paocontents.StartBreadVector(builder, len (curmsg.contents.bread))
    for i in reversed (range (len (curmsg.contents.bread))):
      builder.PrependUOffsetTRelative(ser_bread[i])
    ser_bread_list = builder.EndVector()

    # serialize all order contents
    paocontents.Start(builder)
    paocontents.AddMeat(builder, ser_meat_list)
    paocontents.AddMilk(builder, ser_milk_list)
    paocontents.AddBread(builder, ser_bread_list)
    paocontents.AddVeggies(builder, ser_veggies)
    paocontents.AddDrinks(builder, ser_drinks)
    ser_contents = paocontents.End(builder)

  # start building the Message
  pamsg.Start(builder)
  pamsg.AddType(builder, curmsg.type)
  pamsg.AddContents(builder, ser_contents)
  serialized_message = pamsg.End(builder)

  # finish building the message
  builder.Finish(serialized_message)

  # get the serialized buffer
  buf = builder.Output()

  # return the serialized buffer to the caller
  return buf



# serialize the custom message to iterable frame objects needed by zmq
def serialize_to_frames (cm):
  """ serialize into an interable format """
  # We had to do it this way because the send_serialized method of zmq under the hood
  # relies on send_multipart, which needs a list or sequence of frames. The easiest way
  # to get an iterable out of the serialized buffer is to enclose it inside []
  return [serialize (cm)]
  
  
def deserialize (buf):
    # native format
    result = Message()
    
    # flatbuf formatted message from serialized buffer
    deser_msg = pamsg.Message.GetRootAs(buf, 0)

    # message type
    result.type = deser_msg.Type()

    # ----response message----
    if deser_msg.Type() == MessageType.RESPONSE:
      deser_rcontents = parcontents.ResponseContents()
      deser_rcontents.Init(deser_msg.Contents().Bytes, deser_msg.Contents().Pos) # DON'T FORGET INIT!

      result.contents = ResponseContents()
      result.contents.code = deser_rcontents.Code()
      result.contents.contents = deser_rcontents.Contents()
    
    # ----health message----
    elif deser_msg.Type() == MessageType.HEALTH:
      deser_hcontents = pahcontents.HealthContents()
      deser_hcontents.Init(deser_msg.Contents().Bytes, deser_msg.Contents().Pos)
      
      result.contents = HealthContents()
      result.contents.sensor_status = deser_hcontents.SensorStatus()
      result.contents.dispenser = deser_hcontents.Dispenser()
      result.contents.lightbulb = deser_hcontents.Lightbulb()
      result.contents.fridge_temp = deser_hcontents.FridgeTemp()
      result.contents.freezer_temp = deser_hcontents.FreezerTemp()
      result.contents.icemaker = deser_hcontents.Icemaker()

    # ----order message----
    elif deser_msg.Type() == MessageType.ORDER:
      deser_ocontents = paocontents.OrderContents()
      deser_ocontents.Init(deser_msg.Contents().Bytes, deser_msg.Contents().Pos)

      # deserialize order contents
      result.contents = OrderContents()
      
      # deserialize veggies
      v = deser_ocontents.Veggies()
      result.contents.veggies = Veggies()
      result.contents.veggies.tomato = v.Tomato()
      result.contents.veggies.cucumber = v.Cucumber()
      result.contents.veggies.broccoli = v.Broccoli()
      result.contents.veggies.potato = v.Potato()
      result.contents.veggies.carrot = v.Carrot()
      
      # deserialize drinks
      d = deser_ocontents.Drinks()
      result.contents.drinks = Drinks()

      # deserialize cans
      cans = d.Cans()
      result.contents.drinks.cans = Cans()
      result.contents.drinks.cans.beer = cans.Beer()
      result.contents.drinks.cans.coke = cans.Coke()
      result.contents.drinks.cans.pepsi = cans.Pepsi()

      # deserialize bottles
      bottles = d.Bottles()
      result.contents.drinks.bottles = Bottles()
      result.contents.drinks.bottles.dietcoke = bottles.Dietcoke()
      result.contents.drinks.bottles.fanta = bottles.Fanta()
      result.contents.drinks.bottles.sprite = bottles.Sprite()

      # deserialize meat
      meat_list = []
      for i in range(deser_ocontents.MeatLength()):
          pameatitem = deser_ocontents.Meat(i)
          meat_item = Meat()
          meat_item.quantity = pameatitem.Quantity()
          meat_item.type = pameatitem.Type()
          meat_list.append(meat_item)
      result.contents.meat = meat_list

      # deserialize milk
      milk_list = []
      for i in range(deser_ocontents.MilkLength()):
          pamilkitem = deser_ocontents.Milk(i)
          milk_item = Milk()
          milk_item.quantity = pamilkitem.Quantity()
          milk_item.type = pamilkitem.Type()
          milk_list.append(milk_item)
      result.contents.milk = milk_list

      # deserialize bread
      bread_list = []
      for i in range(deser_ocontents.BreadLength()):
          pabreaditem = deser_ocontents.Bread(i)
          bread_item = Bread()
          bread_item.quantity = pabreaditem.Quantity()
          bread_item.type = pabreaditem.Type()
          bread_list.append(bread_item)
      result.contents.bread = bread_list

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
    
