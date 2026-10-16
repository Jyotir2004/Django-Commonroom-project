# Commonroom

Commonroom is a Django workspace dashboard for viewing a team directory, managing workspace invitations, and tracking member availability and cars.

## Features

- Register and sign in with a username or email address.
- View the workspace directory and member availability.
- Add and remove workspace invitations.
- Add cars to your account and toggle their active status.
- View the dashboard overview and manage accounts through Django's admin.

The directory includes example people for display, along with registered users and invitations associated with the signed-in account.

## Requirements

- Python
- Django 6.1.2

## Setup

In PowerShell, from the repository root:

```powershell
cd core
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install Django==6.1.2
python manage.py migrate
```

Optionally create an administrator account for the Django admin:

```powershell
python manage.py createsuperuser
```

## Run the development server

From the `core` directory with the virtual environment activated:

```powershell
python manage.py runserver
```

Open <http://127.0.0.1:8000/>. Register an account at `/accounts/register/`, then sign in at `/accounts/login/`.

## Main routes

| Path | Purpose |
| --- | --- |
| `/` | Workspace dashboard |
| `/overview/` | Dashboard overview |
| `/invite/` | Add a workspace invitation |
| `/accounts/register/` | Create an account |
| `/accounts/login/` | Sign in |
| `/admin/` | Django administration |

## Tests

Run the Django test suite from the `core` directory:

```powershell
python manage.py test
```

## Project layout

```text
core/
├── accounts/   # Registration and authentication
├── core/       # Django settings and URL configuration
├── home/       # Dashboard, directory, invitations, and car features
└── manage.py
```

The project uses a local SQLite database at `core/db.sqlite3`. The current Django settings are intended for local development; configure a production secret key, allowed hosts, database, and security settings before deploying.
