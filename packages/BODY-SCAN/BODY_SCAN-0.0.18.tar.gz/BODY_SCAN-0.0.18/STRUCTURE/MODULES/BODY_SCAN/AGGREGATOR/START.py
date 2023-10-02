

from KEG import TAP as TAP_KEG
	

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
	def OPEN (port):
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
