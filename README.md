# AI Support Operations SLA Breach Prediction

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-MachineLearning-orange)
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

## Future Enhancements

- Real-world data validation
- FastAPI deployment
- Docker containerisation
- CI/CD automation
- MLflow experiment tracking
- Real-time monitoring dashboards

---

## Repository Structure

```text
AI_Support_Operations_SLA_Breach_Prediction/
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
├── models/
│   └── final_sla_breach_pipeline.joblib
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── README.md 07_triage_explanation_layer.py
├── requirements.txt
├── .gitignore
└── LICENSE

```

---

## Author

**Jumma Mohammad**

GitHub: https://github.com/jumma786

LinkedIn: https://www.linkedin.com/in/jumma-mohammad/

Email: jummamohammad477@gmail.com