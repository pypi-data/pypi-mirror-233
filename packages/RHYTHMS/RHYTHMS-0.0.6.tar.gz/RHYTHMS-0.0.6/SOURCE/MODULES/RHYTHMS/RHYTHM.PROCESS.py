#!/usr/bin/python3



from BOTANIST.PROCESSES.START_MULTIPLE import START_MULTIPLE
	
PROCS = START_MULTIPLE (
	PROCESSES = [
		{ 
			"STRING": 'python3 -m http.server 9000',
			"CWD": None
		}
	],
	WAIT = True
)

'''
EXIT 			= PROCS ["EXIT"]
PROCESSES 		= PROCS ["PROCESSES"]

time.sleep (.5)

EXIT ()
'''

