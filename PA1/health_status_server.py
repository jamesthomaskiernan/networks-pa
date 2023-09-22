# built in packages
import sys # for system exception
import zmq # this package must be imported for ZMQ to work
import time # for sleeping
import argparse # for argument parsing

# files
import message as cm # our custom message in native format
import serialize as sz # this is from the file serialize.py in the same directory

#######################
# Health Server Class #
#######################
class HealthStatusServer ():
	
	# initializer, starts server and begins listening
	def __init__(self, port = 4444, intf = "*"):
		
		print("Health Server starting...")

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
			bind_string = "tcp://" + intf + ":" + str (port)
			print ("Health Server will be binding on {}".format (bind_string))
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
		print ("Health Server now listening for messages.")
		
		while True:

			# receive message from client
			msg = self.receive_message()
			print("Health Server received following message:")
			msg.dump()

			# update message and send it back as a response
			msg.contents.contents = "THIS IS A RESPONSE FROM HEALTH"
			self.send_message(msg)

	# receives serialized message from clients
	def receive_message(self):
		try:
			# Note, in the following, if copy=False, then what is received is
			# a list of frames and not bytes
			msg = self.socket.recv_serialized (sz.deserialize_from_frames, copy=True)
			return msg
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
    
########################
# Command line parsing #
########################
def parseCmdLineArgs ():
	# parse the command line
	parser = argparse.ArgumentParser ()

	# add optional arguments
	parser.add_argument ("-i", "--intf", default="*", help="Interface to bind to (default: *)")
	parser.add_argument ("-p", "--port", type=int, default=4444, help="Port to bind to (default: 4444)")
	args = parser.parse_args ()

	return args
    

#------------------------------------------
# main function
def main ():
	""" Main program """

	print("Demo Health Status Server")

	# first parse the command line args
	parsed_args = parseCmdLineArgs ()
		
	# start the server code
	server = HealthStatusServer(**vars(parsed_args))

#----------------------------------------------
if __name__ == '__main__':
	# here we just print the version numbers
	print("Current libzmq version is %s" % zmq.zmq_version())
	print("Current pyzmq version is %s" % zmq.pyzmq_version())

	main ()