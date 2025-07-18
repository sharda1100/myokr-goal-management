import os
from app import create_app, db
from app.models import User, Organization, Department, Team, OKR, KeyResult
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_ENV') or 'default')
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

@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized.')

@app.cli.command()
def create_test_user():
    """Create a test admin user."""
    from app.models import User
    from app import db
    
    # Check if user already exists
    existing_user = User.query.filter_by(username='admin').first()
    if existing_user:
        print("Admin user already exists!")
        return
    
    user = User(
        username='admin',
        email='admin@myokr.com',
        first_name='Admin',
        last_name='User',
        role='super_admin'
    )
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    print("Test admin user created successfully!")
    print("Username: admin")
    print("Password: password123")

@app.cli.command()
def setup_demo_data():
    """Create demo organization structure and data."""
    from app.models import User, Organization, Department, Team
    from app import db
    
    # Create organization
    org = Organization.query.first()
    if not org:
        org = Organization(name='Demo Company', description='Demo organization for MyOKR')
        db.session.add(org)
        db.session.commit()
        print("✅ Organization created")
    
    # Create departments
    departments = [
        {'name': 'Engineering', 'description': 'Product development and engineering'},
        {'name': 'Marketing', 'description': 'Marketing and growth'},
        {'name': 'Sales', 'description': 'Sales and business development'},
    ]
    
    for dept_data in departments:
        dept = Department.query.filter_by(name=dept_data['name']).first()
        if not dept:
            dept = Department(
                name=dept_data['name'],
                description=dept_data['description'],
                organization_id=org.id
            )
            db.session.add(dept)
            print(f"✅ Department '{dept_data['name']}' created")
    
    db.session.commit()
    
    # Create teams
    teams = [
        {'name': 'Frontend Team', 'description': 'Frontend development team', 'department': 'Engineering'},
        {'name': 'Backend Team', 'description': 'Backend development team', 'department': 'Engineering'},
        {'name': 'Growth Team', 'description': 'Growth and marketing team', 'department': 'Marketing'},
        {'name': 'Sales Team', 'description': 'Sales team', 'department': 'Sales'},
    ]
    
    for team_data in teams:
        team = Team.query.filter_by(name=team_data['name']).first()
        if not team:
            dept = Department.query.filter_by(name=team_data['department']).first()
            if dept:
                team = Team(
                    name=team_data['name'],
                    description=team_data['description'],
                    department_id=dept.id
                )
                db.session.add(team)
                print(f"✅ Team '{team_data['name']}' created")
    
    db.session.commit()
    print("🎉 Demo data setup complete!")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)