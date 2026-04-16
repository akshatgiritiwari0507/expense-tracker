# Basic Expense Tracker

A comprehensive Flask web application for tracking personal expenses and income with advanced analytics, search functionality, and user management.

## [Live Demo](https://expense-tracker-dycf.onrender.com/dashboard) 

## Features

### User Management
- **Secure Authentication**: Signup, login, logout with password hashing
- **Password Change**: Secure password update with old password verification
- **Session Management**: Persistent sessions with auto-logout

### Expense Management
- **Full CRUD Operations**: Add, edit, delete, view expenses
- **Income Tracking**: Complete income management with sources
- **Search Functionality**: Search expenses/income by category, description, or both
- **Date Filtering**: Filter by date range with day-wise grouping
- **Visual Separation**: Today's entries highlighted with special styling

### Dashboard Analytics
- **Financial Overview**: Total income, expenses, and balance
- **Daily Tracking**: Today's income and expenses
- **Recent Activity**: Last 5 expenses and income entries
- **Currency Support**: Indian Rupees (Rs) formatting

### User Experience
- **Responsive Design**: Mobile-friendly Bootstrap 5 interface
- **Smart Notifications**: Hover notifications for page transitions
- **Auto-dismiss Messages**: Flash messages that disappear automatically
- **Date Sorting**: Higher dates appear first in lists
- **Visual Hierarchy**: Clear separation between different days

### Technical Features
- **Database Support**: SQLite for local, PostgreSQL for production
- **Security**: CSRF protection, input validation, secure sessions
- **Production Ready**: Optimized for deployment with proper configuration

## 🛠️ Tech Stack

- **Backend**: Python 3.12, Flask 2.3.3
- **Database**: Flask-SQLAlchemy (SQLite/PostgreSQL)
- **Authentication**: Flask-Login, Werkzeug
- **Forms**: Flask-WTF, WTForms
- **Frontend**: Bootstrap 5, Jinja2 templates
- **Deployment**: Gunicorn WSGI server
- **Environment**: python-dotenv
- **Production**: Render hosting with PostgreSQL

## 📁 Project Structure

```
expense-tracker/
|-- app/
|   |-- __init__.py          # Flask app factory with custom filters
|   |-- config.py            # Production-ready configuration
|   |-- models.py            # SQLAlchemy models (User, Expense, Income)
|   |-- routes.py            # Complete CRUD routes and views
|   |-- forms.py             # All form definitions
|   |-- utils.py             # Helper functions
|-- templates/               # Complete UI templates
|   |-- base.html           # Base template with notifications
|   |-- login.html          # User authentication
|   |-- signup.html         # User registration
|   |-- dashboard.html      # Financial dashboard
|   |-- all_expenses.html   # Expense listing with search
|   |-- all_income.html     # Income listing with search
|   |-- add_edit_expense.html # Expense form
|   |-- edit_income.html    # Income form
|   |-- change_password.html # Password change form
|-- static/
|   |-- css/
|       |-- style.css       # Custom styling
|-- instance/                # Local database storage
|-- .env                     # Environment variables
|-- .gitignore              # Git ignore file
|-- requirements.txt        # Python dependencies
|-- runtime.txt              # Python version for deployment
|-- .python-version         # Python version specification
|-- Procfile                # Deployment configuration
|-- run.py                  # WSGI entry point
|-- README.md               # This file
|-- deploy.md               # Deployment guide
```

## Installation

### Prerequisites

- Python 3.12 or higher
- pip (Python package manager)
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/akshatgiritiwari0507/expense-tracker.git
   cd expense-tracker
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

### Environment Variables

Create a `.env` file in the project root:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True

# Database (SQLite automatically configured for local)
# DATABASE_URL=sqlite:///expense.db
```

## Usage

### Getting Started

1. **Sign up** for a new account
2. **Log in** with your credentials
3. **Add expenses** and **income** using the dashboard buttons
4. **View analytics** on the dashboard
5. **Search and filter** expenses/income by date, category, or description
6. **Change password** from user dropdown menu

### Features Overview

#### Expense Categories
- Food, Travel, Shopping, Bills, Entertainment, Others

#### Income Sources  
- Salary, Business, Investment, Freelance, Others

#### Search Functionality
- Search by category/source, description, or both
- Filter by date range
- Today's entries visually highlighted

#### Dashboard Analytics
- Total income, expenses, and balance
- Today's financial summary
- Recent 5 expenses and income entries
- Currency in Indian Rupees (Rs)

## Deployment

### Quick Deploy to Render

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Render**
   - Sign up at [render.com](https://render.com)
   - Connect your GitHub repository
   - Configure Web Service:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn run:app`
     - **Runtime**: Python 3
   - Add Environment Variables:
     - `SECRET_KEY`: Generate secure key
     - `FLASK_ENV`: `production`
   - Add PostgreSQL database (recommended)

3. **Your app will be live at**: `https://your-app-name.onrender.com`

### Production Configuration

The app automatically switches between SQLite (local) and PostgreSQL (production) based on `DATABASE_URL` environment variable.

For detailed deployment instructions, see [deploy.md](deploy.md).

## Security Features

- **Password Hashing**: Werkzeug secure password hashing
- **CSRF Protection**: All forms protected with CSRF tokens
- **Session Management**: Secure Flask-Login sessions
- **Input Validation**: WTForms validation on all inputs
- **SQL Injection Protection**: SQLAlchemy ORM protection
- **Environment Variables**: Secure configuration management

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions:

1. Check the [Issues](../../issues) section
2. Create a new issue with detailed information
3. Include steps to reproduce any bugs

## Future Enhancements

- Charts and visualizations for spending trends
- CSV export functionality
- Monthly/weekly reports
- Budget alerts and limits
- Recurring expenses
- REST API for mobile app integration
- Multi-currency support
- Custom expense categories
- Receipt image upload

---

**Built with using Flask, Bootstrap 5, and deployed on Render**

## Show Your Support

If you find this project helpful, please give it a star! 

[Live Demo](https://expense-tracker-dycf.onrender.com/dashboard) | [GitHub Repository](https://github.com/akshatgiritiwari0507/expense-tracker)
