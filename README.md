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



flowchart TD
    A([Start]) --> B[Open CommonRoom]
    B --> C{Logged in?}
    C -- No --> D[Register or Login]
    D --> E{Credentials valid?}
    E -- No --> D
    E -- Yes --> F[View Available Rooms]
    C -- Yes --> F
    F --> G{Choose an action}
    G --> H[Create a Room]
    G --> I[Join an Existing Room]
    H --> J[Open Room Chat]
    I --> J
    J --> K[Read and Send Messages]
    K --> L{Continue chatting?}
    L -- Yes --> K
    L -- No --> M[Leave Room]
    M --> F



sequenceDiagram
    actor User
    participant UI as Chat Page
    participant D as Django View
    participant DB as Database

    User->>UI: Type message and submit
    UI->>D: POST message + room ID
    D->>D: Check login and room access
    D->>DB: Save message
    DB-->>D: Message saved
    D-->>UI: Redirect or return response
    UI->>D: Request room messages
    D->>DB: Fetch messages for room
    DB-->>D: Return messages
    D-->>UI: Render chat history
    UI-->>User: Display message
