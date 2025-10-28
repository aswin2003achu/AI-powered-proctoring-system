from flask import Blueprint, render_template, jsonify
from utils.video_stream import start_camera
from models.drowsiness_model import detect_drowsiness

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def home():
    return render_template('index.html')

@main_bp.route('/detect')
def detect():
    frame = start_camera()
    status = detect_drowsiness(frame)
    return jsonify({"drowsiness_status": status})
