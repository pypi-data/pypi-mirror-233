
#
#	https://setuptools.pypa.io/en/latest/userguide/quickstart.html
#
#	https://github.com/pypa/sampleproject/blob/db5806e0a3204034c51b1c00dde7d5eb3fa2532e/setup.py
#
from setuptools import setup, find_packages

VERSION = "0.0.2"
NAME = 'BRUNCH'
INSTALL_REQUIRES = []

def SCAN_DESCRIPTION ():
	DESCRIPTION = ''
	try:
		with open ('MODULE.HTML') as f:
			DESCRIPTION = f.read ()
		print (DESCRIPTION)
	except Exception as E:
		pass;
		
	return DESCRIPTION;


setup (
    version = VERSION,

	name = NAME,
    install_requires = INSTALL_REQUIRES,	
	
	package_dir = { 
		#'bin': 'src/START.py',
		NAME: 'STRUCTURE',
	},
	package_data = {
		NAME: [ 'DIRECTIONS' ]
		
		#NAME: [ 'bin/BRUNCH' ]
    },
	scripts = [ 'STRUCTURE/MOVES/BRUNCH' ],
	
	license = "",
	long_description = SCAN_DESCRIPTION (),
	
	#long_description_content_type = "text/x-rst; charset=UTF-8",
	#long_description_content_type = 'text/markdown'

	long_description_content_type = "text/plain",
)
