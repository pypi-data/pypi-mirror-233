






#
#	https://setuptools.pypa.io/en/latest/userguide/quickstart.html
#
#	https://github.com/pypa/sampleproject/blob/db5806e0a3204034c51b1c00dde7d5eb3fa2532e/setup.py
#
from setuptools import setup, find_packages

setup (
    name = 'EQUITY',
    version = '0.0.1',
    install_requires = [],	
	
	package_dir = { 
		'EQUITY': 'REGION'
	},
	
	license = "COPY SIDEWAYS & PARALLEL",
	long_description = 'EQUITY',
	long_description_content_type = "text/plain",
)

