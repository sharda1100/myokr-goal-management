from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from app.models import User, Organization, Department, Team

bp = Blueprint('admin', __name__)

def admin_required(f):
    """Decorator to require admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/organizations')
@login_required
@admin_required
def organizations():
    """Manage organizations"""
    orgs = Organization.query.all()
    return render_template('admin/organizations.html', organizations=orgs)

@bp.route('/departments')
@login_required
@admin_required
def departments():
    """Manage departments"""
    depts = Department.query.all()
    return render_template('admin/departments.html', departments=depts)

@bp.route('/teams')
@login_required
@admin_required
def teams():
    """Manage teams"""
    teams = Team.query.all()
    return render_template('admin/teams.html', teams=teams)

@bp.route('/users')
@login_required
@admin_required
def users():
    """User management page"""
    users = User.query.all()
    teams = Team.query.all()
    return render_template('admin/users.html', users=users, teams=teams)

@bp.route('/assign-user-to-team', methods=['POST'])
@login_required
@admin_required
def assign_user_to_team():
    """Assign a user to a team"""
    from flask import request
    from app import db
    
    user_id = request.form.get('user_id')
    team_id = request.form.get('team_id')
    
    user = User.query.get_or_404(user_id)
    team = Team.query.get_or_404(team_id)
    
    if team not in user.teams:
        user.teams.append(team)
        db.session.commit()
        flash(f'User {user.get_full_name()} assigned to team {team.name}', 'success')
    else:
        flash(f'User {user.get_full_name()} is already in team {team.name}', 'info')
    
    return redirect(url_for('admin.users'))

@bp.route('/remove-user-from-team', methods=['POST'])
@login_required
@admin_required
def remove_user_from_team():
    """Remove a user from a team"""
    from flask import request
    from app import db
    
    user_id = request.form.get('user_id')
    team_id = request.form.get('team_id')
    
    user = User.query.get_or_404(user_id)
    team = Team.query.get_or_404(team_id)
    
    if team in user.teams:
        user.teams.remove(team)
        db.session.commit()
        flash(f'User {user.get_full_name()} removed from team {team.name}', 'success')
    else:
        flash(f'User {user.get_full_name()} is not in team {team.name}', 'info')
    
    return redirect(url_for('admin.users'))