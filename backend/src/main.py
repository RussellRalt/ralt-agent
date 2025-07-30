import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.chat import chat_bp
from dotenv import load_dotenv
import os

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
load_dotenv()

app.config['SECRET_KEY'] = 'ralt-agent-secret-key-2025'

# Habilitar CORS para todas las rutas
CORS(app, origins=['http://localhost:5173', 'http://127.0.0.1:5173'])

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(chat_bp, url_prefix='/api')

# Configuración de base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/api/status', methods=['GET'])
def status():
    """Endpoint de estado del servidor"""
    return jsonify({
        'service': 'RALT Agent Backend',
        'version': '2.0.0',
        'status': 'running',
        'description': 'Agente multimodal profesional reinventado',
        'features': [
            'Agent Selection System',
            'Multimodal Capabilities',
            'Vision Processing',
            'Web Navigation',
            'Code Assistance',
            'Research Tools',
            'Creative Content'
        ],
        'endpoints': {
            'chat': '/api/chat',
            'agents': '/api/agents',
            'status': '/api/status'
        }
    }), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': '2025-07-30T22:00:00Z',
        'version': '2.0.0'
    }), 200

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return jsonify({
                'message': 'RALT Agent Backend is running',
                'frontend': 'Frontend not deployed yet',
                'api_docs': '/api/status'
            }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested endpoint does not exist',
        'available_endpoints': ['/api/status', '/api/health', '/api/chat', '/api/agents']
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV", "development") == "development"
    
    print(f"🚀 Starting RALT Agent Backend v2.0 on port {port}")
    print(f"🔧 Debug mode: {debug}")
    print(f"🌐 CORS enabled for frontend development")
    print(f"🤖 Agent types available: general, vision, web, code, research, creative")
    
    app.run(debug=debug, host="0.0.0.0", port=port)

