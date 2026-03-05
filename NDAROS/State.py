from abc import ABC, abstractmethod
import time
import time

class State(ABC):
	@abstractmethod
	def execute(self):
		pass

class AlertState(State):
	def __init__(self, context):
		self.context = context
		self.context.displaySlide(0)  # Affichage slide accueil
	
	def execute(self):
		self.context.send("RESET\n")
		while True:
			self.context.send("PRESENCE\n")
			msg = self.context.receive()
			if msg == "PRESENCE":
				break
			time.sleep(0.1)
		
		self.context.displaySlide(1)
		self.context.send("OCEAN_RIVER\n")
		self.context.changeState(PresentationState(self.context))
		self.context.execute()

class PresentationState(State):
	def __init__(self, context):
		self.context = context
		self.start_time = time.time()

	def execute(self):
		while time.time() - self.start_time < 10:
			time.sleep(0.1)
		
		self.context.displaySlide(2)

		self.context.changeState(PipeState(self.context))
		self.context.execute()

class PipeState(State):
	def __init__(self, context):
		self.context = context
		self.start_time = time.time()

	def execute(self):
		btn_river_pressed = False
		btn_ocean_pressed = False
		while not (btn_river_pressed and btn_ocean_pressed):
			if (btn_river_pressed and not btn_ocean_pressed) or (btn_ocean_pressed and not btn_river_pressed):
				self.context.displaySlide(3)  # Afficher la slide du milieu après le premier bouton
			self.context.send("PIPE_AVAILABLE\n")
			if self.context.receive() == "BUTTON_RIVER_PRESSED":
				btn_river_pressed = True
				self.context.send("PIPE_OCEAN\n")
			elif self.context.receive() == "BUTTON_OCEAN_PRESSED":
				btn_ocean_pressed = True
				self.context.send("PIPE_RIVER\n")
    
		self.context.displaySlide(4)  # Afficher la slide finale après les deux boutons
		time.sleep(5)  # Laisser le temps de lire la slide
		self.context.changeState(ReadyProductionState(self.context))
		self.context.execute()

class ReadyProductionState(State):
	def __init__(self, context):
		self.context = context
		self.context.displaySlide(5)  # En attente du bouton central

	def execute(self):
		self.context.send("BUTTON_CENTRAL\n")
		while self.context.receive() != "BUTTON_CENTRAL_PRESSED":
			time.sleep(0.1)

		self.context.displaySlide(6)  # Production lancée
		
		self.context.changeState(ProductionState(self.context))
		self.context.execute()

class ProductionState(State):
	def __init__(self, context):
		self.context = context
		self.context.displaySlide(6)  # Production
		self.start_time = time.time()

	def execute(self):
		while time.time() - self.start_time < 60:
			time.sleep(0.1)
			
		self.context.displaySlide(7)  # Popup mangrove
		
		self.context.changeState(PopupMangroveState(self.context))
		self.context.execute()

class PopupMangroveState(State):
	def __init__(self, context):
		self.context = context
		self.context.displaySlide(7)  # Placement mangrove

	def handle_input(self, message: str):
		while True:
			self.context.send("compteurAimants\n")
			if self.context.arduino.in_waiting > 0:
				line = self.context.receive()
				counter = int(line)
				self.context.mangroveNumber = counter
				if counter > 0:
					self.context.displaySlide(8)  # Production mangrove
					return ProductionMangroveState(self.context)

class ProductionMangroveState(State):
	def __init__(self, context):
		self.context = context
		self.context.displaySlide(8)  # Affichage production mangrove
		self.start_time = time.time()
		self.mangroves_placed = 1

	def handle_input(self, message: str):
		if message == "MANGROVE_PLACED":
			self.mangroves_placed += 1
		
		# Attendre 5 min après que toutes mangroves soient placées
		if self.mangroves_placed >= 3 and time.time() - self.start_time > 300:
			self.context.displaySlide(9)  # Fin
			return CleanState(self.context)
		return None

class CleanState(State):
	def __init__(self, context):
		self.context = context
		self.context.displaySlide(10)  # Remerciements
		self.start_time = time.time()

	def handle_input(self, message: str):
		# Après 5 secondes, revenir à l'accueil
		if time.time() - self.start_time > 5:
			return AlertState(self.context)
		return None