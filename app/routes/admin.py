from pathlib import Path

from fastapi import APIRouter, Depends, Form, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Subscriber, NewsletterIssue, ContentSection, Milestone
from app.services.auth import get_current_admin
from app.services.email import send_email

router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")

SECTION_TYPES = ["greeting", "milestones", "noteworthy", "tips", "qa", "custom"]


# ── Dashboard ────────────────────────────────────────────────────────────────


@router.get("", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    admin: str = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    total_subscribers = db.query(Subscriber).filter(Subscriber.is_active == True).count()
    total_newsletters = db.query(NewsletterIssue).count()
    draft_count = (
        db.query(NewsletterIssue)
        .filter(NewsletterIssue.status == "draft")
        .count()
    )
    sent_count = (
        db.query(NewsletterIssue)
        .filter(NewsletterIssue.status == "sent")
        .count()
    )
    recent_subscribers = (
        db.query(Subscriber)
        .order_by(Subscriber.created_at.desc())
        .limit(5)
        .all()
    )
    return templates.TemplateResponse(
        "admin/dashboard.html",
        {
            "request": request,
            "admin": admin,
            "total_subscribers": total_subscribers,
            "total_newsletters": total_newsletters,
            "draft_count": draft_count,
            "sent_count": sent_count,
            "recent_subscribers": recent_subscribers,
        },
    )


# ── Newsletters ──────────────────────────────────────────────────────────────


@router.get("/newsletters", response_class=HTMLResponse)
async def newsletter_list(
    request: Request,
    admin: str = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    newsletters = (
        db.query(NewsletterIssue)
        .order_by(NewsletterIssue.week_number, NewsletterIssue.created_at.desc())
        .all()
    )
    return templates.TemplateResponse(
        "admin/newsletters.html",
        {"request": request, "admin": admin, "newsletters": newsletters},
    )


@router.get("/newsletters/create", response_class=HTMLResponse)
async def newsletter_create_form(
    request: Request, admin: str = Depends(get_current_admin)
):
    return templates.TemplateResponse(
        "admin/newsletter_form.html",
        {
            "request": request,
            "admin": admin,
            "newsletter": None,
            "section_types": SECTION_TYPES,
        },
    )


@router.post("/newsletters/create")
async def newsletter_create(
    request: Request,
    title: str = Form(...),
    subject_line: str = Form(...),
    week_number: int = Form(...),
    admin: str = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    newsletter = NewsletterIssue(
        title=title, subject_line=subject_line, week_number=week_number
    )
    db.add(newsletter)
    db.commit()
    db.refresh(newsletter)
    return RedirectResponse(
        url=f"/admin/newsletters/{newsletter.id}", status_code=303
    )


@router.get("/newsletters/{newsletter_id}", response_class=HTMLResponse)
async def newsletter_detail(
    request: Request,
    newsletter_id: int,
    admin: str = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    newsletter = db.query(NewsletterIssue).get(newsletter_id)
    if not newsletter:
        return RedirectResponse(url="/admin/newsletters", status_code=303)
    return templates.TemplateResponse(
        "admin/newsletter_detail.html",
        {
            "request": request,
            "admin": admin,
            "newsletter": newsletter,
            "section_types": SECTION_TYPES,
        },
    )


@router.post("/newsletters/{newsletter_id}/edit")
async def newsletter_edit(
    request: Request,
    newsletter_id: int,
    title: str = Form(...),
    subject_line: str = Form(...),
    week_number: int = Form(...),
    status: str = Form("draft"),
    admin: str = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    newsletter = db.query(NewsletterIssue).get(newsletter_id)
    if newsletter:
        newsletter.title = title
        newsletter.subject_line = subject_line
        newsletter.week_number = week_number
        newsletter.status = status
        db.commit()
    return RedirectResponse(
        url=f"/admin/newsletters/{newsletter_id}", status_code=303
    )


@router.post("/newsletters/{newsletter_id}/delete")
async def newsletter_delete(
    newsletter_id: int,
    admin: str = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    newsletter = db.query(NewsletterIssue).get(newsletter_id)
    if newsletter:
        db.delete(newsletter)
        db.commit()
    return RedirectResponse(url="/admin/newsletters", status_code=303)


# ── Sections ─────────────────────────────────────────────────────────────────


@router.post("/newsletters/{newsletter_id}/sections/add")
async def section_add(
    newsletter_id: int,
    section_type: str = Form(...),
    title: str = Form(""),
    body: str = Form(""),
    sort_order: int = Form(0),
    is_paid_only: bool = Form(False),
    admin: str = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    section = ContentSection(
        newsletter_id=newsletter_id,
        section_type=section_type,
        title=title,
        body=body,
        sort_order=sort_order,
        is_paid_only=is_paid_only,
    )
    db.add(section)
    db.commit()
    return RedirectResponse(
        url=f"/admin/newsletters/{newsletter_id}", status_code=303
    )


@router.post("/sections/{section_id}/edit")
async def section_edit(
    section_id: int,
    title: str = Form(""),
    body: str = Form(""),
    sort_order: int = Form(0),
    is_paid_only: bool = Form(False),
    admin: str = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    section = db.query(ContentSection).get(section_id)
    if section:
        section.title = title
        section.body = body
        section.sort_order = sort_order
        section.is_paid_only = is_paid_only
        db.commit()
        return RedirectResponse(
            url=f"/admin/newsletters/{section.newsletter_id}", status_code=303
        )
    return RedirectResponse(url="/admin/newsletters", status_code=303)


@router.post("/sections/{section_id}/delete")
async def section_delete(
    section_id: int,
    admin: str = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    section = db.query(ContentSection).get(section_id)
    if section:
        newsletter_id = section.newsletter_id
        db.delete(section)
        db.commit()
        return RedirectResponse(
            url=f"/admin/newsletters/{newsletter_id}", status_code=303
        )
    return RedirectResponse(url="/admin/newsletters", status_code=303)


# ── Preview + Send ───────────────────────────────────────────────────────────


@router.get("/preview/{newsletter_id}", response_class=HTMLResponse)
async def preview_email(
    request: Request,
    newsletter_id: int,
    admin: str = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    newsletter = db.query(NewsletterIssue).get(newsletter_id)
    if not newsletter:
        return RedirectResponse(url="/admin/newsletters", status_code=303)

    milestones = (
        db.query(Milestone)
        .filter(Milestone.week_number == newsletter.week_number)
        .order_by(Milestone.category)
        .all()
    )

    return templates.TemplateResponse(
        "email/newsletter.html",
        {
            "request": request,
            "newsletter": newsletter,
            "milestones": milestones,
            "subscriber_name": "Preview Parent",
            "baby_name": "Baby",
            "baby_age_weeks": newsletter.week_number,
            "unsubscribe_url": "#",
            "is_preview": True,
        },
    )


@router.post("/preview/{newsletter_id}/send-test")
async def send_test_email(
    request: Request,
    newsletter_id: int,
    test_email: str = Form(...),
    admin: str = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    newsletter = db.query(NewsletterIssue).get(newsletter_id)
    if not newsletter:
        return RedirectResponse(url="/admin/newsletters", status_code=303)

    milestones = (
        db.query(Milestone)
        .filter(Milestone.week_number == newsletter.week_number)
        .order_by(Milestone.category)
        .all()
    )

    html_body = templates.TemplateResponse(
        "email/newsletter.html",
        {
            "request": request,
            "newsletter": newsletter,
            "milestones": milestones,
            "subscriber_name": "Test Parent",
            "baby_name": "Baby",
            "baby_age_weeks": newsletter.week_number,
            "unsubscribe_url": "#",
            "is_preview": False,
        },
    ).body.decode()

    result = send_email(to=test_email, subject=newsletter.subject_line, html_body=html_body)

    return templates.TemplateResponse(
        "admin/newsletter_detail.html",
        {
            "request": request,
            "admin": admin,
            "newsletter": newsletter,
            "section_types": SECTION_TYPES,
            "flash": f"Test email logged! File: {result.get('path', 'N/A')}",
        },
    )


# ── Subscribers ──────────────────────────────────────────────────────────────


@router.get("/subscribers", response_class=HTMLResponse)
async def subscriber_list(
    request: Request,
    q: str = Query(""),
    admin: str = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    query = db.query(Subscriber).order_by(Subscriber.created_at.desc())
    if q:
        query = query.filter(
            Subscriber.email.ilike(f"%{q}%")
            | Subscriber.name.ilike(f"%{q}%")
        )
    subscribers = query.all()
    return templates.TemplateResponse(
        "admin/subscribers.html",
        {"request": request, "admin": admin, "subscribers": subscribers, "q": q},
    )


# ── Milestones ───────────────────────────────────────────────────────────────


@router.get("/milestones", response_class=HTMLResponse)
async def milestone_browser(
    request: Request,
    week: int = Query(0),
    admin: str = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    milestones = (
        db.query(Milestone)
        .filter(Milestone.week_number == week)
        .order_by(Milestone.category, Milestone.id)
        .all()
    )
    categories = {}
    for m in milestones:
        categories.setdefault(m.category, []).append(m)

    return templates.TemplateResponse(
        "admin/milestones.html",
        {
            "request": request,
            "admin": admin,
            "milestones": milestones,
            "categories": categories,
            "week": week,
            "weeks": list(range(0, 13)),
        },
    )
