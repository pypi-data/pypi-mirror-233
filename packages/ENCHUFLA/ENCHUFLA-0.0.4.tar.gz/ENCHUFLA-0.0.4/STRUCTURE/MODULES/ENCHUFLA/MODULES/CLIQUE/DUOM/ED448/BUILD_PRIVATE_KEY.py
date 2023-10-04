


'''
PACT DUOM ED448 BUILD-PRIVATE-KEY \
--path "ED448_PRIVATE_KEY_2.DER" \
--seed "4986888B11358BF3D541B41EEA5DAECE1C6EFF64130A45FC8B9CA48F3E0E02463C99C5AEDC8A847686D669B7D547C18FE448FC5111CA88F4E8"
'''
def BUILD_PRIVATE_KEY (GROUP):

	import click
	@click.option ('--format', default = 'DER', help = 'DER, PEM')
	@click.option ('--path', default = '', help = '')
	@click.option ('--seed', required = True, help = 'Must be 57 bytes')
	@GROUP.command ("BUILD-PRIVATE-KEY")
	def BUILD_PRIVATE_KEY (format, path, seed):	
		print ("BUILD_PRIVATE_KEY")
		
		try:
			assert (len (seed) == 114)
		except Exception:
			#
			#	WORD LIST: https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki
			#
			#		EACH WORD IS:
			#			2 ** 11 = 2048 BITS
			#
			#			11 BOOLEAN UNITS
			#
		
			#
			#	SEED BOOLEAN UNITS:
			#		57 BYTES = (2 ** 8) * 57
			#
			#		8 * 57 = 456
			#
			
			#
			#	11 BOOLEAN UNIT WORDS NECESSARY:
			#
			#		456 / 11 -> 41.45 -> 42 WORDS
			#
		
			#
			#	1 BYTE = 2 ** 8 = 256 BITS
			#
			#	2 BYTES = 
			#
			print ("Seed must be 57 bytes")
			exit ()
		
		SEED 	= seed
		FORMAT 	= format;
		PATH 	= path;
		
		from DUOM.ED448.PRIVATE_KEY.BUILD import BUILD_PRIVATE_KEY
		[ PRIVATE_KEY, PRIVATE_KEY_EXPORT ] = BUILD_PRIVATE_KEY (
			SEED, 
			FORMAT,
			PATH = PATH
		)

		print ("PRIVATE KEY:", PRIVATE_KEY)
		print ("PRIVATE KEY EXPORT:", PRIVATE_KEY_EXPORT)
		print ("PRIVATE KEY PATH:", PATH)

		return;