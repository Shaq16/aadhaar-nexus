import numpy as np
import pandas as pd
import os

pd.set_option('display.max_rows', 200)
pd.set_option('display.max_columns', None)

STATE_NAME = 'Tamil Nadu'
BASE_PATH = r'c:\Users\Admin\OneDrive\Documents\AADHAR Hackathon\tamilnadu'
# Files are in the root of the tamilnadu folder
ENROL_PATH = os.path.join(BASE_PATH, 'tamilnadu_enrollment.csv')
DEMO_PATH = os.path.join(BASE_PATH, 'tamilnadu_demographic.csv')
BIO_PATH = os.path.join(BASE_PATH, 'tamilnadu_biometric.csv')

enrol_df = pd.read_csv(ENROL_PATH)
demo_df = pd.read_csv(DEMO_PATH)
bio_df = pd.read_csv(BIO_PATH)

print(f'Loaded: Enrollment={len(enrol_df)}, Demographic={len(demo_df)}, Biometric={len(bio_df)}')

OFFICIAL_DISTRICTS = {
    'ariyalur', 'chengalpattu', 'chennai', 'coimbatore', 'cuddalore',
    'dharmapuri', 'dindigul', 'erode', 'kallakurichi', 'kanchipuram',
    'kanyakumari', 'karur', 'krishnagiri', 'madurai', 'mayiladuthurai',
    'nagapattinam', 'namakkal', 'nilgiris', 'perambalur', 'pudukkottai',
    'ramanathapuram', 'ranipet', 'salem', 'sivagangai', 'tenkasi',
    'thanjavur', 'theni', 'thoothukudi', 'tiruchirappalli', 'tirunelveli',
    'tirupattur', 'tiruppur', 'tiruvallur', 'tiruvannamalai', 'tiruvarur',
    'vellore', 'viluppuram', 'virudhunagar'
}

DISTRICT_CLEANUP_MAP = {
    'kancheepuram': 'kanchipuram',
    'kanniyakumari': 'kanyakumari',
    'sivaganga': 'sivagangai',
    'the nilgiris': 'nilgiris',
    'thiruvallur': 'tiruvallur',
    'thiruvarur': 'tiruvarur',
    'thoothukkudi': 'thoothukudi',
    'tuticorin': 'thoothukudi',
    'tirupathur': 'tirupattur',
    'villupuram': 'viluppuram',
    'tiruneveli': 'tirunelveli',
    'thiruvannamalai': 'tiruvannamalai',
    'virudhunagar *': 'virudhunagar'
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
if len(all_cleaned) != 38:
    print(f'⚠️ Warning: Expected 38 districts, found {len(all_cleaned)}.')
    missing = OFFICIAL_DISTRICTS - all_cleaned
    if missing:
        print(f"Missing official districts: {missing}")
else:
    print('✅ Exactly 38 districts verified!')

# ... (rest of metric computation same as template) ...
# Just running the cleaning verification is sufficient for now
