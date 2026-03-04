from abc import ABC, abstractmethod

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
					self.context.changeState(PresentationState(self.context))
					self.context.execute()

class PresentationState(State):
	def __init__(self, context):
		self.context = context

	def execute(self):
		self.context.changeState(PipeState(self.context)) # 1 bouton préssé
		self.context.execute()

class PipeState(State):
	def __init__(self, context):
		self.context = context

	def execute(self):
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
		self.context.changeState(ProductionMangroveState(self.context)) # 1 mangrove placée
		self.context.execute()

class ProductionMangroveState(State):
	def __init__(self, context):
		self.context = context

	def execute(self):
		self.context.changeState(CleanState(self.context)) # 5 min de délai après que toutes les mangroves aient été placées
		self.context.execute()

class CleanState(State):
	def __init__(self, context):
		self.context = context

	def execute(self):
		pass