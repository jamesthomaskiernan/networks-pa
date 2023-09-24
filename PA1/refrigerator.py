# built in packages
import sys # for system exception
import zmq # this package must be imported for ZMQ to work
import argparse # for argument parsing
import random # to simulate messages 
import time # use this to measure time it takes to send messages

# files
import serialize as sz # this is from the file serialize.py in the same directory

# imports for message
from message import Message # our custom message in native format
from message import MessageType # enum, 0 1 2
from message import HealthContents, Status, Dispenser
from message import OrderContents, Veggies, Drinks, Bottles, Cans, Meat, MeatType, Milk, MilkType, Bread, BreadType


######################
# Refrigerator Class #
######################
class Refrigerator ():
    
    # initializer, starts refrigerator and connects to address/port
    def __init__(self):

        print("Refrigerator starting...")

        # class vars, updated below, listed here just for convenience
        self.context = None
        self.health_status_socket = None
        self.grocery_socket = None

		# establish context for refrigerator
        try:
            self.context = zmq.Context ()     # returns a singleton object
        except zmq.ZMQError as err:
            print ("ZeroMQ Error: {}".format (err))
            return
        except:
            print ("Some exception occurred getting context {}".format (sys.exc_info()[0]))
            return

		# establish socket for health server
        try:
            self.health_status_socket = self.context.socket (zmq.REQ)
        except zmq.ZMQError as err:
            print ("ZeroMQ Error obtaining context: {}".format (err))
            return
        except:
            print ("Some exception occurred getting REQ socket {}".format (sys.exc_info()[0]))
            return

		# establish socket for grocery server
        try:
            self.grocery_socket = self.context.socket (zmq.REQ)
        except zmq.ZMQError as err:
            print ("ZeroMQ Error obtaining context: {}".format (err))
            return
        except:
            print ("Some exception occurred getting REQ socket {}".format (sys.exc_info()[0]))
            return


    def connect(self, socket, port, address = "127.0.0.1"):
		
        # connect to server
        try:
            # as in a traditional socket, tell the system what IP addr and port are we
            # going to connect to. Here, we are using TCP sockets.
            connect_string = "tcp://" + address + ":" + str (port)
            print ("Refrigerator connecting to {}".format (connect_string))
            socket.connect (connect_string)
        except zmq.ZMQError as err:
            print ("ZeroMQ Error connecting REQ socket: {}".format (err))
            socket.close ()
            return
        except:
            print ("Some exception occurred connecting REQ socket {}".format (sys.exc_info()[0]))
            socket.close ()
            return

    # receive message back from server
    def receive_message(self, socket):
        try:
            # Note, in the following, if copy=False, then what is received is
            # a list of frames and not bytes
            cm = socket.recv_serialized (sz.deserialize_from_frames, copy=True)
            return cm
        except zmq.ZMQError as err:
            print ("ZeroMQ Error receiving serialized message: {}".format (err))
            raise
        except:
            print ("Some exception occurred with recv_serialized {}".format (sys.exc_info()[0]))
            raise

    # send message to server
    def send_message(self, socket, msg):
        try:
            socket.send_serialized (msg, sz.serialize_to_frames)
        except zmq.ZMQError as err:
            print ("ZeroMQ Error serializing request: {}".format (err))
            raise
        except:
            print ("Some exception occurred with send_serialized {}".format (sys.exc_info()[0]))
            raise


   
########################
# Command line parsing #
########################
def parseCmdLineArgs ():
    # parse the command line
    parser = argparse.ArgumentParser ()

    # add optional arguments
    parser.add_argument ("-a", "--addr", default="127.0.0.1", help="IP Address to connect to (default: localhost i.e., 127.0.0.1)")
    parser.add_argument ("-i", "--iters", type=int, default=10, help="Number of iterations (default: 10")
    parser.add_argument ("-p", "--ports", type=int, nargs=2, default=[5555, 4444], help="Ports that client is listening on (default: [5555, 4444])")
    args = parser.parse_args ()

    return args

#------------------------------------------
# main function
def main ():
    """ Main program """

    print("Demo Health Status Server")

    # first parse the command line args
    parsed_args = parseCmdLineArgs ()

    # create refrigerator object (on init, it makes context on sockets for both servers)
    refrigerator = Refrigerator()

    # connect refrigerator to both servers
    refrigerator.connect(refrigerator.grocery_socket, parsed_args.ports[0], parsed_args.addr)
    print("Refrigerator connected to grocery server.")
    refrigerator.connect(refrigerator.health_status_socket, parsed_args.ports[1], parsed_args.addr)
    print("Refrigerator connected to health status server.")

    # use this to keep track of time to send/receive messages
    roundtrip_times_zmpq = []

    # send some arbitrary number of messages
    for i in range(0, parsed_args.iters):

        # find random num, if it's 1, we send health message, else grocery message
        # means ~25% of messages will be health messages
        
        # send health message
        if random.randint(1, 4) == 1:
            
            # create message, set some arbitrary content
            healthcontents = HealthContents()
            
            msg = Message()
            msg.type = MessageType.HEALTH
            msg.contents = healthcontents
            msg.contents.sensor_status = Status.GOOD
            msg.contents.dispenser = Dispenser.PARTIAL
            msg.contents.lightbulb = Status.BAD
            msg.contents.fridge_temp = 35
            msg.contents.freezer_temp = 28
            msg.contents.icemaker = 9

            # time how long it takes
            start_time = time.time () * 1000 # multiply by 1000 to get ms
            print("Sending message to health status server.")
            refrigerator.send_message(refrigerator.health_status_socket, msg)
            msg = refrigerator.receive_message(refrigerator.health_status_socket)
            end_time = time.time () * 1000
            roundtrip_times_zmpq.append(end_time - start_time)
            
        # send grocery message
        else:

            # create message, set some arbitrary content
            ordercontents = OrderContents()

            # add veggies
            v = Veggies()
            v.broccoli = 0
            v.carrot = 4
            v.cucumber = 9
            v.potato = 2
            v.tomato = 1
            ordercontents.veggies = v

            # add Drinks
            d = Drinks()

            # add bottles
            b = Bottles()
            b.sprite = 2
            b.fanta = 4
            b.dietcoke = 2
            d.bottles = b

            # add cans
            c = Cans()
            c.coke = 2
            c.beer = 12
            c.pepsi = 0
            d.cans = c

            ordercontents.drinks = d


            # add meat
            meat1 = Meat()
            meat1.type = MeatType.CHICKEN
            meat1.quantity = 5
            meat2 = Meat()
            meat2.type = MeatType.BEEF
            meat2.quantity = 2
            meat3 = Meat()
            meat3.type = MeatType.TURKEY
            meat3.quantity = 1
            ordercontents.meat = [meat1, meat2, meat3]

            # add milk
            milk1 = Milk()
            milk1.type = MilkType.ALMOND
            milk1.quantity = 2
            milk2 = Milk()
            milk2.type = MilkType.OAT
            milk2.quantity = 1
            ordercontents.milk = [milk1, milk2]

            # add bread
            bread1 = Bread()
            bread1.type = BreadType.WHITE
            bread1.quantity = 1
            bread2 = Bread()
            bread2.type = BreadType.RYE
            bread2.quantity = 3
            ordercontents.bread = [bread1, bread2]

            msg = Message()
            msg.type = MessageType.ORDER
            msg.contents = ordercontents
            
            # time how long it takes
            start_time = time.time () * 1000 # multiply by 1000 to get ms
            print("Sending message to grocery server.")
            refrigerator.send_message(refrigerator.grocery_socket, msg)
            msg = refrigerator.receive_message(refrigerator.grocery_socket)
            end_time = time.time () * 1000
            roundtrip_times_zmpq.append(end_time - start_time)

    avg = sum(roundtrip_times_zmpq) / len(roundtrip_times_zmpq)
    print("Average roundtrip time to both servers with ZMQ: " + str(avg) + "ms")

#----------------------------------------------
if __name__ == '__main__':
    # here we just print the version numbers
    print("Current libzmq version is %s" % zmq.zmq_version())
    print("Current pyzmq version is %s" % zmq.pyzmq_version())

    main ()