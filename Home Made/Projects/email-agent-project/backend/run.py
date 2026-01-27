# Entry point for Flask app

# backend/run.py
from flask import Flask
from flask_cors import CORS
from app.api.routes import api_bp

# 1. Initialize Flask App
app = Flask(__name__)

# 2. Enable CORS (Crucial for React!)
# This allows your React app (localhost:5173) to talk to Flask (localhost:5000)
CORS(app) 

# 3. Register Blueprints (Connect the routes)
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == "__main__":
    print("🚀 Server starting on http://localhost:5000")
    app.run(debug=True, port=5000)