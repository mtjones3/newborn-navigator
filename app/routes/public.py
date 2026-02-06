import calendar
import json
import uuid
from datetime import date, datetime, time, timedelta
from pathlib import Path

from fastapi import APIRouter, Depends, Form, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Subscriber, Milestone, NewsletterIssue, LocalResource, MilestoneTracking, CalendarEvent
from app.services.ai_chat import build_system_prompt, stream_chat_response, generate_milestone_response

router = APIRouter(tags=["public"])
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")


def _baby_age_weeks(birth_date: date | None) -> int | None:
    if not birth_date:
        return None
    delta = date.today() - birth_date
    return max(0, delta.days // 7)


@router.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    return templates.TemplateResponse("public/landing.html", {"request": request})


# ── Subscriber login ─────────────────────────────────────────────────────────


@router.get("/login", response_class=HTMLResponse)
async def subscriber_login_page(request: Request):
    return templates.TemplateResponse("public/login.html", {"request": request})


@router.post("/login")
async def subscriber_login(
    request: Request,
    email: str = Form(...),
    db: Session = Depends(get_db),
):
    subscriber = (
        db.query(Subscriber)
        .filter(Subscriber.email == email, Subscriber.is_active == True)
        .first()
    )
    if not subscriber:
        return templates.TemplateResponse(
            "public/login.html",
            {"request": request, "error": "No active subscription found for that email."},
            status_code=404,
        )
    # Redirect to the correct week based on baby's age
    baby_age = _baby_age_weeks(subscriber.baby_birth_date)
    week = min(baby_age, 16) if baby_age is not None else 0
    return RedirectResponse(
        url=f"/my-updates/{subscriber.unsubscribe_token}?week={week}", status_code=303
    )


# ── Subscribe ────────────────────────────────────────────────────────────────


@router.post("/subscribe")
async def subscribe(
    request: Request,
    email: str = Form(...),
    name: str = Form(""),
    baby_name: str = Form(""),
    baby_birth_date: str = Form(""),
    baby_due_date: str = Form(""),
    db: Session = Depends(get_db),
):
    existing = db.query(Subscriber).filter(Subscriber.email == email).first()
    if existing:
        if not existing.is_active:
            existing.is_active = True
            db.commit()
        # Redirect to the correct week based on baby's age
        baby_age = _baby_age_weeks(existing.baby_birth_date)
        week = min(baby_age, 16) if baby_age is not None else 0
        return RedirectResponse(
            url=f"/my-updates/{existing.unsubscribe_token}?week={week}", status_code=303
        )

    subscriber = Subscriber(
        email=email,
        name=name or None,
        baby_name=baby_name or None,
        baby_birth_date=(
            datetime.strptime(baby_birth_date, "%Y-%m-%d").date()
            if baby_birth_date
            else None
        ),
        baby_due_date=(
            datetime.strptime(baby_due_date, "%Y-%m-%d").date()
            if baby_due_date
            else None
        ),
        unsubscribe_token=uuid.uuid4().hex,
    )
    db.add(subscriber)
    db.commit()
    db.refresh(subscriber)

    # Redirect to the correct week based on baby's age
    baby_age = _baby_age_weeks(subscriber.baby_birth_date)
    week = min(baby_age, 16) if baby_age is not None else 0
    return RedirectResponse(
        url=f"/my-updates/{subscriber.unsubscribe_token}?week={week}", status_code=303
    )


# ── Personalized updates page ────────────────────────────────────────────────


@router.get("/my-updates/{token}", response_class=HTMLResponse)
async def my_updates(
    request: Request,
    token: str,
    week: int | None = Query(None),
    db: Session = Depends(get_db),
):
    subscriber = (
        db.query(Subscriber).filter(Subscriber.unsubscribe_token == token).first()
    )
    if not subscriber:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "status_code": 404, "detail": "Page not found"},
            status_code=404,
        )

    baby_age = _baby_age_weeks(subscriber.baby_birth_date)

    # Use query param week if provided, otherwise calculate from birth date
    if week is not None:
        week = max(0, min(week, 16))
    else:
        week = min(baby_age, 16) if baby_age is not None else 0

    # Get milestones for this week
    milestones = (
        db.query(Milestone)
        .filter(Milestone.week_number == week)
        .order_by(Milestone.category, Milestone.id)
        .all()
    )
    categories = {}
    for m in milestones:
        label = (
            "Social & Emotional"
            if m.category == "social_emotional"
            else m.category.replace("_", " ").title()
        )
        categories.setdefault(label, []).append(m)

    # Get matching newsletter issue if one exists
    newsletter = (
        db.query(NewsletterIssue)
        .filter(NewsletterIssue.week_number == week)
        .order_by(NewsletterIssue.created_at.desc())
        .first()
    )

    # Build the list of all available weeks that have newsletters
    available_issues = (
        db.query(NewsletterIssue)
        .filter(NewsletterIssue.status.in_(["sent", "draft", "scheduled"]))
        .order_by(NewsletterIssue.week_number)
        .all()
    )

    # Get tracking data for this subscriber + this week's milestones
    milestone_ids = [m.id for m in milestones]
    tracking_rows = (
        db.query(MilestoneTracking)
        .filter(
            MilestoneTracking.subscriber_id == subscriber.id,
            MilestoneTracking.milestone_id.in_(milestone_ids),
        )
        .all()
    ) if milestone_ids else []
    tracking = {t.milestone_id: t for t in tracking_rows}

    # Progress counts for the progress bar
    total_count = len(milestones)
    achieved_count = sum(1 for t in tracking_rows if t.status == "achieved")
    concern_count = sum(1 for t in tracking_rows if t.status == "concern")
    untracked_count = total_count - achieved_count - concern_count

    return templates.TemplateResponse(
        "public/my_updates.html",
        {
            "request": request,
            "subscriber": subscriber,
            "baby_age": baby_age,
            "week": week,
            "milestones": milestones,
            "categories": categories,
            "newsletter": newsletter,
            "available_issues": available_issues,
            "token": token,
            "tracking": tracking,
            "total_count": total_count,
            "achieved_count": achieved_count,
            "concern_count": concern_count,
            "untracked_count": untracked_count,
            "baby_name": subscriber.baby_name,
        },
    )


# ── Milestone Tracking ───────────────────────────────────────────────────────


@router.post("/my-updates/{token}/track/{milestone_id}", response_class=HTMLResponse)
async def toggle_milestone(
    request: Request,
    token: str,
    milestone_id: int,
    db: Session = Depends(get_db),
):
    subscriber = _get_subscriber_or_404(token, db)
    if not subscriber:
        return HTMLResponse("Not found", status_code=404)

    milestone = db.query(Milestone).filter(Milestone.id == milestone_id).first()
    if not milestone:
        return HTMLResponse("Milestone not found", status_code=404)

    track = (
        db.query(MilestoneTracking)
        .filter(
            MilestoneTracking.subscriber_id == subscriber.id,
            MilestoneTracking.milestone_id == milestone_id,
        )
        .first()
    )

    if not track:
        track = MilestoneTracking(
            subscriber_id=subscriber.id,
            milestone_id=milestone_id,
            status="achieved",
            achieved_at=datetime.utcnow(),
        )
        db.add(track)
    elif track.status == "achieved":
        track.status = "concern"
        track.achieved_at = None
    elif track.status == "concern":
        track.status = None
        track.achieved_at = None
    else:
        track.status = "achieved"
        track.achieved_at = datetime.utcnow()

    db.commit()
    db.refresh(track)

    # Compute updated progress counts for this week
    week_milestones = (
        db.query(Milestone)
        .filter(Milestone.week_number == milestone.week_number)
        .all()
    )
    week_milestone_ids = [wm.id for wm in week_milestones]
    week_tracking = (
        db.query(MilestoneTracking)
        .filter(
            MilestoneTracking.subscriber_id == subscriber.id,
            MilestoneTracking.milestone_id.in_(week_milestone_ids),
        )
        .all()
    )
    total_count = len(week_milestones)
    achieved_count = sum(1 for t in week_tracking if t.status == "achieved")
    concern_count = sum(1 for t in week_tracking if t.status == "concern")
    untracked_count = total_count - achieved_count - concern_count

    tracking = {milestone.id: track}
    m = milestone

    # Render card with feedback + out-of-band progress bar update
    card_html = templates.TemplateResponse(
        "public/partials/milestone_card.html",
        {"request": request, "m": m, "token": token, "tracking": tracking, "show_feedback": True},
    ).body.decode()

    progress_html = templates.TemplateResponse(
        "public/partials/milestone_progress.html",
        {
            "request": request,
            "week": milestone.week_number,
            "total_count": total_count,
            "achieved_count": achieved_count,
            "concern_count": concern_count,
            "untracked_count": untracked_count,
            "baby_name": subscriber.baby_name if hasattr(subscriber, "baby_name") else None,
        },
    ).body.decode()

    # Use HTMX out-of-band swap to update progress bar alongside the card
    oob_progress = progress_html.replace(
        'id="milestone-progress"',
        'id="milestone-progress" hx-swap-oob="outerHTML"',
        1,
    )

    return HTMLResponse(card_html + oob_progress)


@router.post("/my-updates/{token}/track/{milestone_id}/notes", response_class=HTMLResponse)
async def save_milestone_notes(
    request: Request,
    token: str,
    milestone_id: int,
    notes: str = Form(""),
    db: Session = Depends(get_db),
):
    subscriber = _get_subscriber_or_404(token, db)
    if not subscriber:
        return HTMLResponse("Not found", status_code=404)

    milestone = db.query(Milestone).filter(Milestone.id == milestone_id).first()
    if not milestone:
        return HTMLResponse("Milestone not found", status_code=404)

    track = (
        db.query(MilestoneTracking)
        .filter(
            MilestoneTracking.subscriber_id == subscriber.id,
            MilestoneTracking.milestone_id == milestone_id,
        )
        .first()
    )

    if not track:
        track = MilestoneTracking(
            subscriber_id=subscriber.id,
            milestone_id=milestone_id,
            notes=notes.strip() or None,
        )
        db.add(track)
    else:
        track.notes = notes.strip() or None

    note_text = notes.strip()
    if not note_text:
        track.ai_response = None
        db.commit()
        return HTMLResponse(
            '<span class="text-gray-400 text-xs">Note cleared</span>'
        )

    # Generate AI response
    baby_age = _baby_age_weeks(subscriber.baby_birth_date)
    try:
        ai_response = await generate_milestone_response(
            baby_name=subscriber.baby_name,
            baby_age_weeks=baby_age,
            milestone_title=milestone.title,
            milestone_description=milestone.description,
            parent_note=note_text,
            status=track.status,
        )
        track.ai_response = ai_response
    except Exception as e:
        print(f"AI RESPONSE ERROR: {type(e).__name__}: {e}")
        ai_response = None
        track.ai_response = None

    db.commit()

    if ai_response:
        return HTMLResponse(f'''
            <div class="mt-2 bg-indigo-50 rounded-lg px-3 py-2 border-l-4 border-indigo-400">
                <p class="text-xs text-indigo-800">{ai_response}</p>
            </div>
        ''')
    else:
        return HTMLResponse(
            '<span class="text-green-600 text-xs font-medium">Saved!</span>'
        )


# ── AI Chat ──────────────────────────────────────────────────────────────────


@router.post("/my-updates/{token}/chat")
async def chat(token: str, request: Request, db: Session = Depends(get_db)):
    subscriber = (
        db.query(Subscriber).filter(Subscriber.unsubscribe_token == token).first()
    )
    if not subscriber:
        return StreamingResponse(
            iter([f'data: {json.dumps({"error": "Subscriber not found"})}\n\n']),
            media_type="text/event-stream",
        )

    body = await request.json()
    messages = body.get("messages", [])
    if not messages:
        return StreamingResponse(
            iter([f'data: {json.dumps({"error": "No messages provided"})}\n\n']),
            media_type="text/event-stream",
        )

    baby_age = _baby_age_weeks(subscriber.baby_birth_date)
    viewed_week = body.get("week")
    if viewed_week is not None:
        current_week = max(0, min(int(viewed_week), 16))
    else:
        current_week = min(baby_age, 16) if baby_age is not None else 0

    milestones = (
        db.query(Milestone)
        .filter(Milestone.week_number == current_week)
        .order_by(Milestone.category, Milestone.id)
        .all()
    )
    milestone_dicts = [
        {
            "category": m.category,
            "title": m.title,
            "description": m.description,
            "is_concern_flag": m.is_concern_flag,
            "parent_action": m.parent_action,
        }
        for m in milestones
    ]

    # Query ALL tracking data for this subscriber (not just current week)
    all_tracking = (
        db.query(MilestoneTracking, Milestone)
        .join(Milestone, MilestoneTracking.milestone_id == Milestone.id)
        .filter(MilestoneTracking.subscriber_id == subscriber.id)
        .order_by(Milestone.week_number, Milestone.category)
        .all()
    )
    tracking_history = [
        {
            "week": m.week_number,
            "category": m.category,
            "title": m.title,
            "status": t.status,
            "notes": t.notes,
            "achieved_at": t.achieved_at.isoformat() if t.achieved_at else None,
        }
        for t, m in all_tracking
        if t.status or t.notes
    ]

    system_prompt = build_system_prompt(
        baby_name=subscriber.baby_name,
        baby_age_weeks=baby_age,
        milestones=milestone_dicts,
        tracking_history=tracking_history,
    )

    async def event_generator():
        try:
            async for chunk in stream_chat_response(messages, system_prompt):
                yield f"data: {json.dumps({'text': chunk})}\n\n"
            yield f"data: {json.dumps({'done': True})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.get("/unsubscribe/{token}", response_class=HTMLResponse)
async def unsubscribe(request: Request, token: str, db: Session = Depends(get_db)):
    subscriber = (
        db.query(Subscriber).filter(Subscriber.unsubscribe_token == token).first()
    )
    if subscriber:
        subscriber.is_active = False
        db.commit()
        return templates.TemplateResponse(
            "public/unsubscribed.html",
            {"request": request, "found": True},
        )
    return templates.TemplateResponse(
        "public/unsubscribed.html",
        {"request": request, "found": False},
    )


# ── Local Resources ─────────────────────────────────────────────────────────

NEIGHBORHOODS = [
    "Upper West Side",
    "Upper East Side",
    "Midtown",
    "Chelsea",
    "Greenwich Village",
    "East Village",
    "Lower East Side",
    "Tribeca",
    "SoHo",
    "Harlem",
    "Washington Heights",
    "Financial District",
]


def _get_subscriber_or_404(token: str, db: Session):
    subscriber = (
        db.query(Subscriber).filter(Subscriber.unsubscribe_token == token).first()
    )
    return subscriber


@router.get("/my-updates/{token}/local-resources", response_class=HTMLResponse)
async def local_resources(
    request: Request,
    token: str,
    db: Session = Depends(get_db),
):
    subscriber = _get_subscriber_or_404(token, db)
    if not subscriber:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "status_code": 404, "detail": "Page not found"},
            status_code=404,
        )

    neighborhood = subscriber.neighborhood or ""
    query = db.query(LocalResource)
    if neighborhood:
        query = query.filter(LocalResource.neighborhood == neighborhood)
    resources = query.order_by(LocalResource.category, LocalResource.name).all()

    return templates.TemplateResponse(
        "public/local_resources.html",
        {
            "request": request,
            "subscriber": subscriber,
            "token": token,
            "neighborhoods": NEIGHBORHOODS,
            "selected_neighborhood": neighborhood,
            "selected_category": "all",
            "resources": resources,
        },
    )


@router.get("/my-updates/{token}/local-resources/filter", response_class=HTMLResponse)
async def local_resources_filter(
    request: Request,
    token: str,
    neighborhood: str = Query(""),
    category: str = Query("all"),
    db: Session = Depends(get_db),
):
    subscriber = _get_subscriber_or_404(token, db)
    if not subscriber:
        return HTMLResponse("Not found", status_code=404)

    query = db.query(LocalResource)
    if neighborhood:
        query = query.filter(LocalResource.neighborhood == neighborhood)
    if category and category != "all":
        query = query.filter(LocalResource.category == category)
    resources = query.order_by(LocalResource.category, LocalResource.name).all()

    return templates.TemplateResponse(
        "public/partials/resource_cards.html",
        {
            "request": request,
            "resources": resources,
        },
    )


@router.post("/my-updates/{token}/save-neighborhood")
async def save_neighborhood(
    request: Request,
    token: str,
    neighborhood: str = Form(""),
    db: Session = Depends(get_db),
):
    subscriber = _get_subscriber_or_404(token, db)
    if not subscriber:
        return HTMLResponse("Not found", status_code=404)

    subscriber.neighborhood = neighborhood or None
    db.commit()
    return HTMLResponse(
        '<span class="text-green-600 text-sm font-medium">Saved!</span>'
    )


# ── Family Calendar ──────────────────────────────────────────────────────────


def _get_calendar_days(year: int, month: int, events_by_date: dict) -> list:
    """Build calendar grid with events for display."""
    cal = calendar.Calendar(firstweekday=6)  # Sunday first
    today = date.today()
    days = []

    for d in cal.itermonthdates(year, month):
        day_events = events_by_date.get(d, [])
        days.append({
            "date": d.isoformat(),
            "day": d.day,
            "is_current_month": d.month == month,
            "is_today": d == today,
            "events": day_events,
        })

    return days


@router.get("/my-updates/{token}/calendar", response_class=HTMLResponse)
async def family_calendar(
    request: Request,
    token: str,
    year: int | None = Query(None),
    month: int | None = Query(None),
    db: Session = Depends(get_db),
):
    subscriber = _get_subscriber_or_404(token, db)
    if not subscriber:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "status_code": 404, "detail": "Page not found"},
            status_code=404,
        )

    today = date.today()
    current_year = year or today.year
    current_month = month or today.month

    # Get events for this month (and edges for calendar display)
    first_of_month = date(current_year, current_month, 1)
    if current_month == 12:
        last_of_month = date(current_year + 1, 1, 1) - timedelta(days=1)
    else:
        last_of_month = date(current_year, current_month + 1, 1) - timedelta(days=1)

    # Extend range to cover calendar grid
    start_date = first_of_month - timedelta(days=first_of_month.weekday() + 1)
    end_date = last_of_month + timedelta(days=7)

    events = (
        db.query(CalendarEvent)
        .filter(
            CalendarEvent.subscriber_id == subscriber.id,
            CalendarEvent.event_date >= start_date,
            CalendarEvent.event_date <= end_date,
        )
        .order_by(CalendarEvent.event_date, CalendarEvent.event_time)
        .all()
    )

    events_by_date = {}
    for event in events:
        events_by_date.setdefault(event.event_date, []).append(event)

    calendar_days = _get_calendar_days(current_year, current_month, events_by_date)

    # Upcoming events (next 30 days)
    upcoming_events = (
        db.query(CalendarEvent)
        .filter(
            CalendarEvent.subscriber_id == subscriber.id,
            CalendarEvent.event_date >= today,
            CalendarEvent.event_date <= today + timedelta(days=30),
        )
        .order_by(CalendarEvent.event_date, CalendarEvent.event_time)
        .limit(10)
        .all()
    )

    month_names = [
        "", "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    return templates.TemplateResponse(
        "public/calendar.html",
        {
            "request": request,
            "subscriber": subscriber,
            "token": token,
            "current_year": current_year,
            "current_month": current_month,
            "current_month_name": month_names[current_month],
            "calendar_days": calendar_days,
            "upcoming_events": upcoming_events,
        },
    )


@router.get("/my-updates/{token}/calendar/event/{event_id}")
async def get_calendar_event(
    token: str,
    event_id: int,
    db: Session = Depends(get_db),
):
    subscriber = _get_subscriber_or_404(token, db)
    if not subscriber:
        return JSONResponse({"error": "Not found"}, status_code=404)

    event = (
        db.query(CalendarEvent)
        .filter(CalendarEvent.id == event_id, CalendarEvent.subscriber_id == subscriber.id)
        .first()
    )
    if not event:
        return JSONResponse({"error": "Event not found"}, status_code=404)

    return JSONResponse({
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "event_date": event.event_date.isoformat(),
        "event_time": event.event_time.strftime("%H:%M") if event.event_time else None,
        "category": event.category,
    })


@router.post("/my-updates/{token}/calendar/add")
async def add_calendar_event(
    request: Request,
    token: str,
    title: str = Form(...),
    event_date: str = Form(...),
    event_time: str = Form(""),
    category: str = Form("other"),
    description: str = Form(""),
    db: Session = Depends(get_db),
):
    subscriber = _get_subscriber_or_404(token, db)
    if not subscriber:
        return HTMLResponse("Not found", status_code=404)

    parsed_date = datetime.strptime(event_date, "%Y-%m-%d").date()
    parsed_time = None
    if event_time:
        parsed_time = datetime.strptime(event_time, "%H:%M").time()

    event = CalendarEvent(
        subscriber_id=subscriber.id,
        title=title,
        description=description or None,
        event_date=parsed_date,
        event_time=parsed_time,
        category=category,
    )
    db.add(event)
    db.commit()

    return HTMLResponse("OK")


@router.post("/my-updates/{token}/calendar/edit/{event_id}")
async def edit_calendar_event(
    request: Request,
    token: str,
    event_id: int,
    title: str = Form(...),
    event_date: str = Form(...),
    event_time: str = Form(""),
    category: str = Form("other"),
    description: str = Form(""),
    db: Session = Depends(get_db),
):
    subscriber = _get_subscriber_or_404(token, db)
    if not subscriber:
        return HTMLResponse("Not found", status_code=404)

    event = (
        db.query(CalendarEvent)
        .filter(CalendarEvent.id == event_id, CalendarEvent.subscriber_id == subscriber.id)
        .first()
    )
    if not event:
        return HTMLResponse("Event not found", status_code=404)

    event.title = title
    event.event_date = datetime.strptime(event_date, "%Y-%m-%d").date()
    event.event_time = datetime.strptime(event_time, "%H:%M").time() if event_time else None
    event.category = category
    event.description = description or None
    db.commit()

    return HTMLResponse("OK")


@router.post("/my-updates/{token}/calendar/delete/{event_id}")
async def delete_calendar_event(
    token: str,
    event_id: int,
    db: Session = Depends(get_db),
):
    subscriber = _get_subscriber_or_404(token, db)
    if not subscriber:
        return HTMLResponse("Not found", status_code=404)

    event = (
        db.query(CalendarEvent)
        .filter(CalendarEvent.id == event_id, CalendarEvent.subscriber_id == subscriber.id)
        .first()
    )
    if event:
        db.delete(event)
        db.commit()

    return HTMLResponse("OK")
