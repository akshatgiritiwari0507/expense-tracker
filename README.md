# Basic Expense Tracker

A production-ready Flask web application for tracking personal expenses with user authentication, dashboard analytics, and date-wise expense management.

## 🚀 Features

- **User Authentication**: Secure signup, login, logout with password hashing
- **Expense Management**: Full CRUD operations for expenses
- **Dashboard Analytics**: Total spent, today's spent, category-wise totals, recent expenses
- **Date Filtering**: Filter expenses by date range with day-wise grouping
- **Responsive Design**: Mobile-friendly Bootstrap 5 interface
- **Database Support**: SQLite for local development, PostgreSQL for production
- **Security**: CSRF protection, session management, input validation

## 🛠️ Tech Stack

- **Backend**: Python 3.8+, Flask 2.3.3
- **Database**: Flask-SQLAlchemy (SQLite/PostgreSQL)
- **Authentication**: Flask-Login, Werkzeug
- **Forms**: Flask-WTF, WTForms
- **Frontend**: Bootstrap 5, Jinja2 templates
- **Deployment**: Gunicorn WSGI server
- **Environment**: python-dotenv

## 📁 Project Structure

```
expense-tracker/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuration settings
│   ├── models.py            # SQLAlchemy models (User, Expense)
│   ├── routes.py            # Application routes and views
│   ├── forms.py             # WTForms definitions
│   └── utils.py             # Helper functions
├── templates/               # Jinja2 HTML templates
│   ├── base.html           # Base template
│   ├── login.html          # Login page
│   ├── signup.html         # Signup page
│   ├── dashboard.html      # Dashboard view
│   ├── all_expenses.html   # All expenses with filters
│   └── add_edit_expense.html # Add/Edit expense form
├── static/
│   └── css/
│       └── style.css       # Custom CSS styles
├── instance/                # Database storage (SQLite)
├── .env                     # Environment variables
├── .gitignore              # Git ignore file
├── requirements.txt        # Python dependencies
├── run.py                  # WSGI entry point
├── README.md               # This file
└── deploy.md               # Deployment instructions
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
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

4. **Set up environment variables**
   ```bash
   # Copy the example .env file and modify it
   cp .env.example .env
   
   # Edit .env file with your settings
   # At minimum, change the SECRET_KEY
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## 🔧 Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here-change-in-production
FLASK_ENV=development
FLASK_DEBUG=True

# Database Configuration
# For local development (SQLite) - automatically configured
# DATABASE_URL=sqlite:///instance/expense.db

# For production (PostgreSQL)
# DATABASE_URL=postgresql://username:password@hostname:port/database_name
```

## 📊 Usage

### Getting Started

1. **Sign up** for a new account
2. **Log in** with your credentials
3. **Add expenses** using the "Add Expense" button
4. **View dashboard** for spending analytics
5. **Filter expenses** by date range in the "All Expenses" section

### Categories

The app supports the following expense categories:
- Food
- Travel
- Shopping
- Bills
- Entertainment
- Others

## 🚀 Deployment

### Deploying to Render

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Create Render Account**
   - Sign up at [render.com](https://render.com)
   - Connect your GitHub repository

3. **Configure Web Service**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn run:app`
   - Add PostgreSQL database (optional but recommended)

4. **Set Environment Variables**
   - `SECRET_KEY`: Generate a secure random key
   - `DATABASE_URL`: Provided by Render if using PostgreSQL

For detailed deployment instructions, see [deploy.md](deploy.md).

## 🧪 Testing

Run the test suite:

```bash
pytest
```

## 🔒 Security Features

- **Password Hashing**: Uses Werkzeug's secure password hashing
- **CSRF Protection**: All forms protected with CSRF tokens
- **Session Management**: Secure session handling with Flask-Login
- **Input Validation**: Form validation with WTForms
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

If you encounter any issues or have questions, please:

1. Check the [Issues](../../issues) section
2. Create a new issue with detailed information
3. Include steps to reproduce any bugs

## 🔮 Future Scope

- Charts and visualizations for spending trends
- CSV export functionality
- Monthly/weekly reports
- Budget alerts and limits
- Recurring expenses
- REST API for mobile app integration
- Multi-currency support
- Expense categories customization
- Receipt image upload

---

**Built with ❤️ using Flask and Bootstrap**
