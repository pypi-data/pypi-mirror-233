
'''
	import pathlib
	THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()

	from os.path import dirname, join, normpath
	SEARCH = normpath (join (THIS_FOLDER, "../.."))

	import BODY_SCAN
	BODY_SCAN.START (
		GLOB 		= SEARCH + '/**/*STATUS.py'
	)
'''

import glob

from .FUNCTIONS.START_A_SCAN 			import START_A_SCAN
from .START_MULTIPLE_PROCESSES 		import START_MULTIPLE_PROCESSES

from .AGGREGATE import START as AGGREGATE_START

def START (
	GLOB = "",
	RELATIVE_PATH = False,
	
	MODULE_PATHS = [],
	
	RECORDS = 0	
):
	FINDS = glob.glob (GLOB, recursive = True)
		
	if (RECORDS >= 1):
		print ()
		print ("SEARCHING FOR GLOB:")
		print ("	", GLOB)
		print ()
	
	if (RECORDS >= 1):
		print ()
		print ("	FINDS:", FINDS)
		print ("	FINDS COUNT:", len (FINDS))
		print ();
	
	PATH_STATUSES = []
	for PATH in FINDS:	
		[ STATUS ] = START_A_SCAN (		
			PATH = PATH,
			MODULE_PATHS = MODULE_PATHS,
			RELATIVE_PATH = RELATIVE_PATH,
			RECORDS = RECORDS
		)
		
		PATH_STATUSES.append (STATUS)

	STATUS = AGGREGATE_START (
		PATH_STATUSES
	)

	import json
	print (json.dumps (STATUS, indent = 4))
	
	
	
	return {
		"STATUS": STATUS
	}
	
