from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from app import db
from app.models import User
from app.forms.auth import LoginForm, RegistrationForm

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.index')
            flash('Login successful!', 'success')
            return redirect(next_page)
        flash('Invalid username or password', 'error')
    
    return render_template('auth/login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    return '''
    <div class="container mt-5">
        <h2>User Profile</h2>
        <p><strong>Name:</strong> {}</p>
        <p><strong>Username:</strong> {}</p>
        <p><strong>Email:</strong> {}</p>
        <p><strong>Role:</strong> {}</p>
        <a href="{}" class="btn btn-primary">Back to Dashboard</a>
    </div>
    '''.format(
        current_user.get_full_name(),
        current_user.username,
        current_user.email,
        current_user.role,
        url_for('dashboard.index')
    )

@bp.route('/settings')
@login_required
def settings():
    """User settings page"""
    return '''
    <div class="container mt-5">
        <h2>Settings</h2>
        <p>Settings page coming soon...</p>
        <a href="{}" class="btn btn-primary">Back to Dashboard</a>
    </div>
    '''.format(url_for('dashboard.index'))