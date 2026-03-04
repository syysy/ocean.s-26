import serial
import time
import sys
import vlc

PORT = '/dev/ttyACM0'
BAUD = 9600
TIMEOUT = 1

try:
	arduino = serial.Serial(port=PORT, baudrate=BAUD, timeout=TIMEOUT)
	time.sleep(2)
except Exception as e:
	print(f"Error opening serial port {PORT}: {e}", file=sys.stderr)
	sys.exit(1)


def main():
	player = vlc.MediaPlayer("video.webm")
	time.sleep(1)
	player.play()
	player.set_fullscreen(True)
	
	while True:
		arduino.write(f"LED\n".encode('utf-8'))
		time.sleep(10)

		if arduino.in_waiting > 0:
			line = arduino.readline().decode('utf-8').strip()
			print(f"Received: {line}")
		
	arduino.close()

main()