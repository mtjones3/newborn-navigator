# Newborn Navigator

A weekly newsletter platform for new parents, delivering evidence-based developmental milestones, tips, and local NYC resources for baby's first 12 weeks.

## Tech Stack

- **Backend:** Python 3.11+ / FastAPI / SQLAlchemy / SQLite
- **Frontend:** HTMX / Jinja2 / Tailwind CSS (CDN)
- **Email:** Stubbed sender (Resend-compatible interface, logs to `email_logs/`)
- **Auth:** JWT (cookie-based) for admin; token-based for subscribers

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/mtjones3/newborn-navigator.git
cd newborn-navigator
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

- **Windows (cmd):** `venv\Scripts\activate`
- **Windows (PowerShell):** `venv\Scripts\Activate.ps1`
- **macOS/Linux:** `source venv/bin/activate`

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example and edit as needed:

```bash
cp .env.example .env
```

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Secret key for JWT signing and sessions | `change-me-to-a-random-secret-key-in-production` |
| `ADMIN_USERNAME` | Admin login username | `admin` |
| `ADMIN_PASSWORD_HASH` | bcrypt hash for admin password | hash of `admin123` |
| `DATABASE_URL` | SQLAlchemy database URL | `sqlite:///newborn_navigator.db` |
| `RESEND_API_KEY` | Resend API key for real email sending | placeholder |
| `FROM_EMAIL` | Sender address for newsletters | `hello@newborn-navigator.com` |

### 5. Seed the database

The database and tables are created automatically on first run. Seed the milestone and local resource data:

```bash
python -m app.seed.seed_milestones
python -m app.seed.seed_local_resources
```

### 6. Start the server

```bash
uvicorn app.main:app --reload --port 8000
```

Visit **http://localhost:8000** in your browser.

## Default Admin Credentials

- **Username:** `admin`
- **Password:** `admin123`

Change these in your `.env` file for production.

## Features

### Subscriber Dashboard

- Personalized milestone tracker based on baby's birth date
- Weekly newsletter content delivery
- Browse all weeks (0–12) with categorized milestones
- **Local Resources** — find hospitals, pediatricians, and daycares across 12 Manhattan neighborhoods with HTMX-powered filtering by neighborhood and category

### Admin Panel (`/auth/login`)

- **Dashboard** — Stats overview (subscribers, newsletters, drafts, sent)
- **Newsletters** — Full CRUD with content sections (greeting, milestones, tips, Q&A, custom)
- **Email Preview** — Render newsletter as styled HTML in-browser
- **Send Test** — Test emails logged to `email_logs/` in stub mode
- **Subscribers** — View and search subscriber list
- **Milestones** — Browse all seeded milestones by week and category

### Milestone Categories

Motor, Sensory, Communication, Feeding, Sleep, Social & Emotional, Cognitive

### Email System

Emails are currently stubbed — sending writes HTML + metadata JSON to `email_logs/`. To switch to real sending via Resend, set your `RESEND_API_KEY` in `.env`.

## Project Structure

```
newborn-navigator/
├── app/
│   ├── main.py                  # FastAPI app, middleware, exception handlers
│   ├── config.py                # Settings from .env
│   ├── database.py              # SQLAlchemy engine + session
│   ├── models/
│   │   ├── subscriber.py        # Subscriber model (with neighborhood pref)
│   │   ├── newsletter.py        # NewsletterIssue + ContentSection
│   │   ├── milestone.py         # Milestone model
│   │   └── local_resource.py    # LocalResource model (hospitals, pediatricians, daycares)
│   ├── routes/
│   │   ├── auth.py              # Admin login/logout
│   │   ├── admin.py             # Admin dashboard, newsletters, subscribers, milestones
│   │   └── public.py            # Landing, subscribe, dashboard, local resources
│   ├── services/
│   │   ├── auth.py              # JWT + bcrypt helpers
│   │   └── email.py             # Stubbed email sender
│   ├── seed/
│   │   ├── seed_milestones.py   # ~1,200 milestones across weeks 0-12
│   │   └── seed_local_resources.py  # 32 NYC resources across 12 neighborhoods
│   ├── static/
│   │   └── js/htmx.min.js
│   └── templates/
│       ├── base.html
│       ├── error.html
│       ├── auth/                # Admin login
│       ├── admin/               # Dashboard, newsletters, subscribers, milestones
│       ├── email/               # HTML email template
│       └── public/              # Landing, login, dashboard, local resources
│           └── partials/        # HTMX partials (resource cards)
├── email_logs/                  # Stubbed email output (git-ignored)
├── requirements.txt
├── .env.example
└── .gitignore
```

## License

MIT
