from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app.models import OKR
from datetime import date, timedelta

bp = Blueprint('dashboard', __name__)

@bp.route('/')
@login_required
def index():
    """Main dashboard"""
    # Get user's OKRs
    my_okrs = OKR.query.filter_by(assigned_to=current_user.id).all()
    
    # Calculate statistics
    total_okrs = len(my_okrs)
    completed_okrs = len([okr for okr in my_okrs if okr.status == 'completed'])
    active_okrs = len([okr for okr in my_okrs if okr.status == 'active'])
    
    # Get team OKRs count
    team_okrs_count = 0
    for team in current_user.teams:
        team_okrs_count += team.okrs.count()
    
    # Get recent OKRs (last 5)
    recent_okrs = OKR.query.filter_by(assigned_to=current_user.id)\
                          .order_by(OKR.created_at.desc())\
                          .limit(5).all()
    
    stats = {
        'total_okrs': total_okrs,
        'completed_okrs': completed_okrs,
        'active_okrs': active_okrs,
        'team_okrs_count': team_okrs_count
    }
    
    return render_template('dashboard/index.html', 
                         stats=stats, 
                         recent_okrs=recent_okrs,
                         current_date=date.today())

@bp.route('/analytics')
@login_required
def analytics():
    """Analytics dashboard with comprehensive OKR analytics"""
    # Get current date for calculations
    current_date = date.today()
    
    # === OVERALL STATISTICS ===
    total_okrs = OKR.query.count()
    completed_okrs = OKR.query.filter_by(status='completed').count()
    active_okrs = OKR.query.filter_by(status='active').count()
    paused_okrs = OKR.query.filter_by(status='paused').count()
    cancelled_okrs = OKR.query.filter_by(status='cancelled').count()
    archived_okrs = OKR.query.filter_by(status='archived').count()
    
    # Calculate completion rate
    completion_rate = (completed_okrs / total_okrs * 100) if total_okrs > 0 else 0
    
    # === PROGRESS ANALYTICS ===
    # Get all OKRs for progress analysis
    all_okrs = OKR.query.all()
    
    # Progress distribution
    progress_ranges = {
        '0-25%': 0,
        '26-50%': 0,
        '51-75%': 0,
        '76-99%': 0,
        '100%': 0
    }
    
    total_progress = 0
    for okr in all_okrs:
        total_progress += okr.progress
        if okr.progress == 100:
            progress_ranges['100%'] += 1
        elif okr.progress >= 76:
            progress_ranges['76-99%'] += 1
        elif okr.progress >= 51:
            progress_ranges['51-75%'] += 1
        elif okr.progress >= 26:
            progress_ranges['26-50%'] += 1
        else:
            progress_ranges['0-25%'] += 1
    
    average_progress = total_progress / len(all_okrs) if all_okrs else 0
    
    # === PRIORITY ANALYSIS ===
    high_priority = OKR.query.filter_by(priority='high').count()
    medium_priority = OKR.query.filter_by(priority='medium').count()
    low_priority = OKR.query.filter_by(priority='low').count()
    
    # === TEAM PERFORMANCE ===
    from app.models import Team
    teams = Team.query.all()
    team_stats = []
    
    for team in teams:
        team_okrs = team.okrs.all()
        if team_okrs:
            team_completed = sum(1 for okr in team_okrs if okr.status == 'completed')
            team_total = len(team_okrs)
            team_avg_progress = sum(okr.progress for okr in team_okrs) / team_total
            team_completion_rate = (team_completed / team_total * 100) if team_total > 0 else 0
            
            team_stats.append({
                'name': team.name,
                'total_okrs': team_total,
                'completed': team_completed,
                'completion_rate': team_completion_rate,
                'avg_progress': team_avg_progress,
                'active_okrs': sum(1 for okr in team_okrs if okr.status == 'active')
            })
    
    # Sort teams by completion rate
    team_stats.sort(key=lambda x: x['completion_rate'], reverse=True)
    
    # === TIMELINE ANALYSIS ===
    # OKRs created over time (last 6 months)
    six_months_ago = current_date - timedelta(days=180)
    
    timeline_data = []
    for i in range(6):
        month_start = six_months_ago + timedelta(days=i * 30)
        month_end = month_start + timedelta(days=30)
        
        month_okrs = OKR.query.filter(
            OKR.created_at >= month_start,
            OKR.created_at < month_end
        ).count()
        
        timeline_data.append({
            'month': month_start.strftime('%B %Y'),
            'count': month_okrs
        })
    
    # === OVERDUE ANALYSIS ===
    overdue_okrs = OKR.query.filter(
        OKR.end_date < current_date,
        OKR.status == 'active'
    ).count()
    
    # === STATUS DISTRIBUTION ===
    status_distribution = {
        'active': active_okrs,
        'completed': completed_okrs,
        'paused': paused_okrs,
        'cancelled': cancelled_okrs,
        'archived': archived_okrs
    }
    
    # === USER PERFORMANCE (if user is admin) ===
    user_stats = []
    if current_user.is_admin():
        from app.models import User
        users = User.query.filter_by(role='user').all()
        
        for user in users:
            user_okrs = OKR.query.filter_by(assigned_to=user.id).all()
            if user_okrs:
                user_completed = sum(1 for okr in user_okrs if okr.status == 'completed')
                user_total = len(user_okrs)
                user_avg_progress = sum(okr.progress for okr in user_okrs) / user_total
                user_completion_rate = (user_completed / user_total * 100) if user_total > 0 else 0
                
                user_stats.append({
                    'name': user.get_full_name(),
                    'total_okrs': user_total,
                    'completed': user_completed,
                    'completion_rate': user_completion_rate,
                    'avg_progress': user_avg_progress
                })
        
        user_stats.sort(key=lambda x: x['completion_rate'], reverse=True)
    
    # === RECENT ACTIVITY ===
    recent_completed = OKR.query.filter_by(status='completed').order_by(OKR.updated_at.desc()).limit(5).all()
    recent_created = OKR.query.order_by(OKR.created_at.desc()).limit(5).all()
    
    analytics_data = {
        'overview': {
            'total_okrs': total_okrs,
            'completed_okrs': completed_okrs,
            'active_okrs': active_okrs,
            'paused_okrs': paused_okrs,
            'cancelled_okrs': cancelled_okrs,
            'archived_okrs': archived_okrs,
            'completion_rate': round(completion_rate, 1),
            'average_progress': round(average_progress, 1),
            'overdue_okrs': overdue_okrs
        },
        'progress_distribution': progress_ranges,
        'priority_distribution': {
            'high': high_priority,
            'medium': medium_priority,
            'low': low_priority
        },
        'status_distribution': status_distribution,
        'team_performance': team_stats,
        'timeline': timeline_data,
        'user_performance': user_stats,
        'recent_activity': {
            'completed': recent_completed,
            'created': recent_created
        }
    }
    
    return render_template('dashboard/analytics.html', 
                         analytics=analytics_data, 
                         current_date=current_date)

@bp.route('/analytics/export')
@login_required
def export_analytics():
    """Export analytics data as JSON"""
    from flask import jsonify
    from sqlalchemy import func
    
    # Get the same analytics data as the main analytics route
    current_date = date.today()
    
    total_okrs = OKR.query.count()
    completed_okrs = OKR.query.filter_by(status='completed').count()
    active_okrs = OKR.query.filter_by(status='active').count()
    
    completion_rate = (completed_okrs / total_okrs * 100) if total_okrs > 0 else 0
    
    # Get team performance data
    from app.models import Team
    teams = Team.query.all()
    team_data = []
    
    for team in teams:
        team_okrs = team.okrs.all()
        if team_okrs:
            team_completed = sum(1 for okr in team_okrs if okr.status == 'completed')
            team_total = len(team_okrs)
            team_avg_progress = sum(okr.progress for okr in team_okrs) / team_total
            team_completion_rate = (team_completed / team_total * 100) if team_total > 0 else 0
            
            team_data.append({
                'team_name': team.name,
                'total_okrs': team_total,
                'completed_okrs': team_completed,
                'completion_rate': round(team_completion_rate, 2),
                'average_progress': round(team_avg_progress, 2)
            })
    
    export_data = {
        'export_date': current_date.isoformat(),
        'summary': {
            'total_okrs': total_okrs,
            'completed_okrs': completed_okrs,
            'active_okrs': active_okrs,
            'completion_rate': round(completion_rate, 2)
        },
        'team_performance': team_data
    }
    
    return jsonify(export_data)

@bp.route('/analytics/report')
@login_required
def analytics_report():
    """Generate a printable analytics report"""
    from sqlalchemy import func
    from datetime import datetime, timedelta
    
    # Get the same analytics data as the main analytics route
    current_date = date.today()
    
    # Get all analytics data (same as analytics route but simplified)
    total_okrs = OKR.query.count()
    completed_okrs = OKR.query.filter_by(status='completed').count()
    active_okrs = OKR.query.filter_by(status='active').count()
    
    completion_rate = (completed_okrs / total_okrs * 100) if total_okrs > 0 else 0
    
    # Get recent achievements
    recent_completed = OKR.query.filter_by(status='completed').order_by(OKR.updated_at.desc()).limit(10).all()
    
    # Get overdue OKRs
    overdue_okrs = OKR.query.filter(
        OKR.end_date < current_date,
        OKR.status == 'active'
    ).all()
    
    # Get top performing teams
    from app.models import Team
    teams = Team.query.all()
    team_stats = []
    
    for team in teams:
        team_okrs = team.okrs.all()
        if team_okrs:
            team_completed = sum(1 for okr in team_okrs if okr.status == 'completed')
            team_total = len(team_okrs)
            team_completion_rate = (team_completed / team_total * 100) if team_total > 0 else 0
            
            team_stats.append({
                'name': team.name,
                'total_okrs': team_total,
                'completed': team_completed,
                'completion_rate': team_completion_rate
            })
    
    team_stats.sort(key=lambda x: x['completion_rate'], reverse=True)
    
    report_data = {
        'generated_date': current_date,
        'summary': {
            'total_okrs': total_okrs,
            'completed_okrs': completed_okrs,
            'active_okrs': active_okrs,
            'completion_rate': round(completion_rate, 1)
        },
        'recent_achievements': recent_completed,
        'overdue_okrs': overdue_okrs,
        'top_teams': team_stats[:5],
        'report_period': f"{current_date.strftime('%B %Y')}"
    }
    
    return render_template('dashboard/analytics_report.html', report=report_data)