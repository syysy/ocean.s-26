from flask import Flask, render_template, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Stock de l'état actuel
current_slide = {"slide": 0}

# Charger les slides depuis JSON
def load_slides():
	try:
		slides_path = os.path.join(os.path.dirname(__file__), 'static', 'slides.json')
		with open(slides_path, 'r', encoding='utf-8') as f:
			return json.load(f)
	except Exception as e:
		print(f"Error loading slides: {e}")
		return {"slides": []}

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/api/slides')
def get_slides():
	return jsonify(load_slides())

@app.route('/api/next-slide')
def next_slide():
	slides_data = load_slides()
	max_slide = len(slides_data.get('slides', [])) - 1
	if current_slide["slide"] < max_slide:
		current_slide["slide"] += 1
	return jsonify({"slide": current_slide["slide"]})

@app.route('/api/prev-slide')
def prev_slide():
	if current_slide["slide"] > 0:
		current_slide["slide"] -= 1
	return jsonify({"slide": current_slide["slide"]})

@app.route('/api/goto-slide/<int:slide_num>')
def goto_slide(slide_num):
	slides_data = load_slides()
	max_slide = len(slides_data.get('slides', [])) - 1
	if 0 <= slide_num <= max_slide:
		current_slide["slide"] = slide_num
	return jsonify({"slide": current_slide["slide"]})

@app.route('/api/current-slide')
def get_current_slide():
	return jsonify({"slide": current_slide["slide"]})

@app.route('/static/assets/<path:filename>')
def serve_assets(filename):
	assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
	return send_from_directory(assets_dir, filename)

if __name__ == '__main__':
	app.run(debug=False, host='localhost', port=5000, use_reloader=False)