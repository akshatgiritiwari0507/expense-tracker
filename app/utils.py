from datetime import datetime, date
from decimal import Decimal
import calendar

def format_currency(amount):
    """Format amount as currency with 2 decimal places"""
    if amount is None:
        return "$0.00"
    return f"${amount:.2f}"

def format_date(date_obj):
    """Format date object to readable string"""
    if date_obj is None:
        return ""
    if isinstance(date_obj, datetime):
        return date_obj.strftime('%B %d, %Y')
    return date_obj.strftime('%B %d, %Y')

def get_month_name(month_number):
    """Get month name from month number"""
    return calendar.month_name[month_number]

def get_date_range_for_month(year, month):
    """Get start and end date for a given month"""
    start_date = date(year, month, 1)
    last_day = calendar.monthrange(year, month)[1]
    end_date = date(year, month, last_day)
    return start_date, end_date

def calculate_percentage_change(old_value, new_value):
    """Calculate percentage change between two values"""
    if old_value == 0:
        return 0 if new_value == 0 else 100
    return ((new_value - old_value) / old_value) * 100

def get_current_month_expenses(user_id, db_session):
    """Get total expenses for current month"""
    today = date.today()
    start_date, end_date = get_date_range_for_month(today.year, today.month)
    
    from app.models import Expense
    total = db_session.query(db_session.query(Expense.amount).filter(
        Expense.user_id == user_id,
        Expense.date >= start_date,
        Expense.date <= end_date
    ).scalar() or 0)
    
    return total

def get_previous_month_expenses(user_id, db_session):
    """Get total expenses for previous month"""
    today = date.today()
    if today.month == 1:
        prev_month = 12
        prev_year = today.year - 1
    else:
        prev_month = today.month - 1
        prev_year = today.year
    
    start_date, end_date = get_date_range_for_month(prev_year, prev_month)
    
    from app.models import Expense
    total = db_session.query(db_session.query(Expense.amount).filter(
        Expense.user_id == user_id,
        Expense.date >= start_date,
        Expense.date <= end_date
    ).scalar() or 0)
    
    return total

def validate_date_format(date_string, format='%Y-%m-%d'):
    """Validate date string format"""
    try:
        datetime.strptime(date_string, format)
        return True
    except ValueError:
        return False

def safe_float_conversion(value, default=0.0):
    """Safely convert value to float"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default
