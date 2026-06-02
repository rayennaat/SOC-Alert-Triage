# quick_extract.py
import pandas as pd

df = pd.read_csv("real_test_alerts.csv")

# Get the DDoS sample that worked
ddos = df[df['alert_id'] == 'ALERT-DDoS-006'].iloc[0]

FEATURES = [
    'Flow Duration', 'Total Fwd Packets', 'Total Backward Packets',
    'Flow Bytes/s', 'Flow Packets/s', 'Total Length of Fwd Packets',
    'Total Length of Bwd Packets', 'Fwd Packet Length Mean',
    'Bwd Packet Length Mean', 'Packet Length Std', 'Flow IAT Mean',
    'Fwd IAT Mean', 'Bwd IAT Mean', 'PSH Flag Count',
    'SYN Flag Count', 'FIN Flag Count', 'Destination Port', 'Down/Up Ratio'
]

print("Real DDoS Features:")
for feat in FEATURES:
    print(f"  {feat}: {ddos[feat]}")