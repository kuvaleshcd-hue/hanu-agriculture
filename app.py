"""
Root entry point for Hanu Agri application.
Enables automatic discovery and execution by Render, Railway, and other PaaS providers
using standard root commands (gunicorn app:app).
"""
import os
import sys

# Ensure backend directory is in python search path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(CURRENT_DIR, 'backend')
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# Automatically ensure datasets and models are initialized if missing
try:
    from backend.setup_models import setup
    setup()
except Exception as e:
    print(f"Notice during setup_models: {e}")

# Import the Flask application instance from backend
from backend.app import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
