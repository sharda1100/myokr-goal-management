from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Home page - redirect to dashboard if logged in, otherwise show landing page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    # Show the new landing page template
    return render_template('main/index.html')

@bp.route('/about')
def about():
    return render_template('main/about.html')