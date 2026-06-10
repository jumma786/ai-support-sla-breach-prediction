# AI Support Operations SLA Breach Prediction

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-MachineLearning-orange)
![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-green)
![Status](https://img.shields.io/badge/Status-Completed-success)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Overview

This project develops an end-to-end machine learning solution for predicting Service Level Agreement (SLA) breaches in customer support operations.

The objective is to identify high-risk support tickets at the point of submission, enabling proactive intervention, improved prioritisation, and more efficient allocation of support resources.

The project follows a complete machine learning workflow including:

- Data quality assessment
- Exploratory data analysis
- Feature engineering
- Model development
- Hyperparameter tuning
- Cross-validation
- Threshold optimisation
- Risk assessment
- Governance documentation
- Develop a rule-based AI triage explanation layer
- Production deployment as a FastAPI REST service with automated tests and CI

---

## Quick Start

```bash
# Clone and set up
git clone https://github.com/jumma786/ai-support-sla-breach-prediction.git
cd ai-support-sla-breach-prediction
pip install -r requirements.txt

# Train the model (saves models/sla_breach_pipeline.joblib)
python scripts/train_model.py

# Start the API
uvicorn src.api.app:create_app --factory --host 0.0.0.0 --port 8000

# Verify
curl http://localhost:8000/health
# Interactive docs: http://localhost:8000/docs

# Run tests
pytest tests/ -v
```

### Example Prediction

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "customer_segment": "Enterprise",
    "priority_initial": "Critical",
    "issue_category": "service_outage",
    "agent_queue_length_at_submit": 50,
    "backlog_age_hours": 18.0,
    "negative_sentiment_flag": 1,
    "message_has_deadline": 1
  }'
```

Response:

```json
{
  "prediction": 1,
  "probability": 0.9988,
  "confidence": 0.9988,
  "threshold": 0.5,
  "recommendation": "Escalate immediately",
  "risk_factors": ["Critical priority", "High queue length", "High backlog age", "Negative sentiment", "Urgent deadline"]
}
```

---

## Business Problem

Customer support teams operate under Service Level Agreements (SLAs) that define expected response and resolution targets.

Failure to meet these targets can result in:

- Customer dissatisfaction
- Reduced service quality
- Contractual penalties
- Increased operational costs

The goal of this project is to predict whether a newly created support ticket is likely to breach its SLA before resolution activities begin.

---

## Project Objectives

- Identify the key drivers of SLA breaches
- Develop a leakage-safe prediction pipeline
- Compare multiple machine learning algorithms
- Optimise model performance using cross-validation
- Evaluate business trade-offs through threshold analysis
- Create governance, risk and monitoring documentation
- Develop a rule-based AI triage explanation layer


---

## Project Results Snapshot

| Metric | Value |
|----------|---------|
| Dataset Size | 15,000 Records |
| Features | 30 |
| Target Variable | sla_breached |
| Breach Rate | 60.9% |
| Best Model | Gradient Boosting |
| Precision | 89.2% |
| Recall | 91.3% |
| F1 Score | 90.3% |
| ROC-AUC | 96.1% |
| Threshold | 0.50 |
| Recommendation | Further Validation Using Real Operational Data |

---

## Dataset

| Item | Value |
|--------|--------|
| Records | 15,000 |
| Features | 30 |
| Target | sla_breached |
| Dataset Type | Synthetic Training Dataset |

The dataset contains:

- Customer information
- Ticket metadata
- Support channel information
- Workload indicators
- Agent characteristics
- Sentiment-related features
- Historical ticket activity

---

## Data Quality & Cleaning

### Issues Identified

- Missing values
- Duplicate records
- Inconsistent category labels
- Invalid queue values
- Potential leakage variables

### Cleaning Actions

- Removed 90 duplicate records
- Standardised categorical values
- Imputed missing values
- Corrected invalid queue observations
- Converted timestamp fields
- Removed leakage features

### Final Dataset

```text
15,000 cleaned records
```

---

## Exploratory Data Analysis

### High-Risk Customer Segments

- Enterprise customers showed the highest SLA breach rates.
- Public Sector customers demonstrated elevated operational risk.

### High-Risk Issue Categories

- Service Outages
- Integration Failures

### Key Operational Drivers

- Queue length
- Backlog age
- First response time
- Ticket priority

These variables exhibited strong relationships with SLA outcomes.

---

## Feature Engineering

### Temporal Features

- submitted_hour
- submitted_month
- submitted_dayofweek_num
- is_weekend

### Operational Features

- queue_pressure
- high_backlog_flag

### Sentiment Features

- negative_sentiment_flag

### Text-Derived Features

- message_word_count
- message_has_deadline

### Numerical Transformations

- contract_value_log1p

---

## Machine Learning Models Evaluated

| Model | F1 Score |
|---------|---------|
| Dummy Classifier | 0.757 |
| Logistic Regression | 0.898 |
| Decision Tree | 0.892 |
| Random Forest | 0.898 |
| Gradient Boosting | **0.903** |
| KNN | 0.842 |

---

## Best Model Performance

### Gradient Boosting (Best Performing Model)

| Metric | Score |
|----------|---------|
| Precision | 0.892 |
| Recall | 0.913 |
| F1 Score | 0.903 |
| ROC-AUC | 0.961 |

### Confusion Matrix

| | Predicted No | Predicted Yes |
|---|---|---|
| Actual No | 972 | 202 |
| Actual Yes | 158 | 1668 |

---

## AI Triage Assistant

As an optional extension, a rule-based AI Triage Assistant was developed to improve model transparency and support operational decision-making.

The assistant:

* Loads the trained SLA breach prediction model
* Generates breach probabilities for incoming tickets
* Identifies key risk factors using business rules
* Produces human-readable explanations
* Recommends operational actions based on risk level

### Example Output

```text
Prediction Probability: 100.0%

Main Risk Factors:
- Critical priority ticket
- Service outage issue
- Enterprise customer
- High agent queue length
- High backlog age
- Negative customer sentiment
- Urgent language detected

Recommended Action:
Escalate immediately and assign to a senior support agent.
```

### Business Value

The AI Triage Assistant converts model predictions into actionable business insights by explaining why a ticket is considered high risk and suggesting appropriate operational actions.

The solution was implemented using a rule-based explanation engine without external APIs, demonstrating explainable AI principles and human-in-the-loop decision support.

---

## Cross-Validation Results

5-Fold Stratified Cross Validation

| Metric | Mean Score |
|----------|---------|
| Precision | 0.892 |
| Recall | 0.904 |
| F1 Score | 0.898 |
| ROC-AUC | 0.959 |

The low variance across folds indicates stable model performance.

---

## Threshold Analysis

Selected Threshold:

```text
0.50
```

This threshold provided the strongest balance between:

- Detecting SLA breaches
- Minimising false positives
- Operational efficiency

---

## Risk & Governance

### Identified Risks

- Data Leakage
- Data Quality Issues
- Model Drift
- Operational Misuse
- Synthetic Dataset Limitations

### Mitigation Measures

- Leakage-safe feature selection
- Human review process
- Performance monitoring
- Risk register documentation
- Model card documentation

---

## Limitations

This project uses a synthetic dataset provided for educational purposes.

Although the model achieved strong predictive performance, results should not be interpreted as evidence of production readiness.

Validation using historical operational support-ticket data is required before deployment.

---

## Production Deployment (Implemented)

- FastAPI REST API (`/health`, `/predict`, `/predict-batch`) with Swagger docs at `/docs`
- Reproducible model training via `scripts/train_model.py`
- Automated test suite (pytest, 12 tests) covering data, models, and API
- CI pipeline with GitHub Actions
- Drift detection utilities (PSI, KS-test) in `src/monitoring/`

## Future Enhancements

- Real-world data validation
- Docker containerisation
- MLflow experiment tracking
- Real-time monitoring dashboards

---

## Repository Structure

```text
ai-support-sla-breach-prediction/
│
├── 01_Data/
│   ├── raw data/
│   └── processed data/
│
├── 02_Notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_exploratory_data_analysis.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_model_training.ipynb
│   ├── 05_model_evaluation.ipynb
│   └── 06_final_report.ipynb
│
├── 03_Reports_and_Templates/
│   ├── Executive Summary.docx
│   ├── AI Engineer Final Project Report.docx
│   ├── SLA Breach Prediction Model.docx
│   └── Professional_Risk_Assumptions_Register.xlsx
│
├── src/
│   ├── config.py              # Centralised settings
│   ├── api/                   # FastAPI app, routes, schemas
│   ├── data/                  # Loading, validation, preprocessing
│   ├── features/              # Feature engineering
│   ├── models/                # Train, predict, evaluate
│   └── monitoring/            # Drift detection, metrics
│
├── scripts/
│   └── train_model.py         # Trains and saves the pipeline
│
├── tests/                     # pytest suite (data, models, API)
│
├── models/                    # sla_breach_pipeline.joblib (generated, gitignored)
│
├── .github/workflows/         # CI pipeline
│
├── 07_triage_explanation_layer.py
├── main.py                    # API entry point
├── requirements.txt
├── pyproject.toml
├── .gitignore
└── LICENSE
```

---

## Author

**Jumma Mohammad**

GitHub: https://github.com/jumma786

LinkedIn: https://www.linkedin.com/in/jumma-mohammad/

Email: jummamohammad477@gmail.com