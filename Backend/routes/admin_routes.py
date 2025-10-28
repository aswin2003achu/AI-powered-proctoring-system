from flask import Blueprint, jsonify, request
from services.face_recognition_service import register_face

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/register', methods=['POST'])
def register_student():
    """Register a new student's face."""
    image = request.files.get('image')
    name = request.form.get('name')
    if not image or not name:
        return jsonify({"error": "Missing name or image"}), 400

    result = register_face(image, name)
    return jsonify(result)
