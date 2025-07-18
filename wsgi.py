#!/usr/bin/env python3
import os
from app import create_app, db
from app.models import User, Organization, Department, Team, OKR, KeyResult
from flask_migrate import Migrate

# Use production config in production environment
app = create_app(os.getenv('FLASK_ENV') or 'production')
migrate = Migrate(app, db)

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
