# built in packages
import sys # for system exception
import argparse # for argument parsing
from concurrent import futures # needed for thread pool

import grpc
import schema_pb2 as spb
import schema_pb2_grpc as spb_grpc

########################
# Health Server Class #
########################
class ServiceHandler (spb_grpc.DummyServiceServicer):
	def method (self, req, context):
		""" Handle request message """
		try:

			print(req)
		
			# create response and send it back
			resp = spb.Message()
			resp.type = spb.MessageType.RESPONSE
			rc = spb.ResponseContents()
			rc.contents = "You are healthy"
			rc.code = spb.Code.OK
			resp.response_contents.CopyFrom(rc)
			return resp   # note that this is what is supposed to be returned
		except:
			print ("Some exception occurred handling method {}".format (sys.exc_info()[0]))
			raise

########################
# Command line parsing #
########################
def parseCmdLineArgs ():
	# parse the command line
	parser = argparse.ArgumentParser ()

	# add optional arguments
	parser.add_argument ("-p", "--port", type=int, default=4444, help="Port to bind to (default: 4444)")
	
	args = parser.parse_args ()

	return args
    
#------------------------------------------
# main function
def main ():

	# first parse the command line args
	parsed_args = parseCmdLineArgs ()
	
  # start server
	print("Health Server starting...")
	
	try:
		# create a server handle
		server = grpc.server (futures.ThreadPoolExecutor (max_workers=10))

		# now create our message handler object
		handler = ServiceHandler ()

		# make the binding between the stub and the handler
		spb_grpc.add_DummyServiceServicer_to_server(handler, server)

		server.add_insecure_port("[::]:" + str (parsed_args.port))

		server.start()

		print("Health Server listening on {}".format (parsed_args.port))
		server.wait_for_termination()

	except:
		print ("Some exception occurred {}".format (sys.exc_info()[0]))
		return

main ()


