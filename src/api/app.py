"""FastAPI application factory."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger
from pathlib import Path

from src.config import settings
from src.api.routes import router, set_predictor
from src.models.predict import ModelPredictor


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting up application...")
    try:
        model_path = settings.models_dir / f"{settings.model_name}.joblib"
        if model_path.exists():
            predictor = ModelPredictor(model_path, threshold=settings.default_threshold)
            set_predictor(predictor)
            logger.info("Model loaded successfully")
        else:
            logger.warning(f"Model not found at {model_path}")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    
    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        description="Production ML API for predicting SLA breaches",
        lifespan=lifespan
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routes
    app.include_router(router)
    
    return app
