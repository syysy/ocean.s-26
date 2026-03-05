import serial
import threading
import time 
import requests

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
	
	def _convert_pdf_to_images(self, pdf_assets_dir, png_assets_dir):
		"""Convertir les PDFs en images PNG (première page uniquement)"""
		try:
			from pdf2image import convert_from_path
			import os
			
			# Créer le dossier pour les PNGs s'il n'existe pas
			if not os.path.exists(png_assets_dir):
				os.makedirs(png_assets_dir)
			
			# Chercher tous les PDFs dans le dossier assets
			if not os.path.exists(pdf_assets_dir):
				print(f"PDF assets directory not found: {pdf_assets_dir}")
				return
			
			pdf_files = [f for f in os.listdir(pdf_assets_dir) if f.endswith('.pdf')]
			
			if not pdf_files:
				print(f"No PDF files found in {pdf_assets_dir}")
				return
			
			for pdf_file in pdf_files:
				pdf_path = os.path.join(pdf_assets_dir, pdf_file)
				pdf_name = os.path.splitext(pdf_file)[0]
				img_name = f"{pdf_name}.png"
				img_path = os.path.join(png_assets_dir, img_name)
				
				# Vérifier si l'image existe déjà
				if os.path.exists(img_path):
					print(f"Image {img_name} already exists, skipping conversion")
					continue
				
				print(f"Converting {pdf_file} to image...")
				try:
					# Convertir juste la première page
					images = convert_from_path(pdf_path, dpi=150, first_page=1, last_page=1)
					
					if images:
						images[0].save(img_path, 'PNG')
						print(f"Saved {img_name}")
				except Exception as e:
					print(f"Error converting {pdf_file}: {e}")
		except ImportError:
			print("Warning: pdf2image not installed. Images from PDF won't be generated.")
			print("Install with: pip install pdf2image pillow")
		except Exception as e:
			print(f"Error in PDF conversion: {e}")
	
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
		pdf_assets_dir = os.path.join(web_dir, 'assets')  # Où les PDFs sont stockés
		png_assets_dir = os.path.join(static_dir, 'assets')  # Où les PNGs seront sauvegardés
		
		print(f"Flask config: web_dir={web_dir}")
		print(f"Template dir: {template_dir}")
		print(f"Static dir: {static_dir}")
		print(f"Slides path: {slides_path}")
		print(f"Slides file exists: {os.path.exists(slides_path)}")
		print(f"PDF assets dir: {pdf_assets_dir}")
		print(f"PNG assets dir: {png_assets_dir}")
		
		# Convertir les PDFs en images au démarrage
		self._convert_pdf_to_images(pdf_assets_dir, png_assets_dir)
		
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
		self.state.execute()
