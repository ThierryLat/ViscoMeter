import sys
import serial



ser = serial.Serial(port=sys.argv[1],baudrate=int(sys.argv[2]))

while True:  # The program never ends... will be killed when master is over.


	output = ser.readline() # read output

	sys.stdout.write(output) # write output to stdout
	sys.stdout.flush()
