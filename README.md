# Newborn Navigator

A weekly newsletter platform for new parents, delivering evidence-based milestones and tips for baby's first 12 weeks.

## Tech Stack

- **Backend:** FastAPI + SQLAlchemy + SQLite
- **Frontend:** HTMX + Jinja2 + Tailwind CSS (CDN)
- **Email:** Stubbed sender (Resend-compatible interface, logs to `email_logs/`)
- **Auth:** JWT (cookie-based) for admin

## Quick Start

```cmd
cd C:\Users\mtjon\Desktop\newborn-navigator

:: Create virtual environment and install dependencies
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

:: Seed milestone data
python -m app.seed.seed_milestones

:: Start the server
uvicorn app.main:app --reload --port 8000
```

Then visit:
- **Landing page:** http://localhost:8000
- **Admin login:** http://localhost:8000/auth/login

## Default Admin Credentials

- **Username:** `admin`
- **Password:** `admin123`

## Features

### Public
- Landing page with subscription signup form
- Baby birth date / due date personalization
- One-click unsubscribe via unique token

### Admin Dashboard
- **Dashboard** — Stats overview (subscribers, newsletters, drafts, sent)
- **Newsletters** — Create, edit, delete newsletters with content sections
- **Sections** — Add greeting, milestones, noteworthy, tips, Q&A, or custom sections
- **Email Preview** — Render newsletter as a styled HTML email in-browser
- **Send Test** — Send test emails (logged to `email_logs/` in stub mode)
- **Subscribers** — View and search subscriber list
- **Milestones** — Browse all 73 seeded milestones by week (0-12) and category

### Milestone Categories
Motor, Sensory, Communication, Feeding, Sleep, Social & Emotional, Cognitive

### Email System
Emails are currently stubbed — calling "send" writes the HTML + metadata JSON to `email_logs/`. To switch to real sending via Resend, update `app/services/email.py` with your API key.

## Project Structure

```
newborn-navigator/
├── app/
│   ├── main.py              # FastAPI app, middleware, exception handlers
│   ├── config.py             # Settings from .env
│   ├── database.py           # SQLAlchemy engine + session
│   ├── models/
│   │   ├── subscriber.py     # Subscriber model
│   │   ├── newsletter.py     # NewsletterIssue + ContentSection
│   │   └── milestone.py      # Milestone model
│   ├── routes/
│   │   ├── auth.py           # Login/logout
│   │   ├── admin.py          # Dashboard, newsletters, subscribers, milestones
│   │   └── public.py         # Landing page, subscribe, unsubscribe
│   ├── services/
│   │   ├── auth.py           # JWT + bcrypt
│   │   └── email.py          # Stubbed email sender
│   ├── seed/
│   │   └── seed_milestones.py # 73 milestones across weeks 0-12
│   ├── static/
│   │   └── js/htmx.min.js
│   └── templates/
│       ├── base.html
│       ├── error.html
│       ├── auth/login.html
│       ├── admin/            # Dashboard, newsletters, subscribers, milestones
│       ├── email/newsletter.html  # HTML email template
│       └── public/           # Landing, thank you, unsubscribed
├── email_logs/               # Stubbed email output
├── requirements.txt
├── .env
└── .gitignore
```
