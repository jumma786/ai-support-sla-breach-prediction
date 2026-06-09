"""
07_triage_explanation_layer.py

Rule-Based AI Triage Explanation Layer
AI Support Operations SLA Breach Prediction

Author: Jumma Mohammad
"""

import pandas as pd
import joblib
from pathlib import Path


# ==========================
# Load Model
# ==========================

MODEL_PATH = Path("models/final_sla_breach_pipeline.joblib")

model = joblib.load(MODEL_PATH)


# ==========================
# Recommendation Engine
# ==========================

def recommend_action(probability):

    if probability >= 0.80:
        return "Escalate immediately and assign to a senior support agent."

    elif probability >= 0.60:
        return "Prioritise ticket and monitor closely."

    else:
        return "Proceed with standard support workflow."


# ==========================
# Explanation Engine
# ==========================

def generate_triage_explanation(ticket, probability):

    reasons = []

    # Priority
    if ticket.get("priority_initial") == "Critical":
        reasons.append("Critical priority ticket")

    # Issue Category
    if ticket.get("issue_category") == "service_outage":
        reasons.append("Service outage issue")

    if ticket.get("issue_category") == "integration_failure":
        reasons.append("Integration failure issue")

    # Customer Segment
    if ticket.get("customer_segment") == "Enterprise":
        reasons.append("Enterprise customer")

    # Workload Indicators
    if ticket.get("agent_queue_length_at_submit", 0) > 45:
        reasons.append("High agent queue length")

    if ticket.get("backlog_age_hours", 0) > 12:
        reasons.append("High backlog age")

    # Sentiment
    if ticket.get("negative_sentiment_flag", 0) == 1:
        reasons.append("Negative customer sentiment")

    # Urgency
    if ticket.get("message_has_deadline", 0) == 1:
        reasons.append("Urgent language detected")

    if len(reasons) == 0:
        reasons.append("No major risk factors detected")

    explanation = (
        f"Predicted SLA breach probability: {probability:.1%}\n\n"
        f"Main risk factors:\n"
        + "\n".join([f"- {r}" for r in reasons])
    )

    return explanation


# ==========================
# Predict Ticket
# ==========================

def predict_ticket(ticket_df):

    probability = model.predict_proba(ticket_df)[0, 1]

    explanation = generate_triage_explanation(
        ticket_df.iloc[0].to_dict(),
        probability
    )

    recommendation = recommend_action(probability)

    print("=" * 60)
    print("AI TRIAGE ASSISTANT")
    print("=" * 60)

    print("\nPrediction Probability:")
    print(f"{probability:.1%}")

    print("\nExplanation:")
    print(explanation)

    print("\nRecommended Action:")
    print(recommendation)

    print("=" * 60)


# ==========================
# Example Usage
# ==========================

if __name__ == "__main__":

    sample_ticket = pd.DataFrame([{
        "customer_segment": "Enterprise",
        "uk_region": "London",
        "support_channel": "email",
        "product_area": "Billing",
        "issue_category": "service_outage",
        "priority_initial": "Critical",
        "day_of_week": "Monday",
        "hour_of_day": 10,
        "customer_tenure_months": 24,
        "contract_value_gbp": 50000,
        "previous_tickets_90d": 5,
        "avg_sentiment_score": -0.7,
        "message_length": 120,
        "contains_urgent_keyword": 1,
        "contains_refund_keyword": 0,
        "agent_queue_length_at_submit": 55,
        "assigned_agent": "Amelia",
        "agent_experience_months": 12,
        "backlog_age_hours": 18,
        "first_response_minutes": 150,
        "reopened_last_90d": 1,
        "submitted_hour": 10,
        "submitted_dayofweek_num": 0,
        "submitted_month": 6,
        "is_weekend": 0,
        "contract_value_log1p": 10.82,
        "queue_pressure": 4.23,
        "negative_sentiment_flag": 1,
        "high_backlog_flag": 1,
        "message_word_count": 25,
        "message_has_deadline": 1
    }])

    predict_ticket(sample_ticket)