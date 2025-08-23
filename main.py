from flask import Flask, request, jsonify
from utils.process import process_video

app = Flask(__name__)

@app.route('/procesar_video', methods=['POST'])
def procesar_video():
    data = request.get_json()
    result = process_video(data)
    return jsonify(result)