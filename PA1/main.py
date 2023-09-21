from fridge import Fridge # fridge client
from message import Message # our custom message in native format
import time # use this to measure time it takes to send messages
import random

# create fridge object (on init, it makes context on sockets for both servers)
fridge = Fridge()

# connect fridge to both servers
fridge.connect(fridge.grocery_socket, 5555, "127.0.0.1")
print("Fridge connected to grocery server.")
fridge.connect(fridge.health_socket, 4444, "127.0.0.1")
print("Fridge connected to health server.")

# use this to keep track of time to send/receive messages
roundtrip_times_zmpq = []

# send some arbitrary number of messages
for i in range(0, 100):

    # find random num, if it's 1, we send health message, else grocery message
    # means ~25% of messages will be health messages
    
    # send health message
    if random.randint(1, 4) == 1:
        
        # create message, set some arbitrary content
        msg = Message()
        msg.type = 5
        msg.content = "Hello! This is a message for the health server!"
        
        # time how long it takes
        start_time = time.time () * 1000 # multiply by 1000 to get ms
        print("Sending message to health server.")
        fridge.send_message(fridge.health_socket, msg)
        msg = fridge.receive_message(fridge.health_socket)
        end_time = time.time () * 1000
        roundtrip_times_zmpq.append(end_time - start_time)
        
    # send grocery message
    else:

        # create message, set some arbitrary content
        msg = Message()
        msg.type = 5
        msg.content = "Hello! This is a message for the grocery server!"
        
        # time how long it takes
        start_time = time.time () * 1000 # multiply by 1000 to get ms
        print("Sending message to grocery server.")
        fridge.send_message(fridge.grocery_socket, msg)
        msg = fridge.receive_message(fridge.grocery_socket)
        end_time = time.time () * 1000
        roundtrip_times_zmpq.append(end_time - start_time)

avg = sum(roundtrip_times_zmpq) / len(roundtrip_times_zmpq)
print("Average roundtrip time to both servers with ZMQ: " + str(avg) + "ms")