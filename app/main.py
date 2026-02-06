from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.database import Base, engine
from app.routes import auth, admin, public

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="NewbornAI Navigator")
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

# Middleware
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# Include routers
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(public.router)

# Static files — mounted after routers so it doesn't shadow routes
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent / "static"),
    name="static",
)


# ── Exception handlers ───────────────────────────────────────────────────────


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # Handle auth redirects
    if exc.status_code == 303 and exc.headers and "Location" in exc.headers:
        return RedirectResponse(url=exc.headers["Location"], status_code=303)

    if exc.status_code == 404:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "status_code": 404, "detail": "Page not found"},
            status_code=404,
        )

    return templates.TemplateResponse(
        "error.html",
        {"request": request, "status_code": exc.status_code, "detail": exc.detail},
        status_code=exc.status_code,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return templates.TemplateResponse(
        "error.html",
        {"request": request, "status_code": 422, "detail": "Invalid input"},
        status_code=422,
    )
