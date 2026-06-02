# create_test_alerts.py
"""
Generate a CSV of sample alerts for testing the prioritization system
"""

import pandas as pd
from datetime import datetime, timedelta
import random

# Sample alerts with realistic features
alerts = []

# DDoS alerts (CRITICAL priority expected)
for i in range(10):
    alerts.append({
        'alert_id': f'ALERT-DDoS-{i+1:03d}',
        'source_ip': f'192.168.{random.randint(1,255)}.{random.randint(1,255)}',
        'dest_ip': '10.0.0.50',
        'timestamp': (datetime.now() - timedelta(hours=random.randint(0,24))).isoformat(),
        'Flow Duration': random.randint(50, 200),
        'Total Fwd Packets': random.randint(400000, 600000),
        'Total Backward Packets': random.randint(0, 10),
        'Flow Bytes/s': random.randint(80000000, 120000000),
        'Flow Packets/s': random.randint(400000, 600000),
        'Total Length of Fwd Packets': random.randint(8000000, 12000000),
        'Total Length of Bwd Packets': random.randint(0, 1000),
        'Fwd Packet Length Mean': random.randint(15, 25),
        'Bwd Packet Length Mean': random.randint(0, 10),
        'Packet Length Std': random.randint(3, 8),
        'Flow IAT Mean': random.uniform(0.0001, 0.0005),
        'Fwd IAT Mean': random.uniform(0.0001, 0.0005),
        'Bwd IAT Mean': random.uniform(0, 0.001),
        'PSH Flag Count': 0,
        'SYN Flag Count': random.randint(0, 10),
        'FIN Flag Count': 0,
        'Destination Port': random.choice([80, 443, 53]),
        'Down/Up Ratio': random.uniform(0, 0.1)
    })

# Port Scan alerts (LOW priority expected)
for i in range(15):
    alerts.append({
        'alert_id': f'ALERT-SCAN-{i+1:03d}',
        'source_ip': f'203.0.{random.randint(1,255)}.{random.randint(1,255)}',
        'dest_ip': f'10.0.0.{random.randint(1,255)}',
        'timestamp': (datetime.now() - timedelta(hours=random.randint(0,24))).isoformat(),
        'Flow Duration': random.randint(8000, 12000),
        'Total Fwd Packets': random.randint(4000, 6000),
        'Total Backward Packets': random.randint(0, 5),
        'Flow Bytes/s': random.randint(15000, 25000),
        'Flow Packets/s': random.randint(400, 600),
        'Total Length of Fwd Packets': random.randint(150000, 250000),
        'Total Length of Bwd Packets': random.randint(0, 1000),
        'Fwd Packet Length Mean': random.randint(35, 45),
        'Bwd Packet Length Mean': random.randint(0, 10),
        'Packet Length Std': random.randint(0, 5),
        'Flow IAT Mean': random.uniform(1.5, 2.5),
        'Fwd IAT Mean': random.uniform(1.5, 2.5),
        'Bwd IAT Mean': 0,
        'PSH Flag Count': 0,
        'SYN Flag Count': random.randint(4000, 6000),
        'FIN Flag Count': 0,
        'Destination Port': random.choice([22, 23, 3389, 80, 443]),
        'Down/Up Ratio': 0
    })

# SSH Brute Force (MEDIUM priority expected)
for i in range(8):
    alerts.append({
        'alert_id': f'ALERT-SSH-{i+1:03d}',
        'source_ip': f'198.51.{random.randint(1,255)}.{random.randint(1,255)}',
        'dest_ip': '10.0.0.100',
        'timestamp': (datetime.now() - timedelta(hours=random.randint(0,24))).isoformat(),
        'Flow Duration': random.randint(3000, 6000),
        'Total Fwd Packets': random.randint(150, 250),
        'Total Backward Packets': random.randint(140, 240),
        'Flow Bytes/s': random.randint(8000, 15000),
        'Flow Packets/s': random.randint(40, 60),
        'Total Length of Fwd Packets': random.randint(15000, 25000),
        'Total Length of Bwd Packets': random.randint(14000, 24000),
        'Fwd Packet Length Mean': random.randint(90, 110),
        'Bwd Packet Length Mean': random.randint(95, 105),
        'Packet Length Std': random.randint(15, 25),
        'Flow IAT Mean': random.uniform(18, 22),
        'Fwd IAT Mean': random.uniform(19, 23),
        'Bwd IAT Mean': random.uniform(20, 24),
        'PSH Flag Count': random.randint(80, 120),
        'SYN Flag Count': random.randint(1, 3),
        'FIN Flag Count': random.randint(1, 3),
        'Destination Port': 22,
        'Down/Up Ratio': random.uniform(0.85, 0.95)
    })

# Web Attack - SQL Injection (HIGH priority expected)
for i in range(5):
    alerts.append({
        'alert_id': f'ALERT-SQLI-{i+1:03d}',
        'source_ip': f'185.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
        'dest_ip': '10.0.1.50',
        'timestamp': (datetime.now() - timedelta(hours=random.randint(0,24))).isoformat(),
        'Flow Duration': random.randint(2000, 4000),
        'Total Fwd Packets': random.randint(40, 70),
        'Total Backward Packets': random.randint(35, 65),
        'Flow Bytes/s': random.randint(60000, 90000),
        'Flow Packets/s': random.randint(18, 28),
        'Total Length of Fwd Packets': random.randint(70000, 100000),
        'Total Length of Bwd Packets': random.randint(60000, 90000),
        'Fwd Packet Length Mean': random.randint(1400, 1700),
        'Bwd Packet Length Mean': random.randint(1450, 1650),
        'Packet Length Std': random.randint(350, 450),
        'Flow IAT Mean': random.uniform(35, 45),
        'Fwd IAT Mean': random.uniform(37, 43),
        'Bwd IAT Mean': random.uniform(40, 48),
        'PSH Flag Count': random.randint(20, 35),
        'SYN Flag Count': 1,
        'FIN Flag Count': 1,
        'Destination Port': 80,
        'Down/Up Ratio': random.uniform(0.82, 0.92)
    })

# Create DataFrame
df = pd.DataFrame(alerts)

# Shuffle
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save to CSV
output_file = 'test_alerts.csv'
df.to_csv(output_file, index=False)

print("="*80)
print("TEST ALERTS CSV GENERATED")
print("="*80)
print(f"File: {output_file}")
print(f"Total alerts: {len(df)}")
print("\nAlert distribution:")
print(f"  DDoS (CRITICAL expected):       10")
print(f"  Port Scans (LOW expected):      15")
print(f"  SSH Brute Force (MEDIUM expected): 8")
print(f"  SQL Injection (HIGH expected):   5")
print("\n" + "="*80)
print("USAGE:")
print("="*80)
print("1. Start your API: python simple_wrapper_api.py")
print("2. Upload this CSV to: POST /prioritize/csv")
print("3. Or use curl:")
print(f'   curl -X POST -F "file=@{output_file}" http://localhost:8000/prioritize/csv')
print("="*80)