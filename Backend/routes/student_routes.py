from flask import Blueprint, jsonify
student_bp = Blueprint('student_bp', __name__)

@student_bp.route('/status')
def student_status():
    """Student endpoint to confirm camera availability."""
    return jsonify({"status": "Camera Active"})
