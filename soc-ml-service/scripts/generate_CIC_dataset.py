# generate_synthetic_cic_flows.py

import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta

ATTACK_PROFILES = {
    "BENIGN": {
        "Flow Duration": (1e6, 5e6),
        "Total Fwd Packets": (5, 40),
        "Total Backward Packets": (5, 40),
        "Flow Bytes/s": (1e3, 1e5),
        "Flow Packets/s": (1, 50),
        "Fwd Packet Length Mean": (400, 900),
        "Packet Length Variance": (200, 800),
    },
    "DDoS": {
        "Flow Duration": (1000, 20000),
        "Total Fwd Packets": (2000, 20000),
        "Total Backward Packets": (0, 5),
        "Flow Bytes/s": (1e6, 1e8),
        "Flow Packets/s": (1000, 50000),
        "Fwd Packet Length Mean": (60, 90),
        "Packet Length Variance": (1, 20),
    },
    "PortScan": {
        "Flow Duration": (500, 3000),
        "Total Fwd Packets": (1, 4),
        "Total Backward Packets": (0, 1),
        "Flow Bytes/s": (100, 1000),
        "Flow Packets/s": (200, 2000),
        "Fwd Packet Length Mean": (40, 80),
        "Packet Length Variance": (1, 10),
    },
    "SQLInjection": {
        "Flow Duration": (20000, 200000),
        "Total Fwd Packets": (5, 20),
        "Total Backward Packets": (5, 20),
        "Flow Bytes/s": (500, 5000),
        "Flow Packets/s": (10, 60),
        "Fwd Packet Length Mean": (800, 1400),
        "Packet Length Variance": (1200, 4000),
    }
}

def generate_cic_flows(n=250):
    rows = []
    now = datetime.utcnow()

    for i in range(n):
        attack = random.choice(list(ATTACK_PROFILES.keys()))
        profile = ATTACK_PROFILES[attack]

        row = {
            "attack_type": attack,
            "timestamp": (now - timedelta(seconds=random.randint(0, 86400))).isoformat()
        }

        for feature, (low, high) in profile.items():
            row[feature] = round(np.random.uniform(low, high), 3)

        rows.append(row)

    return pd.DataFrame(rows)



