


def CHECK_STATUS_LOCATION ():
	import pathlib
	THIS_FOLDER = pathlib.Path (__file__).parent.resolve ()

	from os.path import dirname, join, normpath
	CHECK_STATUS = normpath (join (THIS_FOLDER, "../SCAN_PROC/__init__.py"))
	
	return CHECK_STATUS