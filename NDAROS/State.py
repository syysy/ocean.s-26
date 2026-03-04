from abc import ABC, abstractmethod
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
		if message == "MANGROVE_PLACED":
			self.context.displaySlide(8)  # Production mangrove
			return ProductionMangroveState(self.context)
		return None

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