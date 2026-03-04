import serial
import time
import sys

PORT = '/dev/ttyACM1'
BAUD = 9600
TIMEOUT = 1

pinDO = 2
pinAO = "A0" 

try:
	arduino = serial.Serial(port=PORT, baudrate=BAUD, timeout=TIMEOUT)
	time.sleep(2)
except Exception as e:
	print(f"Error opening serial port {PORT}: {e}", file=sys.stderr)
	sys.exit(1)

def main():
	while True:
		arduino.write(f"LED\n".encode('utf-8'))
		time.sleep(10)
	
	arduino.close()

main()