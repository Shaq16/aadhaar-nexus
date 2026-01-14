import numpy as np
import pandas as pd
import os

pd.set_option('display.max_rows', 200)
pd.set_option('display.max_columns', None)

STATE_NAME = 'Karnataka'
BASE_PATH = r'c:\Users\Admin\OneDrive\Documents\AADHAR Hackathon\karnataka'
DATA_PATH = os.path.join(BASE_PATH, 'data')

enrol_df = pd.read_csv(os.path.join(DATA_PATH, 'karnataka_enrollment.csv'))
demo_df = pd.read_csv(os.path.join(DATA_PATH, 'karnataka_demographic.csv'))
bio_df = pd.read_csv(os.path.join(DATA_PATH, 'karnataka_biometric.csv'))

print(f'Loaded: Enrollment={len(enrol_df)}, Demographic={len(demo_df)}, Biometric={len(bio_df)}')

OFFICIAL_DISTRICTS = {
    'bagalkote', 'ballari', 'belagavi', 'bengaluru rural', 'bengaluru urban',
    'bidar', 'chamarajanagar', 'chikkaballapura', 'chikkamagaluru', 'chitradurga',
    'dakshina kannada', 'davanagere', 'dharwad', 'gadag', 'hassan', 'haveri',
    'kalaburagi', 'kodagu', 'kolar', 'koppal', 'mandya', 'mysuru', 'raichur',
    'ramanagara', 'shivamogga', 'tumakuru', 'udupi', 'uttara kannada',
    'vijayanagara', 'vijayapura', 'yadgir'
}

DISTRICT_CLEANUP_MAP = {
    'hasan': 'hassan',
    'davangere': 'davanagere',
    'bagalkot': 'bagalkote',
    'bellary': 'ballari',
    'belgaum': 'belagavi',
    'bangalore': 'bengaluru urban',
    'bangalore urban': 'bengaluru urban',
    'bengaluru': 'bengaluru urban',
    'bengaluru south': 'bengaluru urban',
    'bengaluru north': 'bengaluru urban',
    'bengaluru central': 'bengaluru urban',
    'bengaluru east': 'bengaluru urban',
    'bengaluru west': 'bengaluru urban',
    'bangalore rural': 'bengaluru rural',
    'chamrajnagar': 'chamarajanagar',
    'chamrajanagar': 'chamarajanagar',
    'chamarajanagara': 'chamarajanagar',
    'chikkaballapur': 'chikkaballapura',
    'chikmagalur': 'chikkamagaluru',
    'chickmagalur': 'chikkamagaluru',
    'gulbarga': 'kalaburagi',
    'mysore': 'mysuru',
    'ramanagar': 'ramanagara',
    'shimoga': 'shivamogga',
    'tumkur': 'tumakuru',
    'bijapur': 'vijayapura',
    'bijapur(kar)': 'vijayapura',
}

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
    
    # Check what would be dropped
    dropped = df[~df['district_clean'].isin(OFFICIAL_DISTRICTS)]['district'].unique()
    if len(dropped) > 0:
        print(f"⚠️ Warning: These districts would be dropped: {dropped}")
        total_dropped += len(dropped)
        
    df.dropna(subset=['district_clean'], inplace=True)
    df['district'] = df['district_clean']
    df.drop(columns=['district_clean'], inplace=True)
    df['date'] = pd.to_datetime(df['date'], dayfirst=True)
    df['month'] = df['date'].dt.month

if total_dropped == 0:
    print("✅ Success: No districts dropped!")
else:
    print(f"❌ Failure: {total_dropped} unmapped districts found.")

all_cleaned = set(enrol_df['district'].unique()) | set(demo_df['district'].unique()) | set(bio_df['district'].unique())
print(f'Final Districts ({len(all_cleaned)}): {sorted(all_cleaned)}')
if len(all_cleaned) != 31:
    print(f'⚠️ Warning: Expected 31 districts, found {len(all_cleaned)}.')
else:
    print('✅ Exactly 31 districts verified!')
