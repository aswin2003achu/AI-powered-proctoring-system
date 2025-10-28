from flask import Flask, jsonify
from routes.admin_routes import admin_bp
from routes.teacher_routes import teacher_bp
from routes.student_routes import student_bp

app = Flask(__name__)
app.config.from_object("config")

# Register Blueprints
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(teacher_bp, url_prefix="/teacher")
app.register_blueprint(student_bp, url_prefix="/student")

@app.route('/')
def home():
    return jsonify({"message": "AI Powered Exam Proctoring System API is running"})

if __name__ == '__main__':
    app.run(debug=True)
