import os
import sys

# Add the parent directory to the path so we can import our app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wsgi import app

# Initialize the database on first run
def init_db():
    from app import db
    import sqlite3
    
    # Check if database exists, if not create it
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'instance', 'myokr.db')
    if not os.path.exists(db_path):
        # Create the database tables
        with app.app_context():
            db.create_all()
            
            # Import and run the database initialization
            try:
                from init_db import init_sample_data
                init_sample_data()
            except ImportError:
                pass

# Initialize database on first import
init_db()

# Export the app for Vercel
def handler(request):
    return app(request.environ, request.start_response)

# Also export app directly for Vercel
app = app
