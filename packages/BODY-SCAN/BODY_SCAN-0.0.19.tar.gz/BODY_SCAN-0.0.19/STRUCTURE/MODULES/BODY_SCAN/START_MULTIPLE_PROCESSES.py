







"""
	from .START_MULTIPLE import START_MULTIPLE
	
	PROCS = START_MULTIPLE (
		PROCESSES = [
			{ 
				"STRING": 'python3 -m http.server 9000',
				"CWD": None
			},
			{
				"STRING": 'python3 -m http.server 9001',
				"CWD": None
			}
		]
	)
	
	EXIT 			= PROCS ["EXIT"]
	PROCESSES 		= PROCS ["PROCESSES"]

	time.sleep (.5)
	
	EXIT ()
"""


from 	subprocess import Popen
import 	shlex
import 	atexit
import 	sys

def START_MULTIPLE_PROCESSES (
	PROCESSES = [],
	WAIT = False
):
	PROCESSES_LIST = []

	for PROCESS in PROCESSES:
		if (type (PROCESS) == str):		
			PROCESSES_LIST.append (
				Popen (
					shlex.split (PROCESS)
				)
			)
			
		elif (type (PROCESS) == dict):
			PROCESS_STRING = PROCESS ["STRING"]
		
			CWD = None
			ENV = None
		
			if ("CWD" in PROCESS):
				CWD = PROCESS ["CWD"]
			
			if ("ENV" in PROCESS):
				ENV = PROCESS ["ENV"]
		
			PROCESSES_LIST.append (
				Popen (
					shlex.split (PROCESS_STRING),
					
					cwd = CWD,
					env = ENV,
					
					bufsize 			= - 1,
					executable 			= None, 
					
					stdin 				= None, 
					
					#stdout 			= None, 
					#stderr 			= None, 
					
					stdout 				= sys.stdout,
					stderr 				= sys.stderr,
					
					preexec_fn 			= None, 
					close_fds  			= True, 
					shell				= False, 
										
					universal_newlines	= None, 
					startupinfo			= None, 
					creationflags		= 0, 
					restore_signals		= True, 
					start_new_session	= False, 
					pass_fds			= (), 
					
					#*, 
					
					group				= None, 
					extra_groups		= None, 
					
					user				= None, 
					umask				= - 1, 
					encoding			= None,
					errors				= None, 
					text				= None, 
					pipesize			= - 1, 
					
					#process_group		= None
				)
			)

	
	def EXIT ():
		for PROCESS in PROCESSES_LIST:
			PROCESS.kill ()

	atexit.register (EXIT)
	
	if (WAIT):
		for PROCESS in PROCESSES_LIST:
			#
			#	https://docs.python.org/3/library/subprocess.html#subprocess.Popen.wait
			#
			PROCESS.wait ()	
		
	return {
		"PROCESSES": PROCESSES,
		"EXIT": EXIT
	}
	
	
	
	


