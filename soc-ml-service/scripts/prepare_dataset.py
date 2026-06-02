# prepare_dataset.py
import pandas as pd
import os

# ----------------------------
# CONFIGURATION
# ----------------------------
# Folder containing the MachineLearningCSV extracted files
folder = "data"  # current folder
output_file = "merged_cleaned.csv"

# Minimum threshold to keep columns (drop columns with >50% missing)
min_col_threshold = 0.5

# ----------------------------
# HELPER FUNCTIONS
# ----------------------------
def clean_dataframe(df):
    """Cleans a single dataframe."""
    # Replace NA / inf values
    df = df.replace([pd.NA, float("inf"), float("-inf")], 0)
    
    # Drop columns with too many missing values
    df = df.dropna(axis=1, thresh=len(df) * min_col_threshold)
    
    # Strip column names
    df.columns = df.columns.str.strip()
    
    # Keep only rows with valid labels
    df = df[df["Label"].notna()]
    
    return df

# ----------------------------
# MAIN SCRIPT
# ----------------------------
dfs = []
files = [f for f in os.listdir(folder) if f.endswith(".csv")]

print(f"Found {len(files)} CSV files in folder '{folder}'")

for file in files:
    print(f"\n📌 Checking: {file}")
    
    try:
        # Read first few rows to check columns
        df_sample = pd.read_csv(file, nrows=5, encoding='utf-8-sig')
        df_sample.columns = df_sample.columns.str.strip()
    except Exception as e:
        print(f"⚠️ Skipping {file}: cannot read CSV ({e})")
        continue
    
    if "Label" not in df_sample.columns:
        print(f"❌ Skipping {file}: no Label column")
        continue
    
    print(f"✔️ Loading full CSV: {file}")
    try:
        df = pd.read_csv(file, low_memory=False, encoding='utf-8-sig')
        df.columns = df.columns.str.strip()
        df = clean_dataframe(df)
        dfs.append(df)
        print(f"✅ {file} added with {len(df)} rows")
    except Exception as e:
        print(f"⚠️ Failed to load {file}: {e}")
        continue

# Merge all valid dataframes
if len(dfs) == 0:
    raise Exception("❌ ERROR: No CSV files with 'Label' found!")

merged = pd.concat(dfs, ignore_index=True)
merged.to_csv(output_file, index=False)

print(f"\n🎉 DONE! Created '{output_file}' with {len(merged)} rows")
