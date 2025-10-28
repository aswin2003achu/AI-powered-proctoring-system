from flask import Flask, render_template, jsonify
from routes.main_routes import main_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(main_bp)

@app.route('/health')
def health_check():
    return jsonify({"status": "running", "app": "AI Proctoring System"})

if __name__ == '__main__':
    app.run(debug=True)
