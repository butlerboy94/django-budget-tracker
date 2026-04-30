# Django Budget Tracker

A full-stack personal finance web application built with Django. Users can track income, expenses, and bills through a secure, authenticated dashboard with real-time financial summaries.

Built as a capstone project to demonstrate backend development, relational database design, user authentication, Django ORM aggregation, and automated testing.

---

## Features

- **User Authentication** — Secure registration, login, and logout with auto-login after signup
- **Transaction Tracking** — Full CRUD for income and expense transactions, categorized and dated
- **Bills Management** — Add bills with due dates, mark as paid/unpaid, and track totals
- **Financial Dashboard** — Live summary of total income, total expenses, net balance, and bill stats
- **Per-User Data Isolation** — All data is scoped to the authenticated user; no cross-user data leakage
- **Automated Tests** — Test coverage for CRUD operations and user access control

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django |
| Database | SQLite (development) |
| Language | Python 3 |
| Frontend | Django Templates · HTML · CSS |
| Version Control | Git · GitHub |

---

## Database Design

### Transaction Model
| Field | Type | Notes |
|---|---|---|
| user | ForeignKey | Scoped per user |
| date | DateField | |
| type | CharField | Income or Expense |
| category | CharField | |
| amount | DecimalField | |
| note | TextField | Optional |

### Bill Model
| Field | Type | Notes |
|---|---|---|
| user | ForeignKey | Scoped per user |
| name | CharField | |
| amount | DecimalField | |
| due_date | DateField | |
| paid | BooleanField | |
| notes | TextField | Optional |

Database indexing is implemented for optimized querying by user and date.

---

## Installation & Setup

```bash
# Clone the repository
git clone https://github.com/butlerboy94/django-budget-tracker.git
cd django-budget-tracker

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install django

# Run migrations
python manage.py migrate

# (Optional) Create a superuser
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

Open your browser at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Running Tests

```bash
python manage.py test
```

Tests cover:
- Transaction CRUD (create, read, update, delete)
- Bill CRUD
- User access control (users cannot access other users' data)

---

## Future Enhancements

- [x] Financial data visualization (charts)
- [x] Category management system
- [x] UI/UX improvements

---

## Author

**Kaleb Butler**
Associate of Applied Science – Computer Programming
Rose State College

- 🌐 GitHub: [github.com/butlerboy94](https://github.com/butlerboy94)
- 📧 Email: [butlerkaleb0@gmail.com](mailto:butlerkaleb0@gmail.com)
- 💼 LinkedIn: [linkedin.com/in/kaleb-butler](https://www.linkedin.com/in/kaleb-butler)
