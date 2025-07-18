from app import create_app, db
from app.models import User, Organization, Department, Team, OKR, KeyResult

app = create_app()

with app.app_context():
    print("Dropping existing tables...")
    db.drop_all()
    
    print("Creating new tables...")
    db.create_all()
    
    print("Database tables created successfully!")
    
    # Create a test admin user
    admin = User(
        username='admin',
        email='admin@myokr.com',
        first_name='Admin',
        last_name='User',
        role='super_admin'
    )
    admin.set_password('password123')
    
    # Create a test organization
    org = Organization(
        name='Test Company',
        description='A test organization for MyOKR'
    )
    
    db.session.add(org)
    db.session.add(admin)
    db.session.commit()
    
    # Assign admin to organization
    admin.organization_id = org.id
    db.session.commit()
    
    print("✅ Database initialized successfully!")
    print("✅ Test admin user created!")
    print("Username: admin")
    print("Password: password123")
    print("✅ Test organization created!")