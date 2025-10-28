from flask import Blueprint, jsonify
from services.monitoring_service import monitor_exam

teacher_bp = Blueprint('teacher_bp', __name__)

@teacher_bp.route('/monitor', methods=['GET'])
def monitor():
    """Monitor live exam feed for suspicious activity."""
    status = monitor_exam()
    return jsonify({"monitor_status": status})
