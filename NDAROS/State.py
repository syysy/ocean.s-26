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
		while time.time() - self.start_time < 10:
			time.sleep(0.1)
			
		self.context.displaySlide(7)  # Popup mangrove
		
		self.context.changeState(PopupMangroveState(self.context))
		self.context.execute()

class PopupMangroveState(State):
	def __init__(self, context):
		self.context = context
		self.context.displaySlide(7)  # Placement mangrove

	def execute(self):
		while True:
			self.context.send("MAGNET_COUNTER\n")
			line = self.context.receive()
			if line:
				try:
					counter = int(line)
					self.context.mangroveNumber = counter
					if counter > 0:
						self.context.displaySlide(8)  # Production mangrove
						self.context.changeState(ProductionMangroveState(self.context))
						self.context.execute()
						return
				except ValueError:
					pass
			time.sleep(0.1)

class ProductionMangroveState(State):
	def __init__(self, context):
		self.context = context
		self.last_magnet_count = 0
		self.max_reached_time = None
		self.context.displaySlide(8)  # Affichage production mangrove (1/5)

	def execute(self):
		while True:
			self.context.send("MAGNET_COUNTER\n")
			line = self.context.receive()
			
			if line:
				try:
					magnet_count = int(line)
				except ValueError:
					time.sleep(0.1)
					continue
				
				# Si le nombre de magnets diminue
				if magnet_count < self.last_magnet_count:
					# Si on était à 5 et qu'on avait un timer, reset
					if self.last_magnet_count == 5 and self.max_reached_time is not None:
						# Reset du processus - retour à PopupMangroveState
						self.context.changeState(PopupMangroveState(self.context))
						self.context.execute()
						return
					
					# Si le nombre diminue à 0, revenir à PopupMangroveState
					if magnet_count == 0:
						self.context.changeState(PopupMangroveState(self.context))
						self.context.execute()
						return
				
				# Mettre à jour le compteur
				self.last_magnet_count = magnet_count
				
				# Switch case pour afficher la slide appropriée
				self.display_slide_for_magnet_count(magnet_count)
				
				# Gestion du timer pour 5 magnets
				if magnet_count == 5:
					if self.max_reached_time is None:
						self.max_reached_time = time.time()
					
					# Si 20 secondes ont passé avec 5 magnets
					if time.time() - self.max_reached_time > 5:
						self.context.displaySlide(13)  # Slide de fin
						self.context.changeState(ProductionCompleteState(self.context))
						self.context.execute()
						return
				else:
					# Reset le timer si on n'est pas à 5
					self.max_reached_time = None
			
			time.sleep(0.1)
	
	def display_slide_for_magnet_count(self, count):
		"""Affiche la slide correspondante au nombre de magnets"""
		if count == 0:
			pass  # Rien à afficher
		elif count == 1:
			self.context.displaySlide(8)   # 1/5
			self.context.send("SEPARATION\n")
		elif count == 2:
			self.context.displaySlide(9)   # 2/5
			self.context.send("SEPARATION\n")
		elif count == 3:
			self.context.displaySlide(10)  # 3/5
			self.context.send("SEPARATION\n")
		elif count == 4:
			self.context.displaySlide(11)  # 4/5
			self.context.send("SEPARATION\n")
		elif count >= 5:
			self.context.displaySlide(12)  # 5/5
			self.context.send("SEPARATION\n")

class ProductionCompleteState(State):
	def __init__(self, context):
		self.context = context
		self.context.displaySlide(13)  # Slide de fin
		self.start_time = time.time()

	def execute(self):
		while time.time() - self.start_time < 5:
			self.context.displaySlide(14)  # Slide de fin
			self.context.changeState(CleanState(self.context))
			self.context.execute()

class CleanState(State):
	def __init__(self, context):
		self.context = context
		self.context.displaySlide(14)  # Remerciements
		self.start_time = time.time()

	def execute(self):
		# Attendre 5 secondes avant de revenir à l'accueil
		while time.time() - self.start_time < 5:
			time.sleep(0.1)
		
		# Après 5 secondes, retourner à AlertState
		self.context.changeState(AlertState(self.context))
		self.context.execute()