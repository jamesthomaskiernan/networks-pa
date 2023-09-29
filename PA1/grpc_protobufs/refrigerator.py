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

# imports for sending the message
from declarations import MessageType

  
########################
# Command line parsing #
########################
def parseCmdLineArgs ():
  # parse the command line
  parser = argparse.ArgumentParser ()

  # add optional arguments
  parser.add_argument ("-i", "--iters", type=int, default=10, help="Number of iterations to run (default: 10)")
  parser.add_argument ("-l", "--veclen", type=int, default=20, help="Length of the vector field (default: 20; contents are irrelevant)")
  parser.add_argument ("-n", "--name", default="ProtoBuf gRPC Demo", help="Name to include in each message")
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
  print(parsed_args)
    
  # driver (parsed_args.name, parsed_args.iters, parsed_args.veclen, parsed_args.port)

  print("Refrigerator starting...")
  try:

    # Use the insecure channel to establish connection with server
    channel = grpc.insecure_channel ("localhost:" + str (parsed_args.port))

    # Obtain a proxy object to the server
    stub = spb_grpc.DummyServiceStub (channel)
    print ("Refrigerator has connected to health server.")

    req = spb.Request ()

    # now send i messages
    for i in range (parsed_args.iters):

      req.type = 3
      resp = stub.method (req)
      print(resp)
      print(resp)

      time.sleep (0.050)  # 50 msec

  except:
    return

main()