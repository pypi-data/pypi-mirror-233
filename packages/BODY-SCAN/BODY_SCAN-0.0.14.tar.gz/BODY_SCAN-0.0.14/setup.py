
#
#	https://setuptools.pypa.io/en/latest/userguide/quickstart.html
#
#	https://github.com/pypa/sampleproject/blob/db5806e0a3204034c51b1c00dde7d5eb3fa2532e/setup.py
#
from setuptools import setup, find_packages

VERSION = "0.0.14"

NAME = 'BODY_SCAN'
INSTALL_REQUIRES = [ 'BOTANIST', 'click', 'flask' ]

def SCAN_DESCRIPTION ():
	DESCRIPTION = ''
	try:
		with open ('README.rst') as f:
			DESCRIPTION = f.read ()
		print (DESCRIPTION)
	except Exception as E:
		pass;
		
	return DESCRIPTION;

setup (
    name = NAME,
    version = VERSION,
    install_requires = INSTALL_REQUIRES,	
	package_dir = { NAME: 'src'},
	
	license = "LL",
	long_description = SCAN_DESCRIPTION (),
	long_description_content_type = "text/markdown"
)