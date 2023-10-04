
#
#	https://setuptools.pypa.io/en/latest/userguide/quickstart.html
#
#	https://github.com/pypa/sampleproject/blob/db5806e0a3204034c51b1c00dde7d5eb3fa2532e/setup.py
#
from setuptools import setup, find_packages


def SCAN_VARIABLES ():
	import json

	VARIABLES = {}
	try:
		with open ('VARIABLES.JSON') as f:
			STRING = f.read ().strip()
			print (STRING)
		
			VARIABLES = json.loads (STRING)
	except Exception as E:
		print (E)
	
		pass;
		
	return VARIABLES;


def SCAN_DESCRIPTION ():
	DESCRIPTION = ''
	try:
		with open ('README.rst') as f:
			DESCRIPTION = f.read ()
		print (DESCRIPTION)
	except Exception as E:
		pass;
		
	return DESCRIPTION;

VARIABLES = SCAN_VARIABLES ()

setup (
    name = VARIABLES ['NAME'],
    version = VARIABLES ['VERSION'],
    install_requires = VARIABLES ['INSTALL_REQUIRES'],	
	
	package_dir = { 
		VARIABLES ['NAME']: 'STRUCTURE/MODULES/VEGAN'
	},
	
	license = "VEGAN",
	long_description = SCAN_DESCRIPTION (),
	long_description_content_type = "text/markdown"
)