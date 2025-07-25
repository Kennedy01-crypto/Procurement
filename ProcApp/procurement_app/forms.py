# procurement_app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DecimalField, IntegerField, FileField, FieldList, FormField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NumberRange
from .models import User, Department
from wtforms_sqlalchemy.fields import QuerySelectField


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[
        ('ADA', 'ADA'),
        ('Dept Accountant', 'Dept Accountant'),
        ('SCM', 'SCM'),
        ('Chief Officer', 'Chief Officer')
    ], validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class AIELineItemForm(FlaskForm):
    class Meta:
        # This is needed to avoid CSRF token generation for each subform
        csrf = False
    description = StringField('Description', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    unit_price = DecimalField('Unit Price', validators=[DataRequired(), NumberRange(min=0)])

def department_query():
    # This function will be used by the QuerySelectField to get the department choices
    return Department.query

class AIEForm(FlaskForm):
    procurement_plan_id = StringField('Procurement Plan ID/Ref No.', validators=[DataRequired()])
    department = QuerySelectField('Department', query_factory=department_query, get_label='name', allow_blank=False, validators=[DataRequired()])
    justification = TextAreaField('Justification', validators=[DataRequired()])
    supporting_docs = FileField('Supporting Documents') # Validation can be added if needed
    line_items = FieldList(FormField(AIELineItemForm), min_entries=1)
    submit = SubmitField('Submit AIE')
