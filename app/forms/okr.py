from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SelectField, FieldList, FormField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, Optional
from datetime import date, datetime
from app.models import Team, User

class KeyResultForm(FlaskForm):
    """Form for individual Key Results"""
    title = StringField('Key Result Title', validators=[
        DataRequired(), 
        Length(min=1, max=200)
    ])
    description = TextAreaField('Description', validators=[Length(max=500)])
    target_value = FloatField('Target Value', validators=[
        DataRequired(),
        NumberRange(min=0.1, message="Target value must be greater than 0")
    ])
    current_value = FloatField('Current Value', validators=[
        NumberRange(min=0, message="Current value cannot be negative")
    ], default=0.0)
    unit = StringField('Unit', validators=[Length(max=20)], 
                      render_kw={"placeholder": "e.g., %, count, $, users"})

class OKRForm(FlaskForm):
    """Form for creating/editing OKRs"""
    title = StringField('Objective Title', validators=[
        DataRequired(), 
        Length(min=1, max=200)
    ])
    description = TextAreaField('Objective Description', validators=[Length(max=1000)])
    start_date = DateField('Start Date', validators=[DataRequired()], default=date.today)
    end_date = DateField('End Date', validators=[DataRequired()])
    team_id = SelectField('Team', coerce=int, validators=[DataRequired()])
    assigned_to = SelectField('Assign To', coerce=int, validators=[DataRequired()])
    
    # Key Results (we'll add these dynamically)
    key_result_1_title = StringField('Key Result 1 Title', validators=[DataRequired(), Length(min=1, max=200)])
    key_result_1_description = TextAreaField('Key Result 1 Description', validators=[Optional()])
    key_result_1_target = FloatField('Key Result 1 Target', validators=[DataRequired(), NumberRange(min=0.01)], default=1.0)
    key_result_1_unit = StringField('Key Result 1 Unit', validators=[Optional(), Length(max=20)], default='count')
    
    key_result_2_title = StringField('Key Result 2 Title', validators=[DataRequired(), Length(min=1, max=200)])
    key_result_2_description = TextAreaField('Key Result 2 Description', validators=[Optional()])
    key_result_2_target = FloatField('Key Result 2 Target', validators=[DataRequired(), NumberRange(min=0.01)], default=1.0)
    key_result_2_unit = StringField('Key Result 2 Unit', validators=[Optional(), Length(max=20)], default='count')
    
    key_result_3_title = StringField('Key Result 3 Title', validators=[Optional(), Length(max=200)])
    key_result_3_description = TextAreaField('Key Result 3 Description', validators=[Optional()])
    key_result_3_target = FloatField('Key Result 3 Target', validators=[Optional(), NumberRange(min=0.01)])
    key_result_3_unit = StringField('Key Result 3 Unit', validators=[Optional(), Length(max=20)])
    
    submit = SubmitField('Create OKR')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate team choices
        self.team_id.choices = [(0, 'Select Team')] + [(t.id, t.name) for t in Team.query.all()]
        self.assigned_to.choices = [(0, 'Select User')] + [(u.id, u.get_full_name()) for u in User.query.all()]
    
    def validate_end_date(self, end_date):
        if end_date.data <= self.start_date.data:
            raise ValidationError('End date must be after start date.')
    
    def validate_team_id(self, team_id):
        if team_id.data == 0:
            raise ValidationError('Please select a team.')
    
    def validate_assigned_to(self, assigned_to):
        if assigned_to.data == 0:
            raise ValidationError('Please select a user to assign this OKR to.')

class UpdateProgressForm(FlaskForm):
    """Form for updating OKR progress"""
    current_value = FloatField('Current Value', validators=[
        DataRequired(),
        NumberRange(min=0, message="Current value cannot be negative")
    ])
    submit = SubmitField('Update Progress')