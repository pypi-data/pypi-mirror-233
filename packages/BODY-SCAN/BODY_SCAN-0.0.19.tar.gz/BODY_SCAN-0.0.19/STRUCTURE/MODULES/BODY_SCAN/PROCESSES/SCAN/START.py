



def ADD_PATHS_TO_SYSTEM (PATHS):
	import pathlib
	FIELD = pathlib.Path (__file__).parent.resolve ()

	from os.path import dirname, join, normpath
	import sys
	for PATH in PATHS:
		sys.path.insert (0, normpath (join (FIELD, PATH)))



def CLIQUE ():
	import click
	@click.group ("KEG")
	def GROUP ():
		pass

	'''
		./STATUS_CHECK KEG OPEN \
		--port 10000
	'''
	@GROUP.command ("OPEN")
	@click.option ('--port', required = True)	
	@click.option ('--details', required = True)
	def OPEN (port, details):
		import json
		
		#print ("DETAILS:", details)
		#print (json.loads (details))
	
		DETAILS = json.loads (details)
		MODULE_PATHS = DETAILS ["MODULE_PATHS"];
	
		ADD_PATHS_TO_SYSTEM (MODULE_PATHS)
	
		from KEG import TAP as TAP_KEG
		
		TAP_KEG (
			PORT = port
		)

		return;


	return GROUP
	
def START_CLICK ():
	import click
	@click.group ()
	def GROUP ():
		pass
		
	GROUP.add_command (CLIQUE ())
	GROUP ()

START_CLICK ()



#
