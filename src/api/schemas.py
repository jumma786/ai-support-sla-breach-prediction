"""Pydantic schemas for API requests/responses."""

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Dict, Any


class TicketPredictionRequest(BaseModel):
    """Request schema for single ticket prediction."""
    
    customer_segment: str = Field(..., description="Customer segment")
    priority_initial: str = Field(..., description="Initial ticket priority")
    issue_category: str = Field(..., description="Issue category")
    agent_queue_length_at_submit: int = Field(..., description="Agent queue length")
    backlog_age_hours: float = Field(..., description="Backlog age in hours")
    negative_sentiment_flag: int = Field(..., description="Negative sentiment indicator")
    message_has_deadline: int = Field(..., description="Has deadline indicator")
    
    class Config:
        json_schema_extra = {
            "example": {
                "customer_segment": "Enterprise",
                "priority_initial": "Critical",
                "issue_category": "service_outage",
                "agent_queue_length_at_submit": 50,
                "backlog_age_hours": 18.0,
                "negative_sentiment_flag": 1,
                "message_has_deadline": 1
            }
        }


class PredictionResponse(BaseModel):
    """Response schema for prediction."""
    
    prediction: int = Field(..., description="Binary prediction (0 or 1)")
    probability: float = Field(..., description="Probability of SLA breach")
    confidence: float = Field(..., description="Model confidence")
    threshold: float = Field(..., description="Classification threshold used")
    recommendation: str = Field(..., description="Recommended action")
    risk_factors: List[str] = Field(..., description="Key risk factors")


class HealthResponse(BaseModel):
    """Response schema for health check."""

    model_config = ConfigDict(protected_namespaces=())

    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    model_loaded: bool = Field(..., description="Model availability")


class BatchPredictionRequest(BaseModel):
    """Request schema for batch predictions."""
    
    records: List[Dict[str, Any]] = Field(..., description="Records to predict")


class BatchPredictionResponse(BaseModel):
    """Response schema for batch predictions."""
    
    total_records: int = Field(..., description="Total records processed")
    predictions: List[Dict[str, Any]] = Field(..., description="Predictions")
