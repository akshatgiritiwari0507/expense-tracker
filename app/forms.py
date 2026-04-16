from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SelectField, TextAreaField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional
from wtforms.widgets import TextArea
from app.models import User

class LoginForm(FlaskForm):
    """Login form for user authentication"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    """Signup form for new user registration"""
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_email(self, field):
        """Custom validator to check if email already exists"""
        if User.query.filter_by(email=field.data).first():
            raise ValueError('Email already registered. Please use a different email.')

class ExpenseForm(FlaskForm):
    """Form for adding and editing expenses"""
    amount = FloatField('Amount', validators=[
        DataRequired(), 
        NumberRange(min=0.01, message='Amount must be greater than 0')
    ])
    category = SelectField('Category', 
                          choices=[
                              ('Food', 'Food'),
                              ('Travel', 'Travel'),
                              ('Shopping', 'Shopping'),
                              ('Bills', 'Bills'),
                              ('Entertainment', 'Entertainment'),
                              ('Others', 'Others')
                          ],
                          validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Save Expense')

class ExpenseFilterForm(FlaskForm):
    """Form for filtering expenses by date range"""
    from_date = DateField('From Date', validators=[DataRequired()], format='%Y-%m-%d')
    to_date = DateField('To Date', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Filter')

class IncomeForm(FlaskForm):
    """Form for adding and editing income"""
    amount = FloatField('Amount', validators=[
        DataRequired(), 
        NumberRange(min=0.01, message='Amount must be greater than 0')
    ])
    source = SelectField('Source', 
                        choices=[
                            ('Salary', 'Salary'),
                            ('Business', 'Business'),
                            ('Investment', 'Investment'),
                            ('Freelance', 'Freelance'),
                            ('Others', 'Others')
                        ],
                        validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Save Income')

class ChangePasswordForm(FlaskForm):
    """Form for changing user password"""
    old_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(), 
        Length(min=6, message='Password must be at least 6 characters long')
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(), 
        EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('Change Password')
