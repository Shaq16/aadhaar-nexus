import numpy as np
import pandas as pd
import os

pd.set_option('display.max_rows', 200)
pd.set_option('display.max_columns', None)

STATE_NAME = 'Andhra Pradesh'
BASE_PATH = r'c:\Users\Admin\OneDrive\Documents\AADHAR Hackathon\andhra'
DATA_PATH = os.path.join(BASE_PATH, 'data')

enrol_df = pd.read_csv(os.path.join(DATA_PATH, 'andhra_enrollment.csv'))
demo_df = pd.read_csv(os.path.join(DATA_PATH, 'andhra_demographic.csv'))
bio_df = pd.read_csv(os.path.join(DATA_PATH, 'andhra_biometric.csv'))

print(f'Loaded: Enrollment={len(enrol_df)}, Demographic={len(demo_df)}, Biometric={len(bio_df)}')

OFFICIAL_ANDHRA_DISTRICTS = {
    'alluri sitharama raju', 'anakapalli', 'ananthapuramu', 'annamayya',
    'bapatla', 'chittoor', 'dr. b.r. ambedkar konaseema', 'east godavari',
    'eluru', 'guntur', 'kakinada', 'krishna', 'kurnool', 'nandyal',
    'ntr', 'palnadu', 'parvathipuram manyam', 'prakasam',
    'sri potti sriramulu nellore', 'sri sathya sai', 'srikakulam',
    'tirupati', 'visakhapatnam', 'vizianagaram', 'west godavari',
    'y.s.r. kadapa'
}

TELANGANA_DISTRICTS = {
    'adilabad', 'hyderabad', 'karimnagar', 'khammam', 'mahabubnagar',
    'medak', 'nalgonda', 'nizamabad', 'rangareddy', 'warangal',
    'k.v.rangareddy', 'mahabub nagar', 'karim nagar'
}

DISTRICT_CLEANUP_MAP = {
    'anantapur': 'ananthapuramu', 'ananthapur': 'ananthapuramu',
    'cuddapah': 'y.s.r. kadapa', 'y. s. r': 'y.s.r. kadapa',
    'dr. b. r. ambedkar konaseema': 'dr. b.r. ambedkar konaseema',
    'n. t. r': 'ntr',
    'nellore': 'sri potti sriramulu nellore', 'spsr nellore': 'sri potti sriramulu nellore',
    'visakhapatanam': 'visakhapatnam',
    'k.v. rangareddy': 'rangareddy', 'k.v.rangareddy': 'rangareddy',
    'rangareddi': 'rangareddy', 'karim nagar': 'karimnagar',
    'mahabub nagar': 'mahabubnagar', 'mahbubnagar': 'mahabubnagar'
}

def normalize_name(name):
    if pd.isna(name): return None
    cleaned = str(name).strip().lower()
    if cleaned.endswith(' *'): cleaned = cleaned[:-2].strip()
    if cleaned.endswith('*'): cleaned = cleaned[:-1].strip()
    if cleaned in DISTRICT_CLEANUP_MAP: cleaned = DISTRICT_CLEANUP_MAP[cleaned]
    return cleaned

telangana_data = []

for df_name, df in [('Enrollment', enrol_df), ('Demographic', demo_df), ('Biometric', bio_df)]:
    df['district_norm'] = df['district'].apply(normalize_name)
    
    # 1. Check Telangana
    tg_mask = df['district_norm'].isin(TELANGANA_DISTRICTS)
    tg_count = tg_mask.sum()
    if tg_count > 0:
        telangana_data.append(df[tg_mask])
    
    # 2. Check Unmapped
    df['is_andhra'] = df['district_norm'].isin(OFFICIAL_ANDHRA_DISTRICTS)
    
    # Identify what is neither Andhra nor Telangana
    unknowns = df[(~tg_mask) & (~df['is_andhra'])]['district'].unique()
    if len(unknowns) > 0:
        print(f"⚠️ Warning: Found districts neither AP nor TG in {df_name}: {unknowns}")
    
    df.query('is_andhra == True', inplace=True)
    df['district'] = df['district_norm']
    df.drop(columns=['district_norm', 'is_andhra'], inplace=True)
    df['date'] = pd.to_datetime(df['date'], dayfirst=True)
    df['month'] = df['date'].dt.month

# Verify Telangana Extraction
total_tg = sum([len(x) for x in telangana_data]) if telangana_data else 0
print(f"Telangana Records Extracted: {total_tg}")
if total_tg > 0:
    print("✅ Telangana separation working.")
else:
    print("⚠️ Warning: No Telangana records extracted (check if expected).")

# Verify Andhra Counts
all_cleaned = set(enrol_df['district'].unique()) | set(demo_df['district'].unique()) | set(bio_df['district'].unique())
print(f'Final Andhra Districts ({len(all_cleaned)}): {sorted(all_cleaned)}')

if len(all_cleaned) != 26:
    print(f'⚠️ Warning: Expected 26 districts, found {len(all_cleaned)}.')
    missing = OFFICIAL_ANDHRA_DISTRICTS - all_cleaned
    if missing:
        print(f"Missing official districts: {missing}")
else:
    print('✅ Exactly 26 Andhra districts verified!')
