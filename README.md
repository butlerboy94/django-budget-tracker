Django Budget Tracker

A full-stack financial management web application built with Django that allows users to track income, expenses, and bills through an interactive dashboard. 
This project was developed as a capstone application to demonstrate backend development, database design, authentication, financial logic processing, 
and professional version-controlled software engineering workflow.

Project Overview

The Django Budget Tracker is a secure, user-authenticated budgeting application that enables individuals to manage personal finances efficiently. Users can record income and expense transactions, manage bills, and monitor financial summaries through a dynamic dashboard.

This project demonstrates:
- Clean relational database design
- Secure per-user data isolation
- Financial aggregation using Django ORM
- Full CRUD functionality
- Real-world Git and GitHub workflow practices

Features
- User authentication (login/logout)
- Secure user-specific financial data
- Add income and expense transactions
- Add and manage bills
- Mark bills as paid or unpaid
- Financial dashboard displaying:
  - Total income
  - Total expenses
  - Net balance
  - Bill statistics (total, paid, unpaid)
- Recent transaction display
- Real-time calculations using Django ORM aggregation
- Git version control with remote GitHub repository

Tech Stack
- Python 3
- Django
- SQLite
- HTML
- Git
- GitHub

Database Design
Transaction Model
- User (ForeignKey)
- Date
- Type (Income / Expense)
- Category
- Amount
- Optional note

Bill Model
- User (ForeignKey)
- Name
- Amount
- Due date
- Paid status (Boolean)
- Optional notes
Database indexing is implemented for optimized querying by user and date.

Installation & Setup

Clone the repository:
- git clone https://github.com/butlerboy94/django-budget-tracker.git
- cd django-budget-tracker

Create and activate a virtual environment:
- python -m venv venv
- venv\Scripts\activate

Install Django:
- pip install django

Run migrations:
- python manage.py migrate

Create a superuser (optional):
- python manage.py createsuperuser

Start the devlopment server:
- python manage.py runserver

Open the browser:
- http://127.0.0.1:8000/

Development Workflow

This project follows a professional Git workflow:

- Local development environment
- Structured commits
- Remote repository hosted on GitHub
- Incremental feature development
- Version-controlled history tracking

All new features are committed and pushed to GitHub to simulate real-world software engineering practices.

Future Enhancements
- Monthly budgeting filters
- Financial data visualization (charts)
- Exportable reports (CSV or PDF)
- Recurring bill automation
- UI/UX improvements
- Category management system

Author

- Kaleb Butler
- Associate of Applied Science – Computer Programming
- Rose State College
- GitHub: https://github.com/butlerboy94
