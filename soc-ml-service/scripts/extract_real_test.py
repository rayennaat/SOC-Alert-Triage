# test_with_real_data.py - FIXED VERSION
import pandas as pd
import joblib
import numpy as np
from datetime import datetime, timedelta
import random

print("="*80)
print("EXTRACTING REAL TEST SAMPLES FROM DATASET")
print("="*80)

# Load your actual dataset
df = pd.read_csv("data/merged_cleaned.csv", low_memory=False, encoding='utf-8-sig')
df.columns = df.columns.str.strip()

# Remove BENIGN
df_alerts = df[df['Label'] != 'BENIGN'].copy()

print(f"\n📊 Total alerts in dataset: {len(df_alerts):,}")
print(f"Attack types: {df_alerts['Label'].nunique()}")

# Sample REAL attacks (5 per type)
test_samples = df_alerts.groupby('Label').apply(
    lambda x: x.sample(n=min(5, len(x)), random_state=42)
).reset_index(drop=True)

print(f"\n✅ Extracted {len(test_samples)} REAL test samples")
print("\nDistribution:")
print(test_samples['Label'].value_counts())

# Define features
FEATURES = joblib.load("features.joblib")
PRIORITY_MAPPING = joblib.load("priority_mapping.joblib")

# Add expected priority
test_samples['expected_priority'] = test_samples['Label'].map(PRIORITY_MAPPING)

# ========================================================================
# ADD REQUIRED METADATA COLUMNS
# ========================================================================

# Generate alert IDs
test_samples['alert_id'] = [
    f"ALERT-{label.replace(' ', '').replace('�','')}-{i+1:03d}"
    for i, label in enumerate(test_samples['Label'])
]

# Use actual IPs if available, otherwise generate realistic ones
if 'Source IP' in test_samples.columns:
    test_samples['source_ip'] = test_samples['Source IP']
else:
    # Generate realistic source IPs (external)
    test_samples['source_ip'] = [
        f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
        for _ in range(len(test_samples))
    ]

if 'Destination IP' in test_samples.columns:
    test_samples['dest_ip'] = test_samples['Destination IP']
else:
    # Generate realistic dest IPs (internal 10.x.x.x)
    test_samples['dest_ip'] = [
        f"10.0.{random.randint(0, 255)}.{random.randint(1, 254)}"
        for _ in range(len(test_samples))
    ]

# Generate timestamps (last 48 hours)
base_time = datetime.now() - timedelta(hours=48)
test_samples['timestamp'] = [
    (base_time + timedelta(minutes=random.randint(0, 2880))).isoformat()
    for _ in range(len(test_samples))
]

# ========================================================================
# PREPARE OUTPUT CSV
# ========================================================================

# Columns needed for API
output_cols = [
    'alert_id',
    'source_ip', 
    'dest_ip',
    'timestamp',
    'Label',  # Keep for reference
    'expected_priority'  # Keep for validation
] + FEATURES

# Ensure all feature columns exist
for feat in FEATURES:
    if feat not in test_samples.columns:
        print(f"⚠️  Warning: Feature '{feat}' not in dataset, filling with 0")
        test_samples[feat] = 0

# Clean data
test_samples_clean = test_samples[output_cols].copy()
test_samples_clean = test_samples_clean.replace([np.inf, -np.inf], 0)
test_samples_clean = test_samples_clean.fillna(0)

# Save
test_samples_clean.to_csv("real_test_alerts.csv", index=False)

print("\n" + "="*80)
print("✅ SAVED: real_test_alerts.csv")
print("="*80)
print(f"Total samples: {len(test_samples_clean)}")
print(f"Columns: {len(output_cols)}")
print("\nFirst 3 rows preview:")
print(test_samples_clean[['alert_id', 'Label', 'expected_priority', 'source_ip', 'dest_ip']].head(3))

# ========================================================================
# SHOW EXPECTED RESULTS
# ========================================================================
print("\n" + "="*80)
print("EXPECTED RESULTS BY ATTACK TYPE")
print("="*80)

expected_summary = test_samples_clean.groupby(['Label', 'expected_priority']).size().reset_index(name='count')
for _, row in expected_summary.iterrows():
    print(f"{row['Label']:30s} → {row['expected_priority']:10s} ({row['count']} samples)")

print("\n" + "="*80)
print("NOW TEST WITH:")
print("="*80)
print('curl -X POST http://localhost:8000/prioritize/csv -F "file=@real_test_alerts.csv"')
print("\nOr in Python:")
print("""
import requests
with open('real_test_alerts.csv', 'rb') as f:
    response = requests.post('http://localhost:8000/prioritize/csv', files={'file': f})
    print(response.json())
""")