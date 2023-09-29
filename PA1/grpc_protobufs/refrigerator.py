# The different packages we need in this Python driver code
import os
import sys
import time  # needed for timing measurements and sleep

import random  # random number generator
import argparse  # argument parser

import logging

import grpc   # for gRPC

# import generated packages
import schema_pb2 as spb
import schema_pb2_grpc as spb_grpc
  
########################
# Command line parsing #
########################
def parseCmdLineArgs ():
  # parse the command line
  parser = argparse.ArgumentParser ()

  # add optional arguments
  parser.add_argument ("-i", "--iters", type=int, default=10, help="Number of iterations to run (default: 10)")
  parser.add_argument ("-p", "--port", type=int, default=5577, help="Port where the server part of the peer listens and client side connects to (default: 5577)")
  
  # parse the args
  args = parser.parse_args ()

  return args
    

###############
# Main Driver #
###############
def main ():

  # first parse the command line args
  parsed_args = parseCmdLineArgs ()

  # start client
  print("Refrigerator starting...")
  
  try:

    # use the insecure channel to establish connection with server
    channel = grpc.insecure_channel ("localhost:" + str (parsed_args.port))

    # obtain a proxy object to the server
    stub = spb_grpc.DummyServiceStub (channel)
    print ("Refrigerator has connected to grocery server.")

    # use this to keep track of time to send/receive messages
    roundtrip_times_grpc = []

    # send i message (amount specific by user args)
    for i in range (parsed_args.iters):
      
      # send health message (should be ~25% of messages, rest will be orders)
      if random.randint(1, 4) == 1:
        
        pass # TODO: send message to health server here
          
      # send grocery message
      else:

        # fill request with data        
        ordercontents = spb.OrderContents()
        
        # add veggies
        v = spb.Veggies()
        v.broccoli = 0
        v.carrot = 4
        v.cucumber = 9
        v.potato = 2
        v.tomato = 1
        ordercontents.veggies.CopyFrom(v)

        # add drinks
        d = spb.Drinks()

        # add bottles
        b = spb.Bottles()
        b.sprite = 2
        b.fanta = 4
        b.dietcoke = 2
        d.bottles.CopyFrom(b)

        # add cans
        c = spb.Cans()
        c.coke = 2
        c.beer = 12
        c.pepsi = 0
        d.cans.CopyFrom(c)

        ordercontents.drinks.CopyFrom(d)
        
        # add meat
        meat1 = spb.Meat()
        meat1.type = spb.MeatType.CHICKEN
        meat1.quantity = 5
        meat2 = spb.Meat()
        meat2.type = spb.MeatType.BEEF
        meat2.quantity = 2
        meat3 = spb.Meat()
        meat3.type = spb.MeatType.TURKEY
        meat3.quantity = 1
        ordercontents.meat.append(meat1)
        ordercontents.meat.append(meat2)
        ordercontents.meat.append(meat3)

        # add milk
        milk1 = spb.Milk()
        milk1.type = spb.MilkType.ALMOND
        milk1.quantity = 2
        milk2 = spb.Milk()
        milk2.type = spb.MilkType.OAT
        milk2.quantity = 1
        ordercontents.milk.append(milk1)
        ordercontents.milk.append(milk2)

        # add bread
        bread1 = spb.Bread()
        bread1.type = spb.BreadType.WHITE
        bread1.quantity = 1
        bread2 = spb.Bread()
        bread2.type = spb.BreadType.RYE
        bread2.quantity = 3
        ordercontents.bread.append(bread1)
        ordercontents.bread.append(bread2)

        # set order contents on a new message        
        req = spb.Message()
        req.type = spb.MessageType.ORDER
        req.order_contents.CopyFrom(ordercontents)
        
        # send request and print response
        print("Sending message to grocery server.")
        start_time = time.time () * 1000 # multiply by 1000 to get ms
        resp = stub.method (req)
        end_time = time.time () * 1000
        roundtrip_times_grpc.append(end_time - start_time)
        
        # print response if you want
        print(resp)

    # once done sending message, print out time stats
    avg = sum(roundtrip_times_grpc) / len(roundtrip_times_grpc)
    print("Average roundtrip time to both servers with GRPC: " + str(avg) + "ms")

  except:
    return

main()