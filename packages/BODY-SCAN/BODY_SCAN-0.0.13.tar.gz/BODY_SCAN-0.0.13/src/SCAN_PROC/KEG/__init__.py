

def ADD_PATHS_TO_SYSTEM (PATHS):
	import pathlib
	FIELD = pathlib.Path (__file__).parent.resolve ()

	from os.path import dirname, join, normpath
	import sys
	for PATH in PATHS:
		sys.path.insert (0, normpath (join (FIELD, PATH)))

from .SCAN import SCAN

import json

def TAP (
	PORT = 0,
	RECORDS = 0
):
	if (RECORDS >= 1):
		print ("OPENING KEG ON PORT:", PORT)

	from flask import Flask, request

	app = Flask (__name__)

	@app.route ("/", methods = [ 'GET' ])
	def HOME ():	
		return "?"

	@app.route ("/", methods = [ 'PUT' ])
	def HOME_POST ():
		if (RECORDS >= 1):
			print ("@ HOME PUT", request.data)
	
		DATA = json.loads (request.data.decode ('utf8'))
		
		if (RECORDS >= 1):
			print ("DATA:", DATA)

		FINDS = DATA ['FINDS']
		MODULE_PATHS = DATA ['MODULE PATHS']
		RELATIVE_PATH = DATA ['RELATIVE PATH']

		ADD_PATHS_TO_SYSTEM (MODULE_PATHS)

		STATUS = {
			"PATHS": [],
			"STATS": {
				"EMPTY": 0,
				"CHECKS": {
					"PASSES": 0,
					"ALARMS": 0
				}
			}
		}
		
		STATUS = {}

		for FIND in FINDS:
			SCAN_STATUS = SCAN (FIND)
			
			import os
			if (type (RELATIVE_PATH) == str):
				PATH = os.path.relpath (FIND, RELATIVE_PATH)
			else:
				PATH = FIND
			
			
			STATUS = {
				"PATH": PATH,
				** SCAN_STATUS
			};
			
			
		return json.dumps (STATUS, indent = 4)
		
	app.run (
		port = PORT
	)