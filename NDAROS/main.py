import serial
import time
import sys
import vlc

from Context import Context
from State import State, AlertState, PresentationState, PipeState, ReadyProductionState, ProductionState, PopupMangroveState, ProductionMangroveState

PORT = '/dev/ttyACM0'
BAUD = 9600
TIMEOUT = 1

try:
	arduino = serial.Serial(port=PORT, baudrate=BAUD, timeout=TIMEOUT)
except Exception as e:
	print(f"Error opening serial port {PORT}: {e}", file=sys.stderr)
	sys.exit(1)


def main():
	try:
		context = Context(arduino)
		context.execute()

		'''player = vlc.MediaPlayer("video.webm")
		time.sleep(1)
		player.play()
		player.set_fullscreen(True)'''
		
		while True:
			arduino.write(f"LED\n".encode('utf-8'))

			if arduino.in_waiting > 0:
				line = arduino.readline().decode('utf-8').strip()
				print(f"Received: {line}")

		arduino.close()

	except KeyboardInterrupt:
		arduino.close()
		sys.exit(0)

if __name__ == "__main__":
    main()