#!/usr/bin/env python3
"""
Data seeding script for MyOKR application
Run this to populate the database with sample data
"""

import os
import sys
from datetime import date, datetime, timedelta
from werkzeug.security import generate_password_hash

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Organization, Department, Team, OKR, KeyResult

def create_sample_data():
    """Create sample data for testing"""
    
    # Create Flask app context
    app = create_app('default')
    
    with app.app_context():
        # Clear existing data (optional - comment out if you want to keep existing data)
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        print("Creating sample data...")
        
        # 1. Create Organization
        org = Organization(
            name="TechCorp Solutions",
            description="A leading technology company specializing in software development and digital transformation.",
            is_active=True
        )
        db.session.add(org)
        db.session.flush()
        
        # 2. Create Departments
        engineering_dept = Department(
            name="Engineering",
            description="Software development and technical infrastructure",
            organization_id=org.id
        )
        
        marketing_dept = Department(
            name="Marketing",
            description="Brand management and customer acquisition",
            organization_id=org.id
        )
        
        sales_dept = Department(
            name="Sales",
            description="Revenue generation and customer relations",
            organization_id=org.id
        )
        
        db.session.add_all([engineering_dept, marketing_dept, sales_dept])
        db.session.flush()
        
        # 3. Create Users
        # Admin user
        admin_user = User(
            username="admin",
            email="admin@techcorp.com",
            first_name="Admin",
            last_name="User",
            role="admin",
            organization_id=org.id
        )
        admin_user.set_password("admin123")
        
        # Engineering team lead
        eng_lead = User(
            username="john_doe",
            email="john.doe@techcorp.com",
            first_name="John",
            last_name="Doe",
            role="team_lead",
            organization_id=org.id
        )
        eng_lead.set_password("password123")
        
        # Engineering team members
        eng_dev1 = User(
            username="jane_smith",
            email="jane.smith@techcorp.com",
            first_name="Jane",
            last_name="Smith",
            role="user",
            organization_id=org.id
        )
        eng_dev1.set_password("password123")
        
        eng_dev2 = User(
            username="mike_johnson",
            email="mike.johnson@techcorp.com",
            first_name="Mike",
            last_name="Johnson",
            role="user",
            organization_id=org.id
        )
        eng_dev2.set_password("password123")
        
        # Marketing team lead
        marketing_lead = User(
            username="sarah_wilson",
            email="sarah.wilson@techcorp.com",
            first_name="Sarah",
            last_name="Wilson",
            role="team_lead",
            organization_id=org.id
        )
        marketing_lead.set_password("password123")
        
        # Marketing team member
        marketing_member = User(
            username="alex_brown",
            email="alex.brown@techcorp.com",
            first_name="Alex",
            last_name="Brown",
            role="user",
            organization_id=org.id
        )
        marketing_member.set_password("password123")
        
        # Sales team lead
        sales_lead = User(
            username="david_garcia",
            email="david.garcia@techcorp.com",
            first_name="David",
            last_name="Garcia",
            role="team_lead",
            organization_id=org.id
        )
        sales_lead.set_password("password123")
        
        db.session.add_all([admin_user, eng_lead, eng_dev1, eng_dev2, marketing_lead, marketing_member, sales_lead])
        db.session.flush()
        
        # 4. Create Teams
        # Engineering team
        engineering_team = Team(
            name="Backend Development",
            description="Core backend services and API development",
            department_id=engineering_dept.id,
            team_lead_id=eng_lead.id
        )
        
        frontend_team = Team(
            name="Frontend Development",
            description="User interface and user experience development",
            department_id=engineering_dept.id,
            team_lead_id=eng_lead.id
        )
        
        # Marketing team
        marketing_team = Team(
            name="Digital Marketing",
            description="Online marketing campaigns and social media",
            department_id=marketing_dept.id,
            team_lead_id=marketing_lead.id
        )
        
        # Sales team
        sales_team = Team(
            name="Enterprise Sales",
            description="B2B sales and enterprise client management",
            department_id=sales_dept.id,
            team_lead_id=sales_lead.id
        )
        
        db.session.add_all([engineering_team, frontend_team, marketing_team, sales_team])
        db.session.flush()
        
        # 5. Add users to teams
        engineering_team.members.extend([eng_lead, eng_dev1, eng_dev2])
        frontend_team.members.extend([eng_lead, eng_dev1])
        marketing_team.members.extend([marketing_lead, marketing_member])
        sales_team.members.extend([sales_lead])
        
        # 6. Create Sample OKRs
        # Engineering OKR 1
        eng_okr1 = OKR(
            title="Improve API Performance and Scalability",
            description="Optimize backend APIs to handle 10x more concurrent users while maintaining sub-200ms response times",
            start_date=date.today() - timedelta(days=30),
            end_date=date.today() + timedelta(days=60),
            status="active",
            priority="high",
            team_id=engineering_team.id,
            assigned_to=eng_dev1.id,
            created_by=eng_lead.id
        )
        
        # Engineering OKR 2
        eng_okr2 = OKR(
            title="Implement Modern Frontend Framework",
            description="Migrate legacy frontend to React with improved user experience and performance",
            start_date=date.today() - timedelta(days=15),
            end_date=date.today() + timedelta(days=75),
            status="active",
            priority="medium",
            team_id=frontend_team.id,
            assigned_to=eng_dev2.id,
            created_by=eng_lead.id
        )
        
        # Marketing OKR
        marketing_okr = OKR(
            title="Increase Brand Awareness and Lead Generation",
            description="Boost online presence and generate quality leads through digital marketing campaigns",
            start_date=date.today() - timedelta(days=20),
            end_date=date.today() + timedelta(days=70),
            status="active",
            priority="high",
            team_id=marketing_team.id,
            assigned_to=marketing_member.id,
            created_by=marketing_lead.id
        )
        
        # Sales OKR
        sales_okr = OKR(
            title="Expand Enterprise Client Base",
            description="Acquire new enterprise clients and increase revenue from existing accounts",
            start_date=date.today() - timedelta(days=10),
            end_date=date.today() + timedelta(days=80),
            status="active",
            priority="high",
            team_id=sales_team.id,
            assigned_to=sales_lead.id,
            created_by=sales_lead.id
        )
        
        # Completed OKR (for demonstration)
        completed_okr = OKR(
            title="Implement User Authentication System",
            description="Develop secure user authentication with multi-factor authentication support",
            start_date=date.today() - timedelta(days=90),
            end_date=date.today() - timedelta(days=10),
            status="completed",
            priority="high",
            progress=100.0,
            completion_date=date.today() - timedelta(days=5),
            team_id=engineering_team.id,
            assigned_to=eng_dev1.id,
            created_by=eng_lead.id
        )
        
        db.session.add_all([eng_okr1, eng_okr2, marketing_okr, sales_okr, completed_okr])
        db.session.flush()
        
        # 7. Create Key Results
        # Key Results for Engineering OKR 1
        kr1_1 = KeyResult(
            title="Reduce API Response Time",
            description="Optimize database queries and implement caching",
            target_value=200,
            current_value=350,
            unit="ms",
            okr_id=eng_okr1.id
        )
        kr1_1.calculate_progress()
        
        kr1_2 = KeyResult(
            title="Increase Concurrent User Capacity",
            description="Scale infrastructure to handle more users",
            target_value=10000,
            current_value=3500,
            unit="users",
            okr_id=eng_okr1.id
        )
        kr1_2.calculate_progress()
        
        kr1_3 = KeyResult(
            title="Implement API Rate Limiting",
            description="Add rate limiting to prevent abuse",
            target_value=100,
            current_value=60,
            unit="%",
            okr_id=eng_okr1.id
        )
        kr1_3.calculate_progress()
        
        # Key Results for Engineering OKR 2
        kr2_1 = KeyResult(
            title="Component Migration Progress",
            description="Migrate existing components to React",
            target_value=100,
            current_value=45,
            unit="%",
            okr_id=eng_okr2.id
        )
        kr2_1.calculate_progress()
        
        kr2_2 = KeyResult(
            title="Improve Page Load Speed",
            description="Optimize bundle size and loading times",
            target_value=3,
            current_value=5.2,
            unit="seconds",
            okr_id=eng_okr2.id
        )
        kr2_2.calculate_progress()
        
        # Key Results for Marketing OKR
        kr3_1 = KeyResult(
            title="Increase Website Traffic",
            description="Drive more organic and paid traffic",
            target_value=50000,
            current_value=32000,
            unit="visitors",
            okr_id=marketing_okr.id
        )
        kr3_1.calculate_progress()
        
        kr3_2 = KeyResult(
            title="Generate Qualified Leads",
            description="Convert visitors to quality leads",
            target_value=500,
            current_value=280,
            unit="leads",
            okr_id=marketing_okr.id
        )
        kr3_2.calculate_progress()
        
        kr3_3 = KeyResult(
            title="Improve Social Media Engagement",
            description="Increase followers and engagement rates",
            target_value=25,
            current_value=18,
            unit="% engagement",
            okr_id=marketing_okr.id
        )
        kr3_3.calculate_progress()
        
        # Key Results for Sales OKR
        kr4_1 = KeyResult(
            title="New Enterprise Clients",
            description="Acquire new enterprise-level clients",
            target_value=12,
            current_value=4,
            unit="clients",
            okr_id=sales_okr.id
        )
        kr4_1.calculate_progress()
        
        kr4_2 = KeyResult(
            title="Increase Revenue",
            description="Generate revenue from new and existing clients",
            target_value=2000000,
            current_value=750000,
            unit="$",
            okr_id=sales_okr.id
        )
        kr4_2.calculate_progress()
        
        # Key Results for Completed OKR
        kr5_1 = KeyResult(
            title="User Registration System",
            description="Implement secure user registration",
            target_value=100,
            current_value=100,
            unit="%",
            okr_id=completed_okr.id
        )
        kr5_1.calculate_progress()
        
        kr5_2 = KeyResult(
            title="Multi-Factor Authentication",
            description="Add 2FA support for enhanced security",
            target_value=100,
            current_value=100,
            unit="%",
            okr_id=completed_okr.id
        )
        kr5_2.calculate_progress()
        
        db.session.add_all([
            kr1_1, kr1_2, kr1_3,
            kr2_1, kr2_2,
            kr3_1, kr3_2, kr3_3,
            kr4_1, kr4_2,
            kr5_1, kr5_2
        ])
        
        # 8. Calculate OKR progress based on key results
        eng_okr1.calculate_progress()
        eng_okr2.calculate_progress()
        marketing_okr.calculate_progress()
        sales_okr.calculate_progress()
        
        # Commit all changes
        db.session.commit()
        
        print("✅ Sample data created successfully!")
        print("\n🔐 Login Credentials:")
        print("Admin User:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nTeam Lead (Engineering):")
        print("  Username: john_doe")
        print("  Password: password123")
        print("\nTeam Member (Engineering):")
        print("  Username: jane_smith")
        print("  Password: password123")
        print("\nMarketing Lead:")
        print("  Username: sarah_wilson")
        print("  Password: password123")
        print("\nSales Lead:")
        print("  Username: david_garcia")
        print("  Password: password123")
        print("\n🎯 Sample OKRs have been created for all teams!")
        print("\n🚀 You can now run the application with: python run.py")

if __name__ == "__main__":
    create_sample_data()
