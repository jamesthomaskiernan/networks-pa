# built in packages
import sys # for system exception
import zmq # this package must be imported for ZMQ to work
import time # for sleeping

# files
from message import Message # our custom message in native format
import serialize as sz # this is from the file serialize.py in the same directory

########################
# Grocery Server Class #
########################
class GroceryServer ():
	
	# initializer, starts server and begins listening
	def __init__(self, port = 5555, address = "*"):
		
		print("Grocery Server starting...")

		# class vars, updated below, listed here just for convenience
		self.context = None
		self.socket = None

		# establish context for server
		try:
			self.context = zmq.Context ()     # returns a singleton object
		except zmq.ZMQError as err:
			print ("ZeroMQ Error obtaining context: {}".format (err))
			return
		except:
			print ("Some exception occurred getting context {}".format (sys.exc_info()[0]))
			return

		# establish socket for server
		try:
			self.socket = self.context.socket (zmq.REP)
		except zmq.ZMQError as err:
			print ("ZeroMQ Error obtaining REP socket: {}".format (err))
			return
		except:
			print ("Some exception occurred getting REP socket {}".format (sys.exc_info()[0]))
			return

		# bind server
		try:
			bind_string = "tcp://" + address + ":" + str (port)
			print ("Grocery Server will be binding on {}".format (bind_string))
			self.socket.bind (bind_string)
		except zmq.ZMQError as err:
			print ("ZeroMQ Error binding REP socket: {}".format (err))
			self.socket.close ()
			return
		except:
			print ("Some exception occurred binding REP socket {}".format (sys.exc_info()[0]))
			self.socket.close ()
			return

		# listen for connections
		print ("Grocery Server now listening for messages.")
		
		while True:

			cm = Message()
		
			# receive message from client
			cm = self.receive_message()
			print("Grocery Server received following message:")
			cm.dump()

			# update message and send it back as a response
			cm.content = "THIS IS A RESPONSE FROM GROCERY"
			self.send_message(cm)

	# receives serialized message from clients
	def receive_message(self):
		try:
			# Note, in the following, if copy=False, then what is received is
			# a list of frames and not bytes
			cm = self.socket.recv_serialized (sz.deserialize_from_frames, copy=True)
			return cm
		except zmq.ZMQError as err:
			print ("ZeroMQ Error receiving serialized message: {}".format (err))
			raise
		except:
			print ("Some exception occurred with recv_serialized {}".format (sys.exc_info()[0]))
			raise

	# sends response as serialized message to client
	def send_message(self, msg):
		try:
			self.socket.send_serialized (msg, sz.serialize_to_frames)
		except zmq.ZMQError as err:
			print ("ZeroMQ Error serializing request: {}".format (err))
			raise
		except:
			print ("Some exception occurred with send_serialized {}".format (sys.exc_info()[0]))
			raise

server = GroceryServer(5555, "*")
