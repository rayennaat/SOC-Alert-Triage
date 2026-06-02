# generate_test_alerts.py
"""
Generate realistic test alert data for the SOC prioritization system
Creates both JSON and CSV test files
"""

import pandas as pd
import json
from datetime import datetime, timedelta
import random

# Load the feature names
import joblib
FEATURES = joblib.load("features.joblib")

print("="*80)
print("GENERATING TEST ALERT DATA")
print("="*80)

# Attack patterns based on CIC-IDS-2017 characteristics
ATTACK_PATTERNS = {
    'DDoS': {
        'count': 10,
        'priority_expected': 'CRITICAL',
        'pattern': {
            'Flow Duration': (50, 200),
            'Total Fwd Packets': (400000, 600000),
            'Total Backward Packets': (0, 10),
            'Flow Bytes/s': (80000000, 120000000),
            'Flow Packets/s': (400000, 600000),
            'Total Length of Fwd Packets': (8000000, 12000000),
            'Total Length of Bwd Packets': (0, 1000),
            'Fwd Packet Length Mean': (15, 25),
            'Bwd Packet Length Mean': (0, 10),
            'Packet Length Std': (3, 8),
            'Flow IAT Mean': (0.0001, 0.0005),
            'Fwd IAT Mean': (0.0001, 0.0005),
            'Bwd IAT Mean': (0, 0.001),
            'PSH Flag Count': (0, 5),
            'SYN Flag Count': (0, 10),
            'FIN Flag Count': (0, 5),
            'Destination Port': [80, 443, 53],
            'Down/Up Ratio': (0, 0.1)
        }
    },
    'DoS Hulk': {
        'count': 8,
        'priority_expected': 'HIGH',
        'pattern': {
            'Flow Duration': (100, 500),
            'Total Fwd Packets': (100000, 300000),
            'Total Backward Packets': (0, 100),
            'Flow Bytes/s': (50000000, 90000000),
            'Flow Packets/s': (100000, 300000),
            'Total Length of Fwd Packets': (5000000, 9000000),
            'Total Length of Bwd Packets': (0, 10000),
            'Fwd Packet Length Mean': (45, 55),
            'Bwd Packet Length Mean': (0, 20),
            'Packet Length Std': (10, 20),
            'Flow IAT Mean': (0.0003, 0.001),
            'Fwd IAT Mean': (0.0003, 0.001),
            'Bwd IAT Mean': (0, 0.005),
            'PSH Flag Count': (0, 10),
            'SYN Flag Count': (0, 20),
            'FIN Flag Count': (0, 10),
            'Destination Port': [80, 8080, 443],
            'Down/Up Ratio': (0, 0.05)
        }
    },
    'PortScan': {
        'count': 15,
        'priority_expected': 'LOW',
        'pattern': {
            'Flow Duration': (8000, 12000),
            'Total Fwd Packets': (4000, 6000),
            'Total Backward Packets': (0, 5),
            'Flow Bytes/s': (15000, 25000),
            'Flow Packets/s': (400, 600),
            'Total Length of Fwd Packets': (150000, 250000),
            'Total Length of Bwd Packets': (0, 1000),
            'Fwd Packet Length Mean': (35, 45),
            'Bwd Packet Length Mean': (0, 10),
            'Packet Length Std': (0, 5),
            'Flow IAT Mean': (1.5, 2.5),
            'Fwd IAT Mean': (1.5, 2.5),
            'Bwd IAT Mean': (0, 0.1),
            'PSH Flag Count': (0, 5),
            'SYN Flag Count': (4000, 6000),
            'FIN Flag Count': (0, 5),
            'Destination Port': [22, 23, 80, 443, 3389, 8080],
            'Down/Up Ratio': (0, 0.01)
        }
    },
    'SSH-Patator': {
        'count': 8,
        'priority_expected': 'MEDIUM',
        'pattern': {
            'Flow Duration': (3000, 6000),
            'Total Fwd Packets': (150, 250),
            'Total Backward Packets': (140, 240),
            'Flow Bytes/s': (8000, 15000),
            'Flow Packets/s': (40, 60),
            'Total Length of Fwd Packets': (15000, 25000),
            'Total Length of Bwd Packets': (14000, 24000),
            'Fwd Packet Length Mean': (90, 110),
            'Bwd Packet Length Mean': (95, 105),
            'Packet Length Std': (15, 25),
            'Flow IAT Mean': (18, 22),
            'Fwd IAT Mean': (19, 23),
            'Bwd IAT Mean': (20, 24),
            'PSH Flag Count': (80, 120),
            'SYN Flag Count': (1, 3),
            'FIN Flag Count': (1, 3),
            'Destination Port': [22],
            'Down/Up Ratio': (0.85, 0.95)
        }
    },
    'FTP-Patator': {
        'count': 5,
        'priority_expected': 'MEDIUM',
        'pattern': {
            'Flow Duration': (4000, 8000),
            'Total Fwd Packets': (200, 350),
            'Total Backward Packets': (190, 340),
            'Flow Bytes/s': (10000, 18000),
            'Flow Packets/s': (35, 55),
            'Total Length of Fwd Packets': (20000, 35000),
            'Total Length of Bwd Packets': (19000, 34000),
            'Fwd Packet Length Mean': (85, 105),
            'Bwd Packet Length Mean': (90, 100),
            'Packet Length Std': (18, 28),
            'Flow IAT Mean': (20, 25),
            'Fwd IAT Mean': (21, 26),
            'Bwd IAT Mean': (22, 27),
            'PSH Flag Count': (100, 150),
            'SYN Flag Count': (1, 3),
            'FIN Flag Count': (1, 3),
            'Destination Port': [21],
            'Down/Up Ratio': (0.88, 0.98)
        }
    },
    'DoS slowloris': {
        'count': 5,
        'priority_expected': 'MEDIUM',
        'pattern': {
            'Flow Duration': (50000, 100000),
            'Total Fwd Packets': (100, 500),
            'Total Backward Packets': (50, 400),
            'Flow Bytes/s': (1000, 5000),
            'Flow Packets/s': (2, 10),
            'Total Length of Fwd Packets': (10000, 50000),
            'Total Length of Bwd Packets': (5000, 40000),
            'Fwd Packet Length Mean': (80, 120),
            'Bwd Packet Length Mean': (85, 115),
            'Packet Length Std': (20, 40),
            'Flow IAT Mean': (100, 500),
            'Fwd IAT Mean': (150, 600),
            'Bwd IAT Mean': (200, 700),
            'PSH Flag Count': (20, 100),
            'SYN Flag Count': (1, 5),
            'FIN Flag Count': (0, 2),
            'Destination Port': [80, 443],
            'Down/Up Ratio': (0.4, 0.8)
        }
    }
}

def generate_value(pattern):
    """Generate a value based on pattern"""
    if isinstance(pattern, list):
        return random.choice(pattern)
    elif isinstance(pattern, tuple):
        return random.uniform(pattern[0], pattern[1])
    else:
        return pattern

# Generate alerts
alerts = []
alert_counter = 1

for attack_type, config in ATTACK_PATTERNS.items():
    for i in range(config['count']):
        alert = {
            'alert_id': f'ALERT-{attack_type.replace(" ", "")}-{i+1:03d}',
            'source_ip': f'{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}',
            'dest_ip': f'10.0.{random.randint(0, 255)}.{random.randint(1, 254)}',
            'timestamp': (datetime.now() - timedelta(hours=random.randint(0, 48))).isoformat(),
            'expected_attack': attack_type,
            'expected_priority': config['priority_expected']
        }
        
        # Generate features
        for feature in FEATURES:
            if feature in config['pattern']:
                alert[feature] = generate_value(config['pattern'][feature])
            else:
                alert[feature] = 0
        
        alerts.append(alert)

# Shuffle alerts
random.shuffle(alerts)

# Create DataFrame
df = pd.DataFrame(alerts)

# Save as CSV
csv_filename = 'test_alerts.csv'
df.to_csv(csv_filename, index=False)

print(f"\n✅ Generated {len(alerts)} test alerts")
print(f"\nAlert distribution:")
for attack_type, config in ATTACK_PATTERNS.items():
    print(f"  {attack_type:20s}: {config['count']:2d} alerts (Expected: {config['priority_expected']})")

print(f"\n📁 Saved to: {csv_filename}")

# Create JSON test cases for single alert testing
json_test_cases = {
    'test_cases': []
}

for attack_type in ['DDoS', 'PortScan', 'SSH-Patator']:
    sample = df[df['expected_attack'] == attack_type].iloc[0]
    
    test_case = {
        'name': f'{attack_type} Alert',
        'description': f'Test case for {attack_type} detection',
        'expected_priority': sample['expected_priority'],
        'request': {
            'alert_id': sample['alert_id'],
            'source_ip': sample['source_ip'],
            'dest_ip': sample['dest_ip'],
            'timestamp': sample['timestamp'],
            'features': {feat: float(sample[feat]) for feat in FEATURES}
        }
    }
    
    json_test_cases['test_cases'].append(test_case)

# Save JSON
json_filename = 'test_cases.json'
with open(json_filename, 'w') as f:
    json.dump(json_test_cases, f, indent=2)

print(f"📁 Saved JSON test cases to: {json_filename}")

print("\n" + "="*80)
print("HOW TO USE")
print("="*80)
print("\n1. Start your API:")
print("   python final_soc_api.py")
print("\n2. Test single alert (copy from test_cases.json):")
print("   curl -X POST http://localhost:8000/prioritize \\")
print("     -H 'Content-Type: application/json' \\")
print("     -d @test_cases.json")
print("\n3. Test CSV upload:")
print(f"   curl -X POST http://localhost:8000/prioritize/csv \\")
print(f"     -F 'file=@{csv_filename}'")
print("\n4. Or use the interactive docs:")
print("   http://localhost:8000/docs")

print("\n" + "="*80)
print("✅ TEST DATA READY!")
print("="*80)