import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables from .env if present
load_dotenv()

app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    # Auto-create tables if they don't exist
    with app.app_context():
        from app.extensions import db
        db.create_all()
        
    # In development, we can run with the built-in server.
    # In production, use Gunicorn with Gevent workers for SSE support.
    # e.g., gunicorn -k gevent -w 4 run:app
    app.run(host='0.0.0.0', port=5000, debug=(os.getenv('FLASK_ENV') == 'development'))
