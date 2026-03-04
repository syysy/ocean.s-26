import serial
import time
import sys
import atexit
import signal

from Context import Context
from State import State, AlertState, PresentationState, PipeState, ReadyProductionState, ProductionState, PopupMangroveState, ProductionMangroveState

# Détécter le système d'exploitation pour le port série
PORT = None
if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
	PORT = '/dev/ttyACM0'
elif sys.platform == 'win32':
	PORT = 'COM5'
BAUD = 9600
TIMEOUT = 1

arduino = None

def cleanup():
	global arduino
	if arduino and arduino.is_open:
		print("Closing serial port...")
		arduino.close()

def signal_handler(sig, frame):
	cleanup()
	sys.exit(0)

atexit.register(cleanup)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

try:
	arduino = serial.Serial(port=PORT, baudrate=BAUD, timeout=TIMEOUT)
	time.sleep(2)
except Exception as e:
	print(f"Error opening serial port {PORT}: {e}", file=sys.stderr)
	sys.exit(1)


def main():
	try:
		context = Context(arduino)
		context.execute()

		context.send("LED")

	except KeyboardInterrupt:
		pass
	finally:
		cleanup()

if __name__ == "__main__":
    main()