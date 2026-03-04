from abc import ABC, abstractmethod
import time

class State(ABC):
	@abstractmethod
	def execute(self) -> None:
		pass

class AlertState(State):
	def __init__(self, context):
		self.context = context

	def execute(self):
		while True:
			if self.context.arduino.in_waiting > 0:
				line = self.context.receive()
				if line == "PRESENCE":	
					# Affichage img1
					self.context.displayVideo("danse.mp4")
					self.context.changeState(PresentationState(self.context))
					self.context.execute()

class PresentationState(State):
	def __init__(self, context):
		self.context = context

	def execute(self):
		while True:
			if self.context.arduino.in_waiting > 0:
				line = self.context.receive()
				if line == "DEMARRAGE":	
					# Affichage img2
					self.context.stopVideo()
					self.context.displayVideo("video.webm")
					self.context.changeState(PresentationState(self.context))
					self.context.execute()
     
class PipeState(State):
	def __init__(self, context):
		self.context = context

	def execute(self):
		self.context.stopVideo()
		self.context.changeState(ReadyProductionState(self.context)) # 2 boutons préssés
		self.context.execute()

class ReadyProductionState(State):
	def __init__(self, context):
		self.context = context

	def execute(self):
		self.context.changeState(ProductionState(self.context)) # bouton central préssé
		self.context.execute()

class ProductionState(State):
	def __init__(self, context):
		self.context = context

	def execute(self):
		self.context.changeState(PopupMangroveState(self.context)) # 1 min de délai
		self.context.execute()

class PopupMangroveState(State):
	def __init__(self, context):
		self.context = context

	def execute(self):
		self.context.send("compteurAimants\n")
		while True:
			if self.context.arduino.in_waiting > 0:
				line = self.context.receive()
				counter = int(line)
				if counter >= 1:
					self.context.changeState(ProductionMangroveState(self.context)) # 1 mangrove placée
					self.context.execute()
					break

class ProductionMangroveState(State):
	def __init__(self, context):
		self.context = context

	def execute(self):
		# Vérifier que toutes les mangroves sont placées
		while True:
			self.context.send("compteurAimants\n")
			if self.context.arduino.in_waiting > 0:
				line = self.context.receive()
				counter = int(line)
				self.context.mangroveNumber = counter
				if counter >= 3: # Supposons qu'il y a 3 mangroves à placer
					# Attendre 5 minutes après que toutes les mangroves soient placées
					time.sleep(300) # 5 minutes
					self.context.changeState(CleanState(self.context)) # 5 min de délai après que toutes les mangroves aient été placées
					self.context.execute()
					break

class CleanState(State):
	def __init__(self, context):
		self.context = context

	def execute(self):
		pass