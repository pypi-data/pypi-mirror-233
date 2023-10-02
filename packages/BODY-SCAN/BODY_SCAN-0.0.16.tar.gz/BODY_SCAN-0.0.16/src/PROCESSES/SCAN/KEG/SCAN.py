
def SCAN_FILE (PATH):
	with open (PATH, mode = 'r') as file:
		STRING = file.read ()
		return STRING


import io
import sys
import traceback
def GET_EXCEPTION_TRACEBACK (EXCEPTION : Exception) -> str:
	try:
		file = io.StringIO ()
		traceback.print_exception (EXCEPTION, file = file)
		
		#return traceback.format_stack()
		
		return file.getvalue ().rstrip ().split ("\n")
	except Exception:
		pass;
		
	return 'An exception occurred while calculating trace.'


import json
import time
from time import sleep, perf_counter as pc


def SCAN (FIND):
	PATH = {}
	
	FINDINGS = []
	STATS = {
		"PASSES": 0,
		"ALARMS": 0
	}

	PATH_E = ""

	try:
		
		CONTENTS = SCAN_FILE (FIND)
		CONTENTS += '''
		
try:
	______BODY_SCAN ["CHECKS"] = CHECKS;	
	______BODY_SCAN ["CHECKS FOUND"] = True;
except Exception as E:
	print (E)
	______BODY_SCAN ["CHECKS FOUND"] = False;
		'''
		
		______BODY_SCAN = {}
		exec (
			CONTENTS, 
			{ 
				'______BODY_SCAN': ______BODY_SCAN,
				'__file__': FIND
			}
		)
		

		if (______BODY_SCAN ["CHECKS FOUND"] == False):
			return {
				"EMPTY": True
			}
		
		CHECKS = ______BODY_SCAN ['CHECKS']		

		
		for CHECK in CHECKS:
			try:
				TIME_START = pc ()
				CHECKS [ CHECK ] ()
				TIME_END = pc ()
				TIME_ELAPSED = TIME_END - TIME_START

				FINDINGS.append ({
					"CHECK": CHECK,
					"PASSED": True,
					"ELAPSED": [ TIME_ELAPSED, "SECONDS" ]
				})
				
				STATS ["PASSES"] += 1
				
			except Exception as E:
				TRACE = GET_EXCEPTION_TRACEBACK (E)
				
				FINDINGS.append ({
					"CHECK": CHECK,
					"PASSED": False,
					"EXCEPTION": repr (E),
					"EXCEPTION TRACE": TRACE
				})
				
				STATS ["ALARMS"] += 1
		
		
		return {
			"STATS": STATS,			
			"CHECKS": FINDINGS
		}
		
	except Exception as E:		
		PATH_E = E;

	return {
		"ALARM": "AN EXCEPTION OCCURRED WHILE SCANNING PATH",
		"EXCEPTION": repr (PATH_E),
		"EXCEPTION TRACE": GET_EXCEPTION_TRACEBACK (PATH_E)
	}