# AI-Driven SOC Analyst Assistant for Alert Prioritization

An ML-assisted Security Operations Center (SOC) platform designed to reduce alert fatigue by classifying network attacks and automatically prioritizing security alerts in near real-time environments.

This project combines machine learning, backend orchestration, and analyst-focused visualization to simulate a modern SOC triage workflow.

---

# Overview

Security Operations Centers receive thousands of alerts daily, many of which are false positives or low-priority events. Analysts must quickly identify critical threats while avoiding alert fatigue.

This project addresses that challenge through a dual-stage machine learning pipeline capable of:

- Classifying attack types from network traffic features
- Predicting alert priority levels
- Providing analyst-friendly visualization through a web dashboard
- Exposing inference endpoints through documented REST APIs

The platform was designed as a realistic SOC automation prototype integrating ML inference with enterprise-style backend architecture.

---

# Key Features

- Dual-stage ML classification pipeline
- Attack type prediction (11 classes)
- Alert priority prediction (4 severity levels)
- REST API integration with Swagger documentation
- Spring Boot backend orchestration
- React SOC dashboard
- FastAPI inference service
- CIC-IDS2017 dataset integration
- Weighted classification for heavily imbalanced datasets
- Real-time and batch-processing design considerations
- Analyst-focused workflow visualization

---

# Architecture

```text
Network Alerts / Traffic Features
                │
                ▼
        Feature Engineering
                │
                ▼
        FastAPI ML Service
        ├── Attack Classifier
        └── Priority Classifier
                │
                ▼
      Spring Boot Backend API
                │
                ▼
         React SOC Dashboard
```

---

# Technology Stack

## Backend
- Java
- Spring Boot
- REST APIs
- Swagger/OpenAPI

## Machine Learning
- Python
- FastAPI
- Scikit-learn
- Random Forest Classifier
- Pandas
- NumPy

## Frontend
- React

## Dataset
- CIC-IDS2017 Dataset

---

# Machine Learning Pipeline

## Attack Classification
Predicts one of 11 attack categories from network traffic features.

Examples:
- DoS
- DDoS
- PortScan
- Brute Force
- Web Attacks
- Botnet-related traffic

## Priority Classification
Predicts alert severity across 4 priority levels to assist SOC analysts in triage decisions.

---

# Feature Engineering

The models were trained using 18 network flow features extracted from raw traffic data, including:

- Flow characteristics
- Packet size patterns
- TCP flag behavior
- Connection timing
- Traffic direction statistics

The goal was to preserve strong security-relevant behavioral indicators while enabling fast inference.

---

# Dataset

This project uses the CIC-IDS2017 dataset developed by the Canadian Institute for Cybersecurity.

Dataset characteristics:
- ~2.8 million records
- 80+ original features
- Enterprise-style network simulation
- Multiple attack categories
- Highly imbalanced class distribution

---

# Handling Dataset Imbalance

One of the primary challenges was severe dataset imbalance.

Example:
- DoS Hulk: ~231,000 samples
- Heartbleed: 11 samples

To mitigate this issue:
- weighted classification strategies were implemented
- preprocessing and normalization workflows were applied
- model evaluation emphasized recall and false-negative reduction

---

# Model Selection

Several approaches were evaluated:

| Model | Advantages | Limitations |
|---|---|---|
| Logistic Regression | Fast inference | Lower accuracy |
| Random Forest | High accuracy + explainability | Medium latency |
| Isolation Forest | Novelty detection | Harder tuning |
| Neural Networks | Strong performance | Higher compute cost |

Random Forest was selected as the primary architecture due to:
- strong classification performance
- interpretability
- robustness on structured traffic features
- balanced operational cost

---

# Security & SOC Considerations

The platform was designed with realistic SOC operational constraints in mind:

- alert fatigue reduction
- false positive management
- confidence-based prioritization
- near real-time inference
- scalability considerations
- analyst workflow support

The system intentionally follows a human-in-the-loop approach rather than fully autonomous threat response.

---

# Risks & Limitations

This project is a research/educational SOC prototype and has important limitations:

- trained primarily on known attack patterns
- limited zero-day detection capability
- dependent on dataset quality
- susceptible to distribution drift in real environments
- not intended for production autonomous blocking

Future versions may incorporate:
- threat intelligence feeds
- graph-based correlation
- deep learning models
- continuous retraining pipelines
- SIEM integrations

---

# Future Improvements

Planned enhancements include:

- Docker/Kubernetes deployment
- Wazuh/Splunk integration
- analyst feedback loops
- streaming inference pipelines
- real-time packet ingestion
- role-based authentication
- advanced SOC visualizations
- anomaly detection modules

---

# Project Structure

```text
backend/
├── controllers/
├── services/
├── services/impl/
├── repositories/
├── domain/
└── dto/

ml-service/
├── models/
├── preprocessing/
├── inference/
└── datasets/

frontend/
├── dashboard/
├── components/
└── api/
```

---

# Learning Objectives

This project was developed to explore:
- SOC automation workflows
- ML-assisted security operations
- network traffic analysis
- backend/API orchestration
- scalable security system architecture
- operational cybersecurity constraints

---

# Authors

- Mohamed Mensi
- Hilmi Ouelhazi
- Rayen Naat
- Youssef Ayari

---

# Disclaimer

This project was developed for educational and research purposes only.

It is not intended for offensive use or production-grade autonomous threat response.
