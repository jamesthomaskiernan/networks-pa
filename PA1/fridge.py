# built in packages
import sys # for system exception
import zmq # this package must be imported for ZMQ to work

# files
from message import Message # our custom message in native format
import serialize as sz # this is from the file serialize.py in the same directory

################
# Fridge Class #
################
class Fridge ():
    
    # initializer, starts fridge and connects to address/port
    def __init__(self):

        print("Fridge starting...")

        # class vars, updated below, listed here just for convenience
        self.context = None
        self.health_socket = None
        self.grocery_socket = None

		# establish context for fridge
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
            self.health_socket = self.context.socket (zmq.REQ)
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
            print ("Fridge connecting to {}".format (connect_string))
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