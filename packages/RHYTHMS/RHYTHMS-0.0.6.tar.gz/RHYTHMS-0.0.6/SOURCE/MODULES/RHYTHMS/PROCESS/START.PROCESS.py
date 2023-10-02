#!/usr/bin/python3


def ADD_SYSTEM_PATHS (PATHS):
	import pathlib
	from os.path import dirname, join, normpath
	import sys
	
	THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()	
	for PATH in PATHS:
		sys.path.insert (0, normpath (join (THIS_FOLDER, PATH)))

	return;


ADD_SYSTEM_PATHS ([ 
	'MODULES',
	'MODULES_PIP'
])

