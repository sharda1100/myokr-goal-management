from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Home page - redirect to dashboard if logged in, otherwise show landing page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    # Simple landing page for non-authenticated users
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>MyOKR - Goal Management System</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-8 text-center">
                    <h1 class="display-4 mb-4">🎯 Welcome to MyOKR</h1>
                    <p class="lead">Your goal management system is up and running!</p>
                    <div class="mt-4">
                        <a href="/auth/login" class="btn btn-primary btn-lg me-3">Login</a>
                        <a href="/auth/register" class="btn btn-outline-primary btn-lg">Register</a>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

@bp.route('/about')
def about():
    return "<h1>About MyOKR</h1><p>Coming soon...</p>"