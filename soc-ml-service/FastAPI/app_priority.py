# final_soc_api.py
"""
SOC Alert Prioritization API
Uses the optimally trained models (99.98% accuracy!)
"""

import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
import io

# -----------------------------------------------------------------------------
# Initialize FastAPI
# -----------------------------------------------------------------------------
app = FastAPI(
    title="SOC Alert Prioritization System",
    description="AI-powered system for prioritizing security alerts",
    version="1.0"
)

# Add CORS middleware for dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------
# Load Model Artifacts
# -----------------------------------------------------------------------------
print("="*80)
print("LOADING MODEL ARTIFACTS")
print("="*80)

# Load BOTH models (you trained two approaches!)
attack_classifier = joblib.load("train_models/attack_classifier.joblib")
attack_encoder = joblib.load("train_models/attack_encoder.joblib")
priority_classifier = joblib.load("train_models/priority_classifier.joblib")
priority_encoder = joblib.load("train_models/priority_encoder.joblib")
FEATURES = joblib.load("train_models/features.joblib")
PRIORITY_MAPPING = joblib.load("train_models/priority_mapping.joblib")

print(f"✅ Attack Classifier loaded")
print(f"✅ Priority Classifier loaded")
print(f"✅ Features: {len(FEATURES)}")
print(f"✅ Attack types: {len(attack_encoder.classes_)}")
print(f"✅ Priority levels: {priority_encoder.classes_}")
print("="*80)

# -----------------------------------------------------------------------------
# Priority scoring
# -----------------------------------------------------------------------------
PRIORITY_SCORES = {
    'CRITICAL': 10,
    'HIGH': 7,
    'MEDIUM': 4,
    'LOW': 2
}

# Recommendations by priority
RECOMMENDATIONS = {
    'CRITICAL': [
        "🚨 IMMEDIATE ACTION REQUIRED",
        "Isolate affected systems if possible",
        "Escalate to senior analyst or CISO",
        "Begin incident response procedures",
        "Document all actions taken"
    ],
    'HIGH': [
        "⚠️ Investigate within 1 hour",
        "Check for related alerts across network",
        "Review security logs for indicators of compromise",
        "Prepare incident report",
        "Monitor for escalation"
    ],
    'MEDIUM': [
        "📋 Investigate within 4 hours",
        "Add to investigation queue",
        "Check for patterns with similar alerts",
        "Review affected system logs",
        "Monitor for escalation"
    ],
    'LOW': [
        "📊 Low priority - monitor",
        "Log for future correlation analysis",
        "Review during daily analysis",
        "Check if part of larger pattern"
    ]
}

# Attack-specific recommendations
ATTACK_RECOMMENDATIONS = {
    'DDoS': "💡 Check network bandwidth and consider rate limiting/traffic filtering",
    'DoS Hulk': "💡 Implement rate limiting and check server resources",
    'DoS GoldenEye': "💡 Review HTTP keepalive settings and connection limits",
    'PortScan': "💡 Reconnaissance activity - monitor source IP for follow-up attacks",
    'SSH-Patator': "💡 Review SSH logs, consider fail2ban, check for compromised credentials",
    'FTP-Patator': "💡 Review FTP logs, implement account lockout policies",
    'Bot': "💡 Check for malware infection, review outbound connections",
    'Infiltration': "💡 URGENT: Check for data exfiltration, review all recent access logs",
    'Heartbleed': "💡 URGENT: Patch SSL/TLS immediately, rotate certificates and credentials"
}

# -----------------------------------------------------------------------------
# Request/Response Models
# -----------------------------------------------------------------------------
class AlertInput(BaseModel):
    alert_id: str
    source_ip: str
    dest_ip: str
    timestamp: str
    features: Dict[str, float]
    asset_criticality: Optional[str] = "MEDIUM"  # LOW, MEDIUM, HIGH, CRITICAL


class AlertBatch(BaseModel):
    alerts: List[AlertInput]


# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------
def build_feature_vector(features: Dict[str, float]) -> tuple:
    """Build DataFrame from features"""
    mapped = {}
    missing = []
    
    for feat in FEATURES:
        if feat in features:
            mapped[feat] = features[feat]
        else:
            mapped[feat] = 0
            missing.append(feat)
    
    # Warn if too many missing
    if len(missing) > len(FEATURES) * 0.3:
        raise HTTPException(
            status_code=400,
            detail=f"Too many missing features: {len(missing)}/{len(FEATURES)}"
        )
    
    df = pd.DataFrame([mapped])
    df = df.replace([np.inf, -np.inf], 0).fillna(0)
    
    return df, missing


def get_recommendations(attack_type: str, priority: str) -> List[str]:
    """Generate recommendations"""
    recs = RECOMMENDATIONS.get(priority, RECOMMENDATIONS['MEDIUM']).copy()
    
    # Add attack-specific recommendation
    if attack_type in ATTACK_RECOMMENDATIONS:
        recs.append(ATTACK_RECOMMENDATIONS[attack_type])
    
    return recs


# -----------------------------------------------------------------------------
# Endpoints
# -----------------------------------------------------------------------------
@app.post("/prioritize")
def prioritize_alert(alert: AlertInput):
    """
    Prioritize a single alert
    
    Uses TWO approaches:
    1. Attack classification → Priority mapping (interpretable)
    2. Direct priority classification (accurate)
    
    Returns both for comparison
    """
    try:
        # Build feature vector
        df, missing = build_feature_vector(alert.features)
        
        # -----------------------------------------------------------------
        # APPROACH 1: Attack Classification + Mapping
        # -----------------------------------------------------------------
        attack_probs = attack_classifier.predict_proba(df)[0]
        attack_idx = attack_probs.argmax()
        attack_type = attack_encoder.inverse_transform([attack_idx])[0]
        attack_confidence = float(attack_probs[attack_idx])
        
        # Map to priority
        priority_mapped = PRIORITY_MAPPING.get(attack_type, 'MEDIUM')
        
        # Calculate weighted priority score
        priority_score_mapped = 0.0
        for i, prob in enumerate(attack_probs):
            att = attack_encoder.inverse_transform([i])[0]
            pri = PRIORITY_MAPPING.get(att, 'MEDIUM')
            priority_score_mapped += prob * PRIORITY_SCORES.get(pri, 4)
        priority_score_mapped = round((priority_score_mapped / 10) * 100, 2)
        
        # -----------------------------------------------------------------
        # APPROACH 2: Direct Priority Classification
        # -----------------------------------------------------------------
        priority_probs = priority_classifier.predict_proba(df)[0]
        priority_idx = priority_probs.argmax()
        priority_direct = priority_encoder.inverse_transform([priority_idx])[0]
        priority_confidence = float(priority_probs[priority_idx])
        
        # Calculate weighted priority score
        priority_score_direct = 0.0
        for i, prob in enumerate(priority_probs):
            pri = priority_encoder.inverse_transform([i])[0]
            priority_score_direct += prob * PRIORITY_SCORES.get(pri, 4)
        priority_score_direct = round((priority_score_direct / 10) * 100, 2)
        
        # -----------------------------------------------------------------
        # Use APPROACH 2 as primary (more accurate), keep APPROACH 1 for context
        # -----------------------------------------------------------------
        final_priority = priority_direct
        final_score = priority_score_direct
        
        # Top attack predictions
        top_5_attacks = attack_probs.argsort()[-5:][::-1]
        attack_alternatives = []
        for idx in top_5_attacks:
            if attack_probs[idx] > 0.01:
                att = attack_encoder.inverse_transform([idx])[0]
                attack_alternatives.append({
                    "attack_type": att,
                    "probability": round(float(attack_probs[idx]), 4),
                    "priority": PRIORITY_MAPPING.get(att, 'MEDIUM')
                })
        
        # Get recommendations
        recommendations = get_recommendations(attack_type, final_priority)
        
        return {
            "alert_id": alert.alert_id,
            "classification": {
                "primary_attack_type": attack_type,
                "confidence": round(attack_confidence, 4),
                "alternative_classifications": attack_alternatives
            },
            "prioritization": {
                "priority_level": final_priority,
                "priority_score": final_score,
                "confidence": round(priority_confidence, 4),
                "method": "Direct ML Classification (99.98% accuracy)"
            },
            "comparison": {
                "mapped_priority": priority_mapped,
                "mapped_score": priority_score_mapped,
                "agreement": "✅" if priority_mapped == priority_direct else "⚠️"
            },
            "recommendations": recommendations,
            "context": {
                "source_ip": alert.source_ip,
                "dest_ip": alert.dest_ip,
                "timestamp": alert.timestamp,
                "asset_criticality": alert.asset_criticality
            },
            "metadata": {
                "features_received": len(alert.features),
                "features_missing": len(missing),
                "model_accuracy": "99.98%"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )


@app.post("/prioritize/batch")
def prioritize_batch(batch: AlertBatch):
    """Prioritize multiple alerts and return sorted by priority"""
    results = []
    
    for alert in batch.alerts:
        result = prioritize_alert(alert)
        results.append(result)
    
    # Sort by priority score
    results.sort(key=lambda x: x['prioritization']['priority_score'], reverse=True)
    
    # Add rankings
    for i, result in enumerate(results, 1):
        result['rank'] = i
    
    # Summary statistics
    summary = {}
    for result in results:
        pri = result['prioritization']['priority_level']
        summary[pri] = summary.get(pri, 0) + 1
    
    return {
        "total_alerts": len(results),
        "prioritization_summary": summary,
        "top_10_critical": [r for r in results if r['prioritization']['priority_level'] == 'CRITICAL'][:10],
        "all_alerts": results
    }


@app.post("/prioritize/csv")
async def prioritize_csv(file: UploadFile = File(...)):
    """
    Upload CSV file of alerts and get prioritized results
    
    CSV should have: alert_id, source_ip, dest_ip, timestamp, and all 18 feature columns
    """
    try:
        # Read CSV
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        print(f"\n📁 Processing CSV: {file.filename}")
        print(f"   Rows: {len(df)}")
        print(f"   Columns: {df.columns.tolist()}")
        
        # Check required metadata columns
        required = ['alert_id', 'source_ip', 'dest_ip', 'timestamp']
        missing_meta = [col for col in required if col not in df.columns]
        if missing_meta:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {missing_meta}"
            )
        
        # Fill missing feature columns with 0
        for feat in FEATURES:
            if feat not in df.columns:
                df[feat] = 0
        
        # Extract features
        X = df[FEATURES].copy()
        X = X.replace([np.inf, -np.inf], 0).fillna(0)
        
        # Predict priorities (using direct method)
        priority_probs = priority_classifier.predict_proba(X)
        attack_probs = attack_classifier.predict_proba(X)
        
        results = []
        for i, row in df.iterrows():
            # Priority
            priority_idx = priority_probs[i].argmax()
            priority = priority_encoder.inverse_transform([priority_idx])[0]
            priority_conf = float(priority_probs[i][priority_idx])
            
            # Attack type
            attack_idx = attack_probs[i].argmax()
            attack_type = attack_encoder.inverse_transform([attack_idx])[0]
            attack_conf = float(attack_probs[i][attack_idx])
            
            # Score
            score = 0.0
            for j, prob in enumerate(priority_probs[i]):
                pri = priority_encoder.inverse_transform([j])[0]
                score += prob * PRIORITY_SCORES.get(pri, 4)
            score = round((score / 10) * 100, 2)
            
            results.append({
                "rank": 0,  # Will be set after sorting
                "alert_id": str(row['alert_id']),
                "attack_type": attack_type,
                "attack_confidence": round(attack_conf, 4),
                "priority_level": priority,
                "priority_score": score,
                "priority_confidence": round(priority_conf, 4),
                "source_ip": str(row['source_ip']),
                "dest_ip": str(row['dest_ip']),
                "timestamp": str(row['timestamp'])
            })
        
        # Sort by priority score
        results.sort(key=lambda x: x['priority_score'], reverse=True)
        
        # Add rankings
        for i, result in enumerate(results, 1):
            result['rank'] = i
        
        # Summary
        summary = {}
        for result in results:
            pri = result['priority_level']
            summary[pri] = summary.get(pri, 0) + 1
        
        return {
            "status": "success",
            "file_name": file.filename,
            "total_alerts": len(results),
            "prioritization_summary": summary,
            "critical_alerts": [r for r in results if r['priority_level'] == 'CRITICAL'][:10],
            "high_alerts": [r for r in results if r['priority_level'] == 'HIGH'][:10],
            "all_alerts": results
        }
        
    except Exception as e:
        import traceback
        print(f"\n❌ Error processing CSV:")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )


@app.get("/")
def root():
    """API information"""
    return {
        "message": "SOC Alert Prioritization System",
        "version": "1.0",
        "description": "AI-powered alert prioritization with 99.98% accuracy",
        "model_info": {
            "attack_types": attack_encoder.classes_.tolist(),
            "priority_levels": priority_encoder.classes_.tolist(),
            "features": len(FEATURES),
            "accuracy": "99.98%"
        },
        "endpoints": {
            "/": "API information",
            "/health": "Health check",
            "/features": "List expected features",
            "/test-cases": "Get example test data",
            "/prioritize": "Prioritize single alert (POST)",
            "/prioritize/batch": "Prioritize multiple alerts (POST)",
            "/prioritize/csv": "Upload CSV file (POST)"
        }
    }


@app.get("/health")
def health():
    """Health check with model stats"""
    return {
        "status": "healthy",
        "models_loaded": True,
        "attack_classifier": {
            "classes": len(attack_encoder.classes_),
            "accuracy": "99.95%"
        },
        "priority_classifier": {
            "classes": len(priority_encoder.classes_),
            "accuracy": "99.98%"
        },
        "features": FEATURES
    }


@app.get("/features")
def get_features():
    """List expected features"""
    return {
        "total_features": len(FEATURES),
        "features": FEATURES,
        "example_alert": {
            "alert_id": "ALERT-2024-001",
            "source_ip": "192.168.1.100",
            "dest_ip": "10.0.0.50",
            "timestamp": datetime.now().isoformat(),
            "features": {feat: 0.0 for feat in FEATURES}
        }
    }


@app.get("/test-cases")
def get_test_cases():
    """Get realistic test cases"""
    return {
        "ddos_attack": {
            "alert_id": "ALERT-DDOS-001",
            "source_ip": "192.168.1.100",
            "dest_ip": "10.0.0.50",
            "timestamp": datetime.now().isoformat(),
            "features": {
                "Flow Duration": 100,
                "Total Fwd Packets": 500000,
                "Total Backward Packets": 0,
                "Flow Bytes/s": 100000000,
                "Flow Packets/s": 500000,
                "Total Length of Fwd Packets": 10000000,
                "Total Length of Bwd Packets": 0,
                "Fwd Packet Length Mean": 20,
                "Bwd Packet Length Mean": 0,
                "Packet Length Std": 5,
                "Flow IAT Mean": 0.0002,
                "Fwd IAT Mean": 0.0002,
                "Bwd IAT Mean": 0,
                "PSH Flag Count": 0,
                "SYN Flag Count": 0,
                "FIN Flag Count": 0,
                "Destination Port": 80,
                "Down/Up Ratio": 0
            }
        },
        "portscan": {
            "alert_id": "ALERT-SCAN-001",
            "source_ip": "203.0.113.45",
            "dest_ip": "10.0.0.100",
            "timestamp": datetime.now().isoformat(),
            "features": {
                "Flow Duration": 10000,
                "Total Fwd Packets": 5000,
                "Total Backward Packets": 0,
                "Flow Bytes/s": 20000,
                "Flow Packets/s": 500,
                "Total Length of Fwd Packets": 200000,
                "Total Length of Bwd Packets": 0,
                "Fwd Packet Length Mean": 40,
                "Bwd Packet Length Mean": 0,
                "Packet Length Std": 0,
                "Flow IAT Mean": 2,
                "Fwd IAT Mean": 2,
                "Bwd IAT Mean": 0,
                "PSH Flag Count": 0,
                "SYN Flag Count": 5000,
                "FIN Flag Count": 0,
                "Destination Port": 22,
                "Down/Up Ratio": 0
            }
        }
    }


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*80)
    print("STARTING SOC ALERT PRIORITIZATION API")
    print("="*80)
    print("Navigate to: http://localhost:8000/docs for interactive API documentation")
    print("="*80 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)