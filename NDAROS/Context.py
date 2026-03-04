import serial
import vlc
import threading

from State import State, AlertState

class Context:
	arduino: serial.Serial
	state: State
	personPresent: bool
	mangroveNumber: int
	oceanButtonPressed: bool
	riverButtonPressed: bool
	powerplantButtonPressed: bool
	videoPlaying: bool

	def __init__(self, arduino: serial.Serial):
		self.arduino = arduino
		self.state = AlertState(self)
		self.personPresent = False
		self.mangroveNumber = 0
		self.oceanButtonPressed = False
		self.riverButtonPressed = False
		self.powerplantButtonPressed = False
		self.videoPlaying = False
		self.videoLock = threading.Lock()
		self.player = None
	
	def changeState(self, state: State):
		print(f"\033[91mChanging State to: {state.__class__.__name__}\033[0m")
		self.state = state

	def receive(self):
		if self.arduino.in_waiting > 0:
			line = self.arduino.readline().decode('utf-8').strip()
			print(f"Received: {line}")
		return line

	def send(self, message: str):
		self.arduino.write(f"{message}\n".encode('utf-8'))

	def displayVideo(self, videoPath: str):
		with self.videoLock:
			if self.videoPlaying:
				return
			self.videoPlaying = True
			thread = threading.Thread(target=self._playVideo, args=(videoPath,), daemon=True)
			thread.start()

	def _playVideo(self, videoPath: str):
		"""Runs in a separate thread."""
		self.player = vlc.MediaPlayer(videoPath)
		
		events = self.player.event_manager()
		events.event_attach(vlc.EventType.MediaPlayerEndReached, self._onVideoEnd)
		events.event_attach(vlc.EventType.MediaPlayerStopped, self._onVideoEnd)
		
		self.player.play()
		import time
		time.sleep(0.3)
		self.player.set_fullscreen(True)

	def _onVideoEnd(self, event):
		with self.videoLock:
			self.videoPlaying = False
			if self.player:
				self.player.release()
				self.player = None

	def stopVideo(self):
		with self.videoLock:
			if self.player:
				self.player.stop()
				self.player.release()
				self.player = None
			self.videoPlaying = False
			
	def execute(self):
		print(f"\033[91mCurrent State: {self.state.__class__.__name__}\033[0m")
		self.state.execute()
