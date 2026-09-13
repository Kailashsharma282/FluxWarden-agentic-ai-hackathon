import logging
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.api.incidents import router as incidents_router
from app.api.system import router as system_router
from app.api.scenarios import router as scenarios_router
from app.api.chat import router as chat_router
from app.api.demo import router as demo_router
from app.api.ws import router as ws_router

from contextlib import asynccontextmanager
from app.database.connection import init_db
from app.database.seed import seed_database

# Setup structured logger (Section 45)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("fluxwarden")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing FluxWarden persistence layer...")
    await init_db()
    try:
        await seed_database()
    except Exception as e:
        logger.debug(f"Initial seed notice: {e}")
    yield
    logger.info("FluxWarden backend shutting down.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=(
        f"{settings.TAGLINE}\n\n"
        f"**Participant**: {settings.PARTICIPANT_NAME} (Solo Participant)\n"
        f"**Team**: {settings.TEAM_NAME}\n"
        f"**Hackathon**: {settings.HACKATHON_NAME}"
    ),
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Observability middleware (structured logging, no secrets logged)
@app.middleware("http")
async def observability_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = int((time.time() - start_time) * 1000)
    # Exclude websocket pings from flood
    if not request.url.path.startswith("/ws"):
        logger.info(f"{request.method} {request.url.path} -> {response.status_code} ({process_time}ms)")
    return response

# Include all API Routers
app.include_router(incidents_router)
app.include_router(system_router)
app.include_router(scenarios_router)
app.include_router(chat_router)
app.include_router(demo_router)
app.include_router(ws_router)

@app.get("/")
async def root():
    return {
        "name": settings.PROJECT_NAME,
        "tagline": settings.TAGLINE,
        "status": "OPERATIONAL",
        "participant": settings.PARTICIPANT_NAME,
        "team": settings.TEAM_NAME,
        "hackathon": settings.HACKATHON_NAME,
        "docs_url": "/docs",
        "mode": settings.LLM_PROVIDER
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": time.time()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
