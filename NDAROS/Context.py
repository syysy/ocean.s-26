import serial

from State import State, AlertState

class Context:
	arduino: serial.Serial
	state: State
	personPresent: bool
	mangroveNumber: int
	oceanButtonPressed: bool
	riverButtonPressed: bool
	powerplantButtonPressed: bool

	def __init__(self, arduino: serial.Serial):
		self.arduino = arduino
		self.state = AlertState(self)
		self.personPresent = False
		self.mangroveNumber = 0
		self.oceanButtonPressed = False
		self.riverButtonPressed = False
		self.powerplantButtonPressed = False
	
	def changeState(self, state: State):
		print(f"\033[91mChanging State to: {state.__class__.__name__}\033[0m")
		self.state = state
	
	def execute(self):
		print(f"\033[91mCurrent State: {self.state.__class__.__name__}\033[0m")
		self.state.execute()
