import serial
import time
import sys
import atexit
import signal

from Context import Context
from State import State, AlertState, PresentationState, PipeState, ReadyProductionState, ProductionState, PopupMangroveState, ProductionMangroveState

PORT = '/dev/ttyACM0'
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

def connect_arduino(port=PORT, baud=BAUD, timeout=TIMEOUT, retries=5):
    for attempt in range(retries):
        try:
            arduino = serial.Serial(port=port, baudrate=baud, timeout=timeout)
            time.sleep(2)  # Wait for Arduino to initialize
            return arduino
        except Exception as e:
            if attempt < retries - 1:
                print(f"Connection failed (attempt {attempt+1}/{retries}), retrying in 2s...", file=sys.stderr)
                time.sleep(2)
            else:
                print(f"Error opening serial port {port}: {e}", file=sys.stderr)
                sys.exit(1)

def main():
	try:
		arduino = connect_arduino()
		context = Context(arduino)
		context.execute()

		context.send("LED")

	except KeyboardInterrupt:
		pass
	finally:
		cleanup()

if __name__ == "__main__":
    main()