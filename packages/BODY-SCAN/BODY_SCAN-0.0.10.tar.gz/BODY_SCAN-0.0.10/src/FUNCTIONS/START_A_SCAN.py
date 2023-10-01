
from BOTANIST.PORTS.FIND_AN_OPEN_PORT 	import FIND_AN_OPEN_PORT
from BOTANIST.PROCESSES.START_MULTIPLE import START_MULTIPLE as START_MULTIPLE_PROCESSES
from .CHECK_STATUS_LOCATION 	import CHECK_STATUS_LOCATION


def ATTEMPT_TAP_KEG ():
	PORT = FIND_AN_OPEN_PORT ()

	PROCS = START_MULTIPLE_PROCESSES (
		PROCESSES = [{
			"STRING": f'python3 { CHECK_STATUS_LOCATION () }  KEG OPEN --port { PORT }',
			"CWD": None
		}]
	)

	return [ PORT, PROCS ]

def START_A_SCAN (
	PATH,
	MODULE_PATHS = [],
	RELATIVE_PATH = False,
	RECORDS = 0
):
	[ PORT, PROCS ] = ATTEMPT_TAP_KEG ()
	
	import time
	time.sleep (0.5)
	
	REQUEST_ADDRESS = f'http://127.0.0.1:{ PORT }'
	
	import json
	import requests
	r = requests.put (
		REQUEST_ADDRESS, 
		data = json.dumps ({ 
			"FINDS": [ PATH ],
			"MODULE PATHS": MODULE_PATHS,
			"RELATIVE PATH": RELATIVE_PATH
		})
	)
	
	def FORMAT_RESPONSE (TEXT):
		import json
		return json.loads (TEXT)
	
	STATUS = FORMAT_RESPONSE (r.text)

	if (RECORDS >= 1):
		print ()
		print ("REQUEST ADDRESS :", REQUEST_ADDRESS)
		print ("REQUEST STATUS  :", r.status_code)
		print ("REQUEST TEXT  :", json.dumps (STATUS, indent = 4))
		print ()


	EXIT 			= PROCS ["EXIT"]
	PROCESSES 		= PROCS ["PROCESSES"]
	
	return [ STATUS ]