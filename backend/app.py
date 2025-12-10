from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Import and register blueprints
from routes.gifts import gifts_bp
from routes.capsules import capsules_bp
from routes.music import music_bp

app.register_blueprint(gifts_bp, url_prefix='/api/gifts')
app.register_blueprint(capsules_bp, url_prefix='/api/capsules')
app.register_blueprint(music_bp, url_prefix='/api/music')

@app.route('/')
def index():
    return {'message': 'GiftCapsule API is running'}, 200

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
