from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import OKR, KeyResult, Team, User
from app.forms.okr import OKRForm, UpdateProgressForm
from datetime import date

bp = Blueprint('okr', __name__)

@bp.route('/my-okrs')
@login_required
def my_okrs():
    """User's personal OKRs"""
    okrs = OKR.query.filter_by(assigned_to=current_user.id).all()
    return render_template('okr/my_okrs.html', okrs=okrs, current_date=date.today())

@bp.route('/team-okrs')
@login_required
def team_okrs():
    """Team OKRs for user's teams"""
    team_okrs = []
    for team in current_user.teams:
        team_okrs.extend(team.okrs.all())
    return render_template('okr/team_okrs.html', okrs=team_okrs, current_date=date.today())

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create new OKR"""
    form = OKRForm()
    
    # Populate choices for form fields
    form.team_id.choices = [(0, 'Select Team')] + [(team.id, team.name) for team in Team.query.all()]
    form.assigned_to.choices = [(0, 'Select User')] + [(user.id, user.get_full_name()) for user in User.query.all()]
    
    if form.validate_on_submit():
        # Create the OKR
        okr = OKR(
            title=form.title.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            team_id=form.team_id.data,
            assigned_to=form.assigned_to.data,
            created_by=current_user.id
        )
        db.session.add(okr)
        db.session.flush()  # Get the OKR ID
        
        # Create Key Results
        key_results = []
          # Key Result 1 (required)
        if form.key_result_1_title.data and form.key_result_1_target.data is not None:
            kr1 = KeyResult(
                title=form.key_result_1_title.data,
                description=form.key_result_1_description.data,
                target_value=form.key_result_1_target.data,
                unit=form.key_result_1_unit.data or 'count',
                okr_id=okr.id
            )
            key_results.append(kr1)

        # Key Result 2 (required)
        if form.key_result_2_title.data and form.key_result_2_target.data is not None:
            kr2 = KeyResult(
                title=form.key_result_2_title.data,
                description=form.key_result_2_description.data,
                target_value=form.key_result_2_target.data,
                unit=form.key_result_2_unit.data or 'count',
                okr_id=okr.id
            )
            key_results.append(kr2)
        
        # Key Result 3 (optional)
        if form.key_result_3_title.data and form.key_result_3_target.data is not None:
            kr3 = KeyResult(
                title=form.key_result_3_title.data,
                description=form.key_result_3_description.data,
                target_value=form.key_result_3_target.data,
                unit=form.key_result_3_unit.data or 'count',
                okr_id=okr.id
            )
            key_results.append(kr3)
        
        # Add all key results
        for kr in key_results:
            db.session.add(kr)
        
        # Ensure at least one key result is provided
        if not key_results:
            flash('At least one key result is required!', 'error')
            return render_template('okr/create.html', form=form)
        
        db.session.commit()
        flash('OKR created successfully!', 'success')
        return redirect(url_for('okr.view', id=okr.id))
    
    return render_template('okr/create.html', form=form)

@bp.route('/view/<int:id>')
@login_required
def view(id):
    """View specific OKR"""
    okr = OKR.query.get_or_404(id)
    
    # Check if user has permission to view this OKR
    if not (okr.assigned_to == current_user.id or 
            okr.created_by == current_user.id or 
            current_user.is_admin() or 
            current_user in okr.team.members):
        flash('You do not have permission to view this OKR.', 'error')
        return redirect(url_for('dashboard.index'))
    
    key_results = okr.key_results.all()
    return render_template('okr/view.html', okr=okr, key_results=key_results)

@bp.route('/update-progress/<int:kr_id>', methods=['GET', 'POST'])
@login_required
def update_progress(kr_id):
    """Update progress for a specific key result"""
    kr = KeyResult.query.get_or_404(kr_id)
    okr = kr.okr
    
    # Check permissions
    if not (okr.assigned_to == current_user.id or current_user.is_admin()):
        flash('You do not have permission to update this OKR.', 'error')
        return redirect(url_for('okr.view', id=okr.id))
    
    form = UpdateProgressForm()
    
    if form.validate_on_submit():
        kr.current_value = form.current_value.data
        kr.calculate_progress()
        
        # Recalculate OKR overall progress
        okr.calculate_progress()
        
        db.session.commit()
        flash('Progress updated successfully!', 'success')
        return redirect(url_for('okr.view', id=okr.id))
    
    # Pre-populate form with current values
    form.current_value.data = kr.current_value
    
    return render_template('okr/update_progress.html', form=form, key_result=kr, okr=okr)

@bp.route('/all')
@login_required
def all_okrs():
    """View all OKRs (for admins)"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard.index'))
    
    okrs = OKR.query.all()
    return render_template('okr/all_okrs.html', okrs=okrs)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit existing OKR"""
    okr = OKR.query.get_or_404(id)
    
    # Check if user has permission to edit this OKR
    if not (current_user.id == okr.assigned_to or current_user.is_admin()):
        flash('You do not have permission to edit this OKR.', 'error')
        return redirect(url_for('okr.view', id=id))
    
    form = OKRForm(obj=okr)
    
    # Populate choices for form fields
    form.team_id.choices = [(0, 'Select Team')] + [(team.id, team.name) for team in Team.query.all()]
    form.assigned_to.choices = [(0, 'Select User')] + [(user.id, user.get_full_name()) for user in User.query.all()]
    
    if form.validate_on_submit():
        # Update OKR
        okr.title = form.title.data
        okr.description = form.description.data
        okr.start_date = form.start_date.data
        okr.end_date = form.end_date.data
        okr.team_id = form.team_id.data
        okr.assigned_to = form.assigned_to.data
        
        # Update key results
        key_results = okr.key_results.all()
        
        # Update first key result
        if key_results and len(key_results) > 0:
            key_results[0].title = form.key_result_1_title.data
            key_results[0].description = form.key_result_1_description.data
            key_results[0].target_value = form.key_result_1_target.data
            key_results[0].unit = form.key_result_1_unit.data or 'count'
        elif form.key_result_1_title.data:
            kr = KeyResult(
                title=form.key_result_1_title.data,
                description=form.key_result_1_description.data,
                target_value=form.key_result_1_target.data,
                unit=form.key_result_1_unit.data or 'count',
                current_value=0,
                okr_id=okr.id
            )
            db.session.add(kr)
        
        # Update second key result
        if key_results and len(key_results) > 1:
            key_results[1].title = form.key_result_2_title.data
            key_results[1].description = form.key_result_2_description.data
            key_results[1].target_value = form.key_result_2_target.data
            key_results[1].unit = form.key_result_2_unit.data or 'count'
        elif form.key_result_2_title.data:
            kr = KeyResult(
                title=form.key_result_2_title.data,
                description=form.key_result_2_description.data,
                target_value=form.key_result_2_target.data,
                unit=form.key_result_2_unit.data or 'count',
                current_value=0,
                okr_id=okr.id
            )
            db.session.add(kr)
        
        # Update third key result
        if key_results and len(key_results) > 2:
            key_results[2].title = form.key_result_3_title.data
            key_results[2].description = form.key_result_3_description.data
            key_results[2].target_value = form.key_result_3_target.data
            key_results[2].unit = form.key_result_3_unit.data or 'count'
        elif form.key_result_3_title.data:
            kr = KeyResult(
                title=form.key_result_3_title.data,
                description=form.key_result_3_description.data,
                target_value=form.key_result_3_target.data,
                unit=form.key_result_3_unit.data or 'count',
                current_value=0,
                okr_id=okr.id
            )
            db.session.add(kr)
        
        db.session.commit()
        flash('OKR updated successfully!', 'success')
        return redirect(url_for('okr.view', id=okr.id))
    
    # Pre-populate form with existing key results
    key_results = okr.key_results.all()
    if key_results:
        if len(key_results) > 0:
            form.key_result_1_title.data = key_results[0].title
            form.key_result_1_description.data = key_results[0].description
            form.key_result_1_target.data = key_results[0].target_value
            form.key_result_1_unit.data = key_results[0].unit
        if len(key_results) > 1:
            form.key_result_2_title.data = key_results[1].title
            form.key_result_2_description.data = key_results[1].description
            form.key_result_2_target.data = key_results[1].target_value
            form.key_result_2_unit.data = key_results[1].unit
        if len(key_results) > 2:
            form.key_result_3_title.data = key_results[2].title
            form.key_result_3_description.data = key_results[2].description
            form.key_result_3_target.data = key_results[2].target_value
            form.key_result_3_unit.data = key_results[2].unit
    
    return render_template('okr/edit.html', form=form, okr=okr)

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    """Delete OKR"""
    okr = OKR.query.get_or_404(id)
    
    # Check if user has permission to delete this OKR
    if not (current_user.id == okr.assigned_to or current_user.is_admin()):
        flash('You do not have permission to delete this OKR.', 'error')
        return redirect(url_for('okr.view', id=id))
    
    # Delete associated key results first
    KeyResult.query.filter_by(okr_id=id).delete()
    
    # Delete the OKR
    db.session.delete(okr)
    db.session.commit()
    
    flash('OKR deleted successfully!', 'success')
    return redirect(url_for('okr.my_okrs'))

