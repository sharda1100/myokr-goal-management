#!/usr/bin/env python3
import os
from app import create_app, db
from app.models import User, Organization, Department, Team, OKR, KeyResult
from flask_migrate import Migrate

# Use production config in production environment
app = create_app(os.getenv('FLASK_ENV') or 'production')
migrate = Migrate(app, db)

# Initialize database on first run
def init_db():
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            
            # Check if we need to add sample data
            if User.query.count() == 0:
                # Import and run the database initialization
                from init_db import init_sample_data
                init_sample_data()
                print("Database initialized with sample data")
        except Exception as e:
            print(f"Database initialization error: {e}")
            # Try to create tables at least
            try:
                db.create_all()
            except Exception as e2:
                print(f"Failed to create tables: {e2}")

# Initialize database
init_db()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Organization': Organization,
        'Department': Department,
        'Team': Team,
        'OKR': OKR,
        'KeyResult': KeyResult
    }

if __name__ == '__main__':
    # For local development
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
