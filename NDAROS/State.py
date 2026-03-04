from abc import ABC, abstractmethod
import time
import time

class State(ABC):
	@abstractmethod
	def handle_input(self, message: str):
		"""Handle message from Arduino and return next state or None"""
		pass

class AlertState(State):
	def __init__(self, context):
		self.context = context
		self.context.displaySlide(0)  # Affichage slide accueil

	def handle_input(self, message: str):
		if message == "PRESENCE":
			self.context.displaySlide(1)  # Affichage danse video
			return PresentationState(self.context)
		return None

class PresentationState(State):
	def __init__(self, context):
		self.context = context
		self.context.displaySlide(2)  # Video présentation

	def handle_input(self, message: str):
		if message == "DEMARRAGE":
			self.context.displaySlide(3)  # Boutons sélection
			return PipeState(self.context)
		return None

class PipeState(State):
	def __init__(self, context):
		self.context = context
		self.context.displaySlide(3)  # Affiche les 3 options
		self.start_time = time.time()

	def handle_input(self, message: str):
		# Attendre que 2 boutons soient pressés
		if message == "OCEAN_RIVER":
			self.context.displaySlide(4)  # Transition production
			return ReadyProductionState(self.context)
		elif message == "OCEAN_POWER":
			self.context.displaySlide(4)
			return ReadyProductionState(self.context)
		elif message == "RIVER_POWER":
			self.context.displaySlide(4)
			return ReadyProductionState(self.context)
		return None

class ReadyProductionState(State):
	def __init__(self, context):
		self.context = context
		self.context.displaySlide(5)  # En attente du bouton central

	def handle_input(self, message: str):
		if message == "CENTER_BUTTON":
			self.context.displaySlide(6)  # Production lancée
			return ProductionState(self.context)
		return None

class ProductionState(State):
	def __init__(self, context):
		self.context = context
		self.context.displaySlide(6)  # Production
		self.start_time = time.time()

	def handle_input(self, message: str):
		# Attendre 1 minute avant popup mangrove
		if time.time() - self.start_time > 60:
			self.context.displaySlide(7)  # Popup mangrove
			return PopupMangroveState(self.context)
		return None

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

	def execute(self):
		while True:
			self.context.send("compteurAimants\n")
			if self.context.arduino.in_waiting > 0:
				line = self.context.receive()
				counter = int(line)
				self.context.mangroveNumber = counter
				if counter >= 3: # Supposons qu'il y a 3 mangroves à placer
					self.context.displaySlide(9)
					# Attendre 5 minutes après que toutes les mangroves soient placées
					time.sleep(300) # 5 minutes
					return CleanState(self.context)

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