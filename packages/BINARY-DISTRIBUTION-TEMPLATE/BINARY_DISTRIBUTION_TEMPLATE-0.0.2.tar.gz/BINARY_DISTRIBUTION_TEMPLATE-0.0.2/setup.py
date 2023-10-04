
#
#	https://setuptools.pypa.io/en/latest/userguide/quickstart.html
#
#	https://github.com/pypa/sampleproject/blob/db5806e0a3204034c51b1c00dde7d5eb3fa2532e/setup.py
#
from setuptools import setup, find_packages

setup (
    version = "0.0.2",

	name = "BINARY_DISTRIBUTION_TEMPLATE",
    install_requires = [],	
	
	package_dir = { 
		'BINARY_DISTRIBUTION_TEMPLATE': 'src',
	},
	
	license = "",
	long_description = "",
	long_description_content_type = "text/markdown"
)