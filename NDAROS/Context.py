import serial
import threading

from State import State, AlertState

class Context:
	arduino: serial.Serial
	state: State
	flask_process: object

	def __init__(self, arduino: serial.Serial):
		self.arduino = arduino
		self.state = AlertState(self)
		self.flask_running = False
		
		# Démarrer Flask en thread background
		self._start_flask()
	
	def _start_flask(self):
		"""Lancer le serveur Flask en thread background"""
		import sys
		import os
		
		# Ajouter le chemin web au PYTHONPATH
		web_dir = os.path.join(os.path.dirname(__file__), 'web')
		
		thread = threading.Thread(target=self._run_flask, daemon=True)
		thread.start()
		time.sleep(2)  # Attendre que Flask démarre
		self.flask_running = True
		print("Flask server started")
	
	def _run_flask(self):
		"""Exécute Flask (appelé dans un thread)"""
		import sys
		import os
		import json
		from flask import Flask, render_template, jsonify
		
		web_dir = os.path.join(os.path.dirname(__file__), 'web')
		template_dir = os.path.join(web_dir, 'templates')
		static_dir = os.path.join(web_dir, 'static')
		slides_path = os.path.join(static_dir, 'slides.json')
		
		print(f"Flask config: web_dir={web_dir}")
		print(f"Template dir: {template_dir}")
		print(f"Static dir: {static_dir}")
		print(f"Slides path: {slides_path}")
		print(f"Slides file exists: {os.path.exists(slides_path)}")
		
		app = Flask(__name__, 
		           template_folder=template_dir,
		           static_folder=static_dir)
		
		current_slide = [0]  # Utiliser liste pour modifier dans les fonctions imbriquées
		
		def load_slides():
			"""Charger les slides depuis le fichier JSON"""
			try:
				with open(slides_path, 'r', encoding='utf-8') as f:
					return json.load(f)
			except Exception as e:
				print(f"Error loading slides from {slides_path}: {e}")
				return {"slides": [{"type": "text", "content": f"Error: {e}"}]}
		
		@app.route('/')
		def index():
			return render_template('index.html')
		
		@app.route('/api/slides')
		def get_slides():
			slides = load_slides()
			return jsonify(slides)
		
		@app.route('/api/next-slide')
		def next_slide():
			slides = load_slides()
			max_slide = len(slides.get('slides', [])) - 1
			if current_slide[0] < max_slide:
				current_slide[0] += 1
			return jsonify({"slide": current_slide[0]})
		
		@app.route('/api/prev-slide')
		def prev_slide():
			if current_slide[0] > 0:
				current_slide[0] -= 1
			return jsonify({"slide": current_slide[0]})
		
		@app.route('/api/goto-slide/<int:slide_num>')
		def goto_slide(slide_num):
			slides = load_slides()
			max_slide = len(slides.get('slides', [])) - 1
			if 0 <= slide_num <= max_slide:
				current_slide[0] = slide_num
			return jsonify({"slide": current_slide[0]})
		
		@app.route('/api/current-slide')
		def get_current_slide():
			return jsonify({"slide": current_slide[0]})
		
		try:
			app.run(debug=False, host='localhost', port=5000, use_reloader=False)
		except Exception as e:
			print(f"Error running Flask: {e}")
	
	def changeState(self, state: State):
		print(f"\033[91mChanging State to: {state.__class__.__name__}\033[0m")
		self.state = state

	def receive(self):
		if self.arduino.in_waiting > 0:
			line = self.arduino.readline().decode('utf-8').strip()
			print(f"Received: {line}")
			return line
		return ""

	def send(self, message: str):
		self.arduino.write(f"{message}\n".encode('utf-8'))
	
	def displaySlide(self, slide_num: int):
		"""Afficher une slide via Flask/Reveal.js"""
		try:
			if self.flask_running:
				response = requests.get(f"http://localhost:5000/api/goto-slide/{slide_num}")
				print(f"Displaying slide {slide_num}")
		except Exception as e:
			print(f"Error displaying slide: {e}")
	
	def execute(self):
		print(f"\033[91mCurrent State: {self.state.__class__.__name__}\033[0m")
		print("Running main loop... listening for Arduino messages")
		
		# Boucle principale unique
		while True:
			try:
				# Lire message Arduino
				message = self.receive()
				
				if message:
					# Laisser l'état actuel traiter le message
					next_state = self.state.handle_input(message)
					
					# Si un nouvel état est retourné, le changer
					if next_state:
						self.changeState(next_state)
				
				# Court délai pour éviter consommation CPU
				time.sleep(0.1)
				
			except KeyboardInterrupt:
				print("Interrupted by user")
				break
			except Exception as e:
				print(f"Error in main loop: {e}")
				time.sleep(1)
