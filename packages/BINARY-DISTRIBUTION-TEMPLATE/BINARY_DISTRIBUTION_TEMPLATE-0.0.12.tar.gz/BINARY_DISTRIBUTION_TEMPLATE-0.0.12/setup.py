
#
#	https://setuptools.pypa.io/en/latest/userguide/quickstart.html
#
#	https://github.com/pypa/sampleproject/blob/db5806e0a3204034c51b1c00dde7d5eb3fa2532e/setup.py
#
from setuptools import setup, find_packages, Extension

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
    version = "0.0.12",

	name = "BINARY_DISTRIBUTION_TEMPLATE",
    install_requires = [],	
	
	package_dir = { 
		#'bin': 'src/START.py',
		'BINARY_DISTRIBUTION_TEMPLATE': 'src',
	},
	package_data = {
		'BINARY_DISTRIBUTION_TEMPLATE': [ 'bin/BINARY_DISTRIBUTION_TEMPLATE' ]
    },
	scripts = [ 'src/bin/BINARY_DISTRIBUTION_TEMPLATE' ],
	
	license = "",
	long_description = SCAN_DESCRIPTION (),
	#long_description_content_type = "text/x-rst; charset=UTF-8",
	long_description_content_type = "text/plain",
	
)