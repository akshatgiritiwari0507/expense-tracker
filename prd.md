# Basic Expense Tracker — PRD + Windsurf Build Prompts

## 1) Project Goal

Build a **production-ready Basic Expense Tracker web app** focused on backend learning and internship mid-review.

Primary goals:

* Clean backend architecture
* Authentication + session management
* Expense CRUD
* Dashboard summaries
* Date-wise filtering
* GitHub-ready structure
* Render deployment ready
* Local SQLite + production PostgreSQL support

---

## 2) Final Tech Stack

* **Backend:** Python + Flask
* **ORM:** Flask-SQLAlchemy
* **Auth:** Flask-Login + Werkzeug password hashing
* **Templates:** Jinja2
* **Frontend:** Bootstrap 5 CDN
* **Local DB:** SQLite
* **Production DB:** PostgreSQL
* **Deployment:** Render
* **WSGI:** Gunicorn
* **Env:** python-dotenv

---

## 3) Final Folder Structure

```text
expense-tracker/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── routes.py
│   ├── forms.py
│   └── utils.py
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── all_expenses.html
│   └── add_edit_expense.html
├── static/
│   └── css/
│       └── style.css
├── instance/
├── .env
├── .gitignore
├── requirements.txt
├── README.md
├── deploy.md
└── run.py
```

---

## 4) Functional Requirements

### Authentication

* Signup with name, email, password
* Login
* Logout
* Password hashing
* Session-based authentication
* Protect all expense routes

### Expense CRUD

* Add expense
* View expenses
* Edit expense
* Delete expense
* Fields:

  * amount
  * category
  * description
  * date (default today)

### Dashboard

* Total spent (all-time)
* Today spent
* Category-wise totals table
* Recent 5 expenses
* Add expense CTA button

### All Expenses

* From date / to date filter
* Default = today
* Group expenses by date
* Table under each date
* Edit + delete actions

### Categories

Hardcoded dropdown:

* Food
* Travel
* Shopping
* Bills
* Entertainment
* Others

---

## 5) Database Schema

```sql
users (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
)

expenses (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  amount REAL NOT NULL,
  category TEXT NOT NULL,
  description TEXT,
  date DATE NOT NULL,
  FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
)
```

---

## 6) Non-Functional Requirements

* Clean modular code
* Mobile responsive UI
* Bootstrap green theme
* GitHub-ready code quality
* Render deployment compatibility
* `.env` based config
* No unnecessary libraries
* Beginner-friendly readable code

---

igone 7 ang 8 as i will manuallly give you these commands

# 7) Windsurf Master Prompt

Use this as the **main prompt** in Windsurf.

```text
Build a production-ready Flask web app named "Basic Expense Tracker".

Requirements:
- Use Flask app factory pattern
- Use Flask-SQLAlchemy
- Use Flask-Login session auth
- Use Werkzeug password hashing
- Use SQLite locally and PostgreSQL in production via DATABASE_URL
- Use Bootstrap 5 CDN + Jinja templates
- Use clean modular structure exactly as provided
- Create all required templates
- Add login/signup/logout
- Implement full expense CRUD
- Add dashboard with total spent, today spent, category totals, recent expenses
- Add all expenses page with date range filter and day-wise grouped tables
- Use hardcoded categories dropdown
- Add .gitignore, README.md, deploy.md
- Keep code deployment-ready for Render
- Ensure run.py works with gunicorn run:app
- Keep code simple, readable, internship-review friendly
- Add comments where useful
```

---

# 8) Phase-wise Windsurf Prompts

Use these prompts one by one for better results.

## Prompt 1 — Setup + Config

```text
Create the complete Flask project skeleton with app factory pattern, config.py, SQLAlchemy setup, Flask-Login setup, .env support, requirements.txt, .gitignore, and run.py. Ensure SQLite local support and PostgreSQL production support.
```

## Prompt 2 — Models + Auth

```text
Create SQLAlchemy models for User and Expense with proper relationships. Implement signup, login, logout, password hashing, session auth, and protected routes.
```

## Prompt 3 — Expense CRUD

```text
Implement add, edit, delete, and list expense routes with Bootstrap templates. Use category dropdown and date default as today.
```

## Prompt 4 — Dashboard

```text
Create dashboard route and template showing total spent, today's spent, category-wise totals, and recent 5 expenses.
```

## Prompt 5 — Date Filters

```text
Create all expenses page with from-date and to-date filter. Group expenses by day and render separate Bootstrap tables for each date.
```

## Prompt 6 — Deployment

```text
Prepare the project for GitHub and Render deployment. Add README.md with setup steps and deploy.md with Render instructions including build and start command.
```

---

## 9) GitHub README Sections

* Overview
* Features
* Tech stack
* Folder structure
* Installation
* Environment variables
* Run locally
* Deployment
* Future scope

---

## 10) Render Deployment Requirements

* Build command: `pip install -r requirements.txt`
* Start command: `gunicorn run:app`
* Add PostgreSQL database
* Set `SECRET_KEY`
* Set `DATABASE_URL`

---

## 11) Future Scope (Only mention in README/PPT)

* Charts
* CSV export
* Monthly reports
* Budget alerts
* Recurring expenses
* REST APIs
