from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.backend.tasks.update_guru_stats import update_guru_stats


from app.backend.routes import api_router
from app.backend.database.connection import engine
from app.backend.database.connection import engine, SessionLocal


from app.backend.database.models import Base
from app.backend.scheduler import start as start_scheduler
from app.backend.database.init_sample_data import load_sample_data

from app.backend.services.ollama_service import ollama_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Hedge Fund API", description="Backend API for AI Hedge Fund", version="0.1.0")

# Initialize database tables (this is safe to run multiple times)
Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
    load_sample_data(db)

scheduler = AsyncIOScheduler(timezone="UTC")
scheduler.add_job(update_guru_stats, CronTrigger(hour=2, minute=0), id="update_guru_stats")


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routes
app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    """Startup event to check Ollama availability."""
    try:
        logger.info("Checking Ollama availability...")
        status = await ollama_service.check_ollama_status()
        
        if status["installed"]:
            if status["running"]:
                logger.info(f"✓ Ollama is installed and running at {status['server_url']}")
                if status["available_models"]:
                    logger.info(f"✓ Available models: {', '.join(status['available_models'])}")
                else:
                    logger.info("ℹ No models are currently downloaded")
            else:
                logger.info("ℹ Ollama is installed but not running")
                logger.info("ℹ You can start it from the Settings page or manually with 'ollama serve'")
        else:
            logger.info("ℹ Ollama is not installed. Install it to use local models.")
            logger.info("ℹ Visit https://ollama.com to download and install Ollama")
            
    except Exception as e:
        logger.warning(f"Could not check Ollama status: {e}")
        logger.info("ℹ Ollama integration is available if you install it later")


    if not scheduler.running:
        scheduler.start()