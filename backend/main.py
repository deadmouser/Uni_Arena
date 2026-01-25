from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from database import engine, Base
from routers import auth, admin, organizer, matches, coach, venues, tournaments, notifications, statistics, players, admin_tournaments, institutions

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Uni Arena - Sports Management System for Institutions"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(admin.router, prefix=settings.API_V1_PREFIX)
app.include_router(organizer.router, prefix=settings.API_V1_PREFIX)
app.include_router(matches.router, prefix=settings.API_V1_PREFIX)
app.include_router(coach.router, prefix=settings.API_V1_PREFIX)
app.include_router(venues.router, prefix=settings.API_V1_PREFIX)
app.include_router(tournaments.router, prefix=settings.API_V1_PREFIX)
app.include_router(notifications.router, prefix=settings.API_V1_PREFIX)
app.include_router(statistics.router, prefix=settings.API_V1_PREFIX)
app.include_router(players.router, prefix=settings.API_V1_PREFIX)
app.include_router(admin_tournaments.router, prefix=settings.API_V1_PREFIX)
app.include_router(institutions.router, prefix=settings.API_V1_PREFIX)

from fastapi.staticfiles import StaticFiles
import os

# Create static directory if it doesn't exist
if not os.path.exists("static/uploads"):
    os.makedirs("static/uploads")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Uni Arena API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
