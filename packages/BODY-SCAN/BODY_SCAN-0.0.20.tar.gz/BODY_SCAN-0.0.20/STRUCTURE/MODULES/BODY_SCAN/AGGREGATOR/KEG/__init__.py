
from BOTANIST.PORTS.FIND_AN_OPEN_PORT 	import FIND_AN_OPEN_PORT

def CORE_KEG ():
	from flask import Flask, request

	app = Flask (__name__)

	@app.route ("/", methods = [ 'PUT' ])
	def HOME_POST ():
		return;
		
	PORT = FIND_AN_OPEN_PORT ()
	app.run (
		port = PORT
	)
	
	#print ("APP RUNNING")
	
	return [ PORT ]