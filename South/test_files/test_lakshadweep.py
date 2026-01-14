import numpy as np
import pandas as pd
import os

pd.set_option('display.max_rows', 200)
pd.set_option('display.max_columns', None)

STATE_NAME = 'Lakshadweep'
BASE_PATH = r'c:\Users\Admin\OneDrive\Documents\AADHAR Hackathon\lakshadweep'
# Files in root for this state
DATA_PATH = BASE_PATH 

enrol_df = pd.read_csv(os.path.join(DATA_PATH, 'lakshwadeep_enrollment.csv'))
demo_df = pd.read_csv(os.path.join(DATA_PATH, 'lakshwadeep_demographic.csv'))
bio_df = pd.read_csv(os.path.join(DATA_PATH, 'lakshwadeep_biometric.csv'))

print(f'Loaded: Enrollment={len(enrol_df)}, Demographic={len(demo_df)}, Biometric={len(bio_df)}')

OFFICIAL_DISTRICTS = {'lakshadweep'}
DISTRICT_CLEANUP_MAP = {}

def clean_district_name(name):
    if pd.isna(name): return None
    cleaned = str(name).strip().lower()
    if cleaned.endswith(' *'): cleaned = cleaned[:-2].strip()
    if cleaned.endswith('*'): cleaned = cleaned[:-1].strip()
    if cleaned in DISTRICT_CLEANUP_MAP: cleaned = DISTRICT_CLEANUP_MAP[cleaned]
    return cleaned

total_dropped = 0
for df in [enrol_df, demo_df, bio_df]:
    df['district_clean'] = df['district'].apply(clean_district_name)
    
    dropped = df[~df['district_clean'].isin(OFFICIAL_DISTRICTS)]['district'].unique()
    if len(dropped) > 0:
        print(f"⚠️ Warning: These districts would be dropped: {dropped}")
        total_dropped += len(dropped)
        
    df.dropna(subset=['district_clean'], inplace=True)
    df['district'] = df['district_clean']
    df.drop(columns=['district_clean'], inplace=True)

if total_dropped == 0:
    print("✅ Success: No districts dropped!")
else:
    print(f"❌ Failure: {total_dropped} unmapped districts found.")

all_cleaned = set(enrol_df['district'].unique()) | set(demo_df['district'].unique()) | set(bio_df['district'].unique())
print(f'Final Districts ({len(all_cleaned)}): {sorted(all_cleaned)}')
if len(all_cleaned) != 1:
    print(f'⚠️ Warning: Expected 1 district, found {len(all_cleaned)}.')
else:
    print('✅ Exactly 1 district verified!')
