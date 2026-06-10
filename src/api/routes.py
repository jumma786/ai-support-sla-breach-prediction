"""API route handlers."""

from fastapi import APIRouter, HTTPException
import pandas as pd
from loguru import logger

from src.api.schemas import (
    TicketPredictionRequest, PredictionResponse, 
    BatchPredictionRequest, BatchPredictionResponse, HealthResponse
)
from src.config import settings
from src.models.predict import ModelPredictor

router = APIRouter()

# Initialize predictor
predictor = None


def set_predictor(pred: ModelPredictor):
    """Set the predictor instance."""
    global predictor
    predictor = pred


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=settings.api_version,
        model_loaded=predictor is not None
    )


@router.post("/predict", response_model=PredictionResponse)
async def predict_ticket(request: TicketPredictionRequest):
    """Predict SLA breach for a single ticket."""
    
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Convert request to DataFrame
        X = pd.DataFrame([request.dict()])
        
        # Make prediction
        prediction, probability = predictor.predict(X)
        
        # Generate recommendation
        if probability[0] >= 0.80:
            recommendation = "Escalate immediately"
        elif probability[0] >= 0.60:
            recommendation = "Prioritize and monitor"
        else:
            recommendation = "Standard workflow"
        
        # Identify risk factors
        risk_factors = []
        if request.priority_initial == "Critical":
            risk_factors.append("Critical priority")
        if request.agent_queue_length_at_submit > 45:
            risk_factors.append("High queue length")
        if request.backlog_age_hours > 12:
            risk_factors.append("High backlog age")
        if request.negative_sentiment_flag == 1:
            risk_factors.append("Negative sentiment")
        if request.message_has_deadline == 1:
            risk_factors.append("Urgent deadline")
        
        return PredictionResponse(
            prediction=int(prediction[0]),
            probability=float(probability[0]),
            confidence=max(probability[0], 1 - probability[0]),
            threshold=predictor.threshold,
            recommendation=recommendation,
            risk_factors=risk_factors if risk_factors else ["No major risk factors"]
        )
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/predict-batch", response_model=BatchPredictionResponse)
async def predict_batch(request: BatchPredictionRequest):
    """Predict SLA breach for multiple tickets."""
    
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        X = pd.DataFrame([record.dict() for record in request.records])
        predictions, probabilities = predictor.predict(X)
        
        results = []
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            results.append({
                "record_id": i,
                "prediction": int(pred),
                "probability": float(prob)
            })
        
        return BatchPredictionResponse(
            total_records=len(request.records),
            predictions=results
        )
    
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
