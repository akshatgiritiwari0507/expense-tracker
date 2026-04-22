from datetime import datetime, date
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import func, desc
from app import db
from app.models import User, Expense, Income, Category
from app.forms import LoginForm, SignupForm, ExpenseForm, ExpenseFilterForm, IncomeForm, ChangePasswordForm, CategoryForm, ReportForm
from app.reports import ReportGenerator

# Create blueprint
main = Blueprint('main', __name__)

# Authentication routes
@main.route('/')
def index():
    """Redirect to dashboard if logged in, otherwise to login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    """Login route for user authentication"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html', form=form)

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup route for new user registration"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = SignupForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('signup.html', form=form)

@main.route('/logout')
@login_required
def logout():
    """Logout route to end user session"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

@main.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change user password"""
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Password changed successfully!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Current password is incorrect.', 'error')
    
    return render_template('change_password.html', form=form)

# Dashboard route
@main.route('/dashboard')
@login_required
def dashboard():
    """Dashboard showing expense summaries and recent expenses"""
    # Get total spent (all-time)
    total_spent = db.session.query(func.sum(Expense.amount)).filter_by(user_id=current_user.id).scalar() or 0
    
    # Get total income (all-time)
    total_income = db.session.query(func.sum(Income.amount)).filter_by(user_id=current_user.id).scalar() or 0
    
    # Get today's spent
    today = date.today()
    today_spent = db.session.query(func.sum(Expense.amount)).filter_by(user_id=current_user.id).filter(Expense.date == today).scalar() or 0
    
    # Get today's income
    today_income = db.session.query(func.sum(Income.amount)).filter_by(user_id=current_user.id).filter(Income.date == today).scalar() or 0
    
    # Calculate balance
    balance = total_income - total_spent
    
    # Get category-wise totals
    category_totals = db.session.query(
        Expense.category, 
        func.sum(Expense.amount).label('total')
    ).filter_by(user_id=current_user.id).group_by(Expense.category).all()
    
    # Get recent 5 expenses
    recent_expenses = Expense.query.filter_by(user_id=current_user.id).order_by(desc(Expense.created_at)).limit(5).all()
    
    # Get recent 5 income
    recent_income = Income.query.filter_by(user_id=current_user.id).order_by(desc(Income.created_at)).limit(5).all()
    
    return render_template('dashboard.html', 
                         total_spent=total_spent,
                         total_income=total_income,
                         balance=balance,
                         today_spent=today_spent,
                         today_income=today_income,
                         category_totals=category_totals,
                         recent_expenses=recent_expenses,
                         recent_income=recent_income)

# Expense CRUD routes
@main.route('/expenses')
@login_required
def all_expenses():
    """Show all expenses with date filtering and search"""
    # Default to empty (show all data)
    from_date = request.args.get('from_date', '')
    to_date = request.args.get('to_date', '')
    search_query = request.args.get('search', '').strip()
    search_type = request.args.get('search_type', 'both')
    
    form = ExpenseFilterForm()
    
    # Query expenses - apply date filter only if dates are provided
    expenses = Expense.query.filter_by(user_id=current_user.id)
    
    if from_date and to_date:
        form.from_date.data = datetime.strptime(from_date, '%Y-%m-%d').date()
        form.to_date.data = datetime.strptime(to_date, '%Y-%m-%d').date()
        expenses = expenses.filter(
            Expense.date >= form.from_date.data,
            Expense.date <= form.to_date.data
        )
    
    # Apply search filter
    if search_query:
        if search_type == 'category':
            expenses = expenses.filter(Expense.category.ilike(f'%{search_query}%'))
        elif search_type == 'description':
            expenses = expenses.filter(Expense.description.ilike(f'%{search_query}%'))
        else:  # both
            expenses = expenses.filter(
                (Expense.category.ilike(f'%{search_query}%')) |
                (Expense.description.ilike(f'%{search_query}%'))
            )
    
    # Sort by date (highest first)
    expenses = expenses.order_by(desc(Expense.date)).all()
    
    # Group expenses by date
    expenses_by_date = {}
    
    for expense in expenses:
        expense_date = expense.date.strftime('%Y-%m-%d')
        if expense_date not in expenses_by_date:
            expenses_by_date[expense_date] = []
        expenses_by_date[expense_date].append(expense)
    
    # Sort dates in descending order (highest date first)
    ordered_expenses = {}
    for date_key in sorted(expenses_by_date.keys(), reverse=True):
        ordered_expenses[date_key] = expenses_by_date[date_key]
    
    expenses_by_date = ordered_expenses
    
    return render_template('all_expenses.html', 
                         form=form,
                         expenses_by_date=expenses_by_date,
                         from_date=from_date,
                         to_date=to_date,
                         search_query=search_query,
                         search_type=search_type,
                         today_date=date.today().strftime('%Y-%m-%d'))

@main.route('/expenses/filter', methods=['POST'])
@login_required
def filter_expenses():
    """Filter expenses by date range"""
    form = ExpenseFilterForm()
    if form.validate_on_submit():
        return redirect(url_for('main.all_expenses', 
                              from_date=form.from_date.data.strftime('%Y-%m-%d'),
                              to_date=form.to_date.data.strftime('%Y-%m-%d')))
    return redirect(url_for('main.all_expenses'))

@main.route('/income/add', methods=['POST'])
@login_required
def add_income():
    """Add a new income"""
    try:
        amount = float(request.form.get('amount'))
        source = request.form.get('source')
        description = request.form.get('description')
        income_date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        
        income = Income(
            user_id=current_user.id,
            amount=amount,
            source=source,
            description=description,
            date=income_date
        )
        db.session.add(income)
        db.session.commit()
        flash('Income added successfully!', 'success')
    except Exception as e:
        flash('Error adding income. Please try again.', 'error')
    
    return redirect(url_for('main.dashboard'))

# Income CRUD routes
@main.route('/income')
@login_required
def all_income():
    """Show all income with date filtering and search"""
    # Default to empty (show all data)
    from_date = request.args.get('from_date', '')
    to_date = request.args.get('to_date', '')
    search_query = request.args.get('search', '').strip()
    search_type = request.args.get('search_type', 'both')
    
    # Query income - apply date filter only if dates are provided
    income_query = Income.query.filter_by(user_id=current_user.id)
    
    if from_date and to_date:
        income_query = income_query.filter(
            Income.date >= datetime.strptime(from_date, '%Y-%m-%d').date(),
            Income.date <= datetime.strptime(to_date, '%Y-%m-%d').date()
        )
    
    # Apply search filter
    if search_query:
        if search_type == 'source':
            income_query = income_query.filter(Income.source.ilike(f'%{search_query}%'))
        elif search_type == 'description':
            income_query = income_query.filter(Income.description.ilike(f'%{search_query}%'))
        else:  # both
            income_query = income_query.filter(
                (Income.source.ilike(f'%{search_query}%')) |
                (Income.description.ilike(f'%{search_query}%'))
            )
    
    # Sort by date (highest first)
    income_list = income_query.order_by(desc(Income.date)).all()
    
    # Group income by date
    income_by_date = {}
    
    for income in income_list:
        income_date = income.date.strftime('%Y-%m-%d')
        if income_date not in income_by_date:
            income_by_date[income_date] = []
        income_by_date[income_date].append(income)
    
    # Sort dates in descending order (highest date first)
    ordered_income = {}
    for date_key in sorted(income_by_date.keys(), reverse=True):
        ordered_income[date_key] = income_by_date[date_key]
    
    income_by_date = ordered_income
    
    return render_template('all_income.html', 
                         income_by_date=income_by_date,
                         from_date=from_date,
                         to_date=to_date,
                         search_query=search_query,
                         search_type=search_type,
                         today_date=date.today().strftime('%Y-%m-%d'))

@main.route('/income/edit/<int:income_id>', methods=['GET', 'POST'])
@login_required
def edit_income(income_id):
    """Edit an existing income"""
    income = Income.query.filter_by(id=income_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        try:
            income.amount = float(request.form.get('amount'))
            income.source = request.form.get('source')
            income.description = request.form.get('description')
            income.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
            income.updated_at = datetime.utcnow()
            
            db.session.commit()
            flash('Income updated successfully!', 'success')
            return redirect(url_for('main.all_income'))
        except Exception as e:
            flash('Error updating income. Please try again.', 'error')
    
    return render_template('edit_income.html', income=income)

@main.route('/income/delete/<int:income_id>', methods=['POST'])
@login_required
def delete_income(income_id):
    """Delete an income"""
    income = Income.query.filter_by(id=income_id, user_id=current_user.id).first_or_404()
    
    try:
        db.session.delete(income)
        db.session.commit()
        flash('Income deleted successfully!', 'success')
    except Exception as e:
        flash('Error deleting income. Please try again.', 'error')
    
    return redirect(url_for('main.all_income'))

@main.route('/expenses/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    """Add a new expense"""
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(
            user_id=current_user.id,
            amount=form.amount.data,
            category=form.category.data,
            description=form.description.data,
            date=form.date.data
        )
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    # Set default date to today
    if not form.date.data:
        form.date.data = date.today()
    
    # Get user categories
    categories = Category.query.filter_by(user_id=current_user.id).all()
    
    return render_template('add_edit_expense.html', form=form, title='Add Expense', categories=categories)

@main.route('/expenses/edit/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    """Edit an existing expense"""
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first_or_404()
    form = ExpenseForm(obj=expense)
    
    if form.validate_on_submit():
        expense.amount = form.amount.data
        expense.category = form.category.data
        expense.description = form.description.data
        expense.date = form.date.data
        expense.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Expense updated successfully!', 'success')
        return redirect(url_for('main.all_expenses'))
    
    # Get user categories
    categories = Category.query.filter_by(user_id=current_user.id).all()
    
    return render_template('add_edit_expense.html', form=form, title='Edit Expense', categories=categories)

@main.route('/expenses/delete/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    """Delete an expense"""
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first_or_404()
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully!', 'success')
    return redirect(url_for('main.all_expenses'))

# Category management routes
@main.route('/categories')
@login_required
def categories():
    """Display and manage expense categories"""
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('categories.html', categories=categories)

@main.route('/categories/add', methods=['GET', 'POST'])
@login_required
def add_category():
    """Add a new expense category"""
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            icon=form.icon.data,
            color=form.color.data,
            user_id=current_user.id
        )
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully!', 'success')
        return redirect(url_for('main.categories'))
    return render_template('add_category.html', form=form)

@main.route('/categories/edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    """Edit an existing expense category"""
    category = Category.query.filter_by(id=category_id, user_id=current_user.id).first_or_404()
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        category.name = form.name.data
        category.icon = form.icon.data
        category.color = form.color.data
        db.session.commit()
        flash('Category updated successfully!', 'success')
        return redirect(url_for('main.categories'))
    return render_template('edit_category.html', form=form, category=category)

@main.route('/categories/delete/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    """Delete an expense category"""
    category = Category.query.filter_by(id=category_id, user_id=current_user.id).first_or_404()
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('main.categories'))

# Report generation routes
@main.route('/reports')
@login_required
def reports():
    """Display financial reports and analytics"""
    form = ReportForm()
    return render_template('reports.html', form=form)

@main.route('/reports/generate', methods=['POST'])
@login_required
def generate_report():
    """Generate financial report"""
    form = ReportForm()
    if form.validate_on_submit():
        report_generator = ReportGenerator(current_user.id)
        
        # Determine date range
        start_date = form.from_date.data
        end_date = form.to_date.data
        
        if form.report_type.data == 'monthly':
            start_date = date(date.today().year, date.today().month, 1)
            end_date = date(date.today().year, date.today().month, 28)  # Simplified
        elif form.report_type.data == 'yearly':
            start_date = date(date.today().year, 1, 1)
            end_date = date(date.today().year, 12, 31)
        
        # Generate report
        if form.export_format.data == 'pdf':
            report_data = report_generator.generate_pdf_report(start_date, end_date, form.report_type.data)
            filename = f"financial_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        else:  # Excel
            report_data = report_generator.generate_excel_report(start_date, end_date)
            filename = f"financial_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        # Return file for download
        from flask import send_file
        import io
        return send_file(
            io.BytesIO(report_data),
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf' if form.export_format.data == 'pdf' else 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    flash('Please fill out the report form correctly.', 'danger')
    return redirect(url_for('main.reports'))

@main.route('/api/charts/spending')
@login_required
def spending_chart():
    """API endpoint for spending chart data"""
    chart_type = request.args.get('type', 'pie')
    report_generator = ReportGenerator(current_user.id)
    chart_data = report_generator.generate_spending_chart(chart_type)
    return jsonify({'chart_data': chart_data})

@main.route('/api/charts/trends')
@login_required
def trends_chart():
    """API endpoint for trends chart data"""
    report_generator = ReportGenerator(current_user.id)
    chart_data = report_generator.generate_trend_chart()
    return jsonify({'chart_data': chart_data})

@main.route('/api/dashboard-stats')
@login_required
def dashboard_stats():
    """API endpoint for dashboard statistics"""
    total_expenses = db.session.query(func.sum(Expense.amount)).filter_by(user_id=current_user.id).scalar() or 0
    total_income = db.session.query(func.sum(Income.amount)).filter_by(user_id=current_user.id).scalar() or 0
    balance = total_income - total_expenses
    total_transactions = db.session.query(Expense).filter_by(user_id=current_user.id).count() + \
                        db.session.query(Income).filter_by(user_id=current_user.id).count()
    
    return jsonify({
        'total_expenses': total_expenses,
        'total_income': total_income,
        'balance': balance,
        'total_transactions': total_transactions
    })

# Error handlers
@main.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@main.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('500.html'), 500
