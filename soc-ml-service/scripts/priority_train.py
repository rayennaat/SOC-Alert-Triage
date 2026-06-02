# final_optimal_training.py
"""
OPTIMAL APPROACH FOR PROJECT 4:
- Remove BENIGN traffic (not an alert)
- Train on ATTACKS ONLY
- Assign priorities based on attack severity
- This gives you a true "alert prioritization" system
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib

print("="*80)
print("OPTIMAL SOC ALERT PRIORITIZATION TRAINING")
print("="*80)

# Load dataset
df = pd.read_csv("data/merged_cleaned.csv", low_memory=False, encoding='utf-8-sig')
df.columns = df.columns.str.strip()

print(f"\n📊 Original dataset: {len(df):,} records")
print(f"Classes: {df['Label'].nunique()}")

# ========================================
# KEY INSIGHT: Remove BENIGN traffic
# BENIGN is not an "alert" - only attacks are!
# ========================================
df_alerts = df[df['Label'] != 'BENIGN'].copy()

print(f"\n✅ Alert-only dataset: {len(df_alerts):,} records")
print(f"Attack types: {df_alerts['Label'].nunique()}")
print("\nAttack distribution:")
print(df_alerts['Label'].value_counts())

# Define features (your existing 18 features)
FEATURES = [
    'Flow Duration',
    'Total Fwd Packets',
    'Total Backward Packets',
    'Flow Bytes/s',
    'Flow Packets/s',
    'Total Length of Fwd Packets',
    'Total Length of Bwd Packets',
    'Fwd Packet Length Mean',
    'Bwd Packet Length Mean',
    'Packet Length Std',
    'Flow IAT Mean',
    'Fwd IAT Mean',
    'Bwd IAT Mean',
    'PSH Flag Count',
    'SYN Flag Count',
    'FIN Flag Count',
    'Destination Port',
    'Down/Up Ratio'
]

# Priority mapping based on BUSINESS IMPACT
PRIORITY_MAPPING = {
    # CRITICAL: Immediate service disruption or data breach
    'DDoS': 'CRITICAL',
    'Heartbleed': 'CRITICAL',
    'Infiltration': 'CRITICAL',
    
    # HIGH: Serious security threat requiring urgent attention
    'DoS Hulk': 'HIGH',
    'DoS GoldenEye': 'HIGH',
    'Web Attack â€" Sql Injection': 'HIGH',
    'Bot': 'HIGH',
    
    # MEDIUM: Security concern requiring investigation
    'DoS Slowhttptest': 'MEDIUM',
    'DoS slowloris': 'MEDIUM',
    'FTP-Patator': 'MEDIUM',
    'SSH-Patator': 'MEDIUM',
    'Web Attack â€" Brute Force': 'MEDIUM',
    'Web Attack â€" XSS': 'MEDIUM',
    
    # LOW: Reconnaissance activity, not immediate threat
    'PortScan': 'LOW'
}

# Add priority column
df_alerts['Priority'] = df_alerts['Label'].map(PRIORITY_MAPPING)

# Handle any unmapped labels
if df_alerts['Priority'].isna().any():
    print("\n⚠️  Warning: Some labels not mapped to priority")
    print(df_alerts[df_alerts['Priority'].isna()]['Label'].unique())
    df_alerts = df_alerts.dropna(subset=['Priority'])

print("\n" + "="*80)
print("PRIORITY DISTRIBUTION")
print("="*80)
priority_counts = df_alerts['Priority'].value_counts()
for priority, count in priority_counts.items():
    pct = (count / len(df_alerts)) * 100
    print(f"{priority:12s}: {count:8,} ({pct:5.2f}%)")

# ========================================
# PREPARE DATA
# ========================================
X = df_alerts[FEATURES].copy()
y_attack = df_alerts['Label']      # Attack type
y_priority = df_alerts['Priority']  # Priority level

# Clean data
X = X.replace([float("inf"), float("-inf")], 0)
X = X.fillna(0)

# Encode labels
attack_encoder = LabelEncoder()
priority_encoder = LabelEncoder()

y_attack_encoded = attack_encoder.fit_transform(y_attack)
y_priority_encoded = priority_encoder.fit_transform(y_priority)

# ========================================
# TRAIN TWO MODELS
# ========================================

print("\n" + "="*80)
print("TRAINING MODEL 1: ATTACK CLASSIFICATION")
print("="*80)

X_train, X_test, y_attack_train, y_attack_test = train_test_split(
    X, y_attack_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_attack_encoded
)

attack_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", RandomForestClassifier(
        n_estimators=300,
        max_depth=25,
        min_samples_split=10,
        min_samples_leaf=4,
        max_features='sqrt',
        random_state=42,
        n_jobs=-1,
        class_weight='balanced',
        verbose=1
    ))
])

attack_pipeline.fit(X_train, y_attack_train)
y_attack_pred = attack_pipeline.predict(X_test)

print("\n📊 Attack Classification Performance:")
print(f"Accuracy: {accuracy_score(y_attack_test, y_attack_pred):.4f}")
print("\nTop 5 Classes by Sample Count:")
print(classification_report(
    y_attack_test, y_attack_pred,
    target_names=attack_encoder.classes_,
    zero_division=0
).split('\n')[:10])

# ========================================
# PRIORITY CLASSIFICATION
# ========================================

print("\n" + "="*80)
print("TRAINING MODEL 2: PRIORITY CLASSIFICATION")
print("="*80)

X_train_p, X_test_p, y_priority_train, y_priority_test = train_test_split(
    X, y_priority_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_priority_encoded
)

priority_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", RandomForestClassifier(
        n_estimators=300,
        max_depth=25,
        min_samples_split=10,
        min_samples_leaf=4,
        max_features='sqrt',
        random_state=42,
        n_jobs=-1,
        class_weight='balanced',
        verbose=1
    ))
])

priority_pipeline.fit(X_train_p, y_priority_train)
y_priority_pred = priority_pipeline.predict(X_test_p)

print("\n📊 Priority Classification Performance:")
print(f"Accuracy: {accuracy_score(y_priority_test, y_priority_pred):.4f}")
print("\n" + classification_report(
    y_priority_test, y_priority_pred,
    target_names=priority_encoder.classes_,
    zero_division=0
))

# Confusion matrix
print("\n" + "="*80)
print("CONFUSION MATRIX (Priority)")
print("="*80)
cm = confusion_matrix(y_priority_test, y_priority_pred)
print("\n         ", "  ".join(f"{p:8s}" for p in priority_encoder.classes_))
for i, priority in enumerate(priority_encoder.classes_):
    print(f"{priority:8s}", "  ".join(f"{cm[i,j]:8d}" for j in range(len(priority_encoder.classes_))))

# Per-class accuracy
print("\n" + "="*80)
print("PER-CLASS ACCURACY (Priority)")
print("="*80)
for i, priority in enumerate(priority_encoder.classes_):
    class_correct = cm[i, i]
    class_total = cm[i, :].sum()
    accuracy = (class_correct / class_total * 100) if class_total > 0 else 0
    print(f"{priority:12s}: {accuracy:6.2f}% ({class_correct:,}/{class_total:,})")

# ========================================
# SAVE MODELS
# ========================================
joblib.dump(attack_pipeline, "attack_classifier.joblib")
joblib.dump(attack_encoder, "attack_encoder.joblib")
joblib.dump(priority_pipeline, "priority_classifier.joblib")
joblib.dump(priority_encoder, "priority_encoder.joblib")
joblib.dump(FEATURES, "features.joblib")
joblib.dump(PRIORITY_MAPPING, "priority_mapping.joblib")

print("\n" + "="*80)
print("SAVED FILES")
print("="*80)
print("  ✅ attack_classifier.joblib      (Attack type classification)")
print("  ✅ attack_encoder.joblib")
print("  ✅ priority_classifier.joblib    (Direct priority classification)")
print("  ✅ priority_encoder.joblib")
print("  ✅ features.joblib")
print("  ✅ priority_mapping.joblib")

# ========================================
# TEST BOTH APPROACHES
# ========================================
print("\n" + "="*80)
print("TESTING: ATTACK CLASSIFICATION + MAPPING vs DIRECT PRIORITY")
print("="*80)

test_samples = df_alerts.sample(n=5, random_state=42)

for idx, row in test_samples.iterrows():
    features = row[FEATURES].values.reshape(1, -1)
    
    # Approach 1: Classify attack → Map to priority
    attack_pred = attack_pipeline.predict(features)[0]
    attack_type = attack_encoder.inverse_transform([attack_pred])[0]
    priority_mapped = PRIORITY_MAPPING.get(attack_type, 'MEDIUM')
    
    # Approach 2: Direct priority classification
    priority_pred = priority_pipeline.predict(features)[0]
    priority_direct = priority_encoder.inverse_transform([priority_pred])[0]
    
    # True values
    true_attack = row['Label']
    true_priority = row['Priority']
    
    print(f"\n{'='*70}")
    print(f"True Attack: {true_attack}")
    print(f"True Priority: {true_priority}")
    print(f"-" * 70)
    print(f"Approach 1 (Attack→Priority): {attack_type} → {priority_mapped} {'✅' if priority_mapped == true_priority else '❌'}")
    print(f"Approach 2 (Direct Priority):  {priority_direct} {'✅' if priority_direct == true_priority else '❌'}")

print("\n" + "="*80)
print("✅ TRAINING COMPLETE!")
print("="*80)
print("\n📋 You now have TWO approaches:")
print("   1. Attack Classification + Priority Mapping (more interpretable)")
print("   2. Direct Priority Classification (potentially more accurate)")
print("\n💡 Recommendation: Use Approach 1 for better explainability in SOC context")