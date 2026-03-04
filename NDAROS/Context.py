from State.py import State

class Context:
	state: State
	personPresent: bool
	mangroveNumber: int
	oceanButtonPressed: bool
	riverButtonPressed: bool
	powerplantButtonPressed: bool

	def __init__(self):
		pass
	
	def changeState(self, state: State):
		print(f"\033[91mChanging State to: {state.__class__.__name__}\033[0m")
		self.state = state
	
	def execute(self):
		self.state.execute()
