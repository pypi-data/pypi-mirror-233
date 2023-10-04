

def KEG (GROUP):
	import click
	@GROUP.group ("KEG")
	def GROUP ():
		pass
		
	import click
	@GROUP.command ("START")
	def EXAMPLE ():	
		print ("START")

		from KEG import START
		START ()

		return;

	return;