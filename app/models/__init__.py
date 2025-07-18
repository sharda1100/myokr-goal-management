from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

# User-Team association table
user_teams = db.Table('user_teams',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    role = db.Column(db.String(20), default='user')  # user, team_lead, admin, super_admin
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    
    # Relationships - Fixed the ambiguous foreign key issue
    teams = db.relationship('Team', secondary=user_teams, lazy='subquery',
                           backref=db.backref('members', lazy=True))
    
    # Separate relationships for assigned and created OKRs
    assigned_okrs = db.relationship('OKR', foreign_keys='OKR.assigned_to', 
                                   backref='assignee', lazy='dynamic')
    created_okrs = db.relationship('OKR', foreign_keys='OKR.created_by', 
                                  backref='creator', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def is_admin(self):
        return self.role in ['admin', 'super_admin']
    
    def is_team_lead(self):
        return self.role in ['team_lead', 'admin', 'super_admin']
    
    def __repr__(self):
        return f'<User {self.username}>'

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    users = db.relationship('User', backref='organization', lazy='dynamic')
    departments = db.relationship('Department', backref='organization', lazy='dynamic')
    
    def __repr__(self):
        return f'<Organization {self.name}>'

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Foreign keys
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
    
    # Relationships
    teams = db.relationship('Team', backref='department', lazy='dynamic')
    
    def __repr__(self):
        return f'<Department {self.name}>'

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Foreign keys
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    team_lead_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    team_lead = db.relationship('User', foreign_keys=[team_lead_id])
    okrs = db.relationship('OKR', backref='team', lazy='dynamic')
    
    def __repr__(self):
        return f'<Team {self.name}>'

class OKR(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='active')  # active, paused, completed, cancelled, archived
    progress = db.Column(db.Float, default=0.0)  # 0-100
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    priority = db.Column(db.String(20), default='medium')  # high, medium, low
    completion_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    
    # Foreign keys
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships are defined in User model to avoid circular references
    key_results = db.relationship('KeyResult', backref='okr', lazy='dynamic', 
                                 cascade='all, delete-orphan')
    
    def calculate_progress(self):
        """Calculate OKR progress based on key results"""
        key_results = self.key_results.all()
        if not key_results:
            return 0.0
        
        total_progress = sum(kr.progress for kr in key_results)
        self.progress = total_progress / len(key_results)
        return self.progress
    
    def get_status_color(self):
        colors = {
            'active': 'primary',
            'paused': 'warning', 
            'completed': 'success',
            'cancelled': 'danger',
            'archived': 'secondary'
        }
        return colors.get(self.status, 'secondary')
    
    def get_priority_color(self):
        colors = {
            'high': 'danger',
            'medium': 'warning',
            'low': 'info'
        }
        return colors.get(self.priority, 'secondary')
    
    def is_overdue(self):
        from datetime import date
        return self.end_date < date.today() and self.status == 'active'
    
    def days_remaining(self):
        from datetime import date
        if self.status == 'completed':
            return 0
        delta = self.end_date - date.today()
        return max(0, delta.days)
    
    def __repr__(self):
        return f'<OKR {self.title}>'

class KeyResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    target_value = db.Column(db.Float, nullable=False)
    current_value = db.Column(db.Float, default=0.0)
    unit = db.Column(db.String(20))  # %, count, revenue, etc.
    progress = db.Column(db.Float, default=0.0)  # 0-100
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = db.Column(db.Text)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    okr_id = db.Column(db.Integer, db.ForeignKey('okr.id'), nullable=False)
    
    def calculate_progress(self):
        """Calculate progress percentage based on current vs target value"""
        if self.target_value == 0:
            return 0.0
        
        self.progress = min((self.current_value / self.target_value) * 100, 100)
        return self.progress
    
    def get_progress_color(self):
        if self.progress >= 100:
            return 'success'
        elif self.progress >= 75:
            return 'info'
        elif self.progress >= 50:
            return 'warning'
        else:
            return 'danger'
    
    def get_status_text(self):
        if self.progress >= 100:
            return 'Completed'
        elif self.progress >= 75:
            return 'On Track'
        elif self.progress >= 50:
            return 'At Risk'
        else:
            return 'Off Track'
    
    def __repr__(self):
        return f'<KeyResult {self.title}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))