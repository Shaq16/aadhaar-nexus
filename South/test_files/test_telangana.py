import numpy as np
import pandas as pd
import os

pd.set_option('display.max_rows', 200)
pd.set_option('display.max_columns', None)

STATE_NAME = 'Telangana'
BASE_PATH = r'c:\Users\Admin\OneDrive\Documents\AADHAR Hackathon\telangana'
DATA_PATH = os.path.join(BASE_PATH, 'data')

# 1. Load Files
enrol_df = pd.read_csv(os.path.join(DATA_PATH, 'telangana_enrollment.csv'))
demo_df = pd.read_csv(os.path.join(DATA_PATH, 'telangana_demographic.csv'))
bio_df = pd.read_csv(os.path.join(DATA_PATH, 'telangana_biometric.csv'))

# 2. Load Extracted Data
tg_extracted_path = os.path.join(DATA_PATH, 'telangna_dist_in_andhra.csv')
if os.path.exists(tg_extracted_path):
    tg_extracted_df = pd.read_csv(tg_extracted_path)
    print(f'Loaded {len(tg_extracted_df)} records from extracted file.')
    
    # Merge
    if not tg_extracted_df.empty:
        ext_enrol = tg_extracted_df[tg_extracted_df['source_file'] == 'Enrollment'].drop(columns=['source_file'])
        ext_demo = tg_extracted_df[tg_extracted_df['source_file'] == 'Demographic'].drop(columns=['source_file'])
        ext_bio = tg_extracted_df[tg_extracted_df['source_file'] == 'Biometric'].drop(columns=['source_file'])
        
        enrol_df = pd.concat([enrol_df, ext_enrol], ignore_index=True)
        demo_df = pd.concat([demo_df, ext_demo], ignore_index=True)
        bio_df = pd.concat([bio_df, ext_bio], ignore_index=True)
else:
    print('Warning: Extracted Telangana file not found.')

print(f'Total: Enrollment={len(enrol_df)}, Demographic={len(demo_df)}, Biometric={len(bio_df)}')

OFFICIAL_DISTRICTS = {
    'adilabad', 'bhadradri kothagudem', 'hanumakonda', 'hyderabad', 'jagtial',
    'jangaon', 'jayashankar bhupalpally', 'jogulamba gadwal', 'kamareddy',
    'karimnagar', 'khammam', 'komaram bheem asifabad', 'mahabubabad',
    'mahabubnagar', 'mancherial', 'medak', 'medchal–malkajgiri', 'mulugu',
    'nagarkurnool', 'nalgonda', 'narayanpet', 'nirmal', 'nizamabad',
    'peddapalli', 'rajanna sircilla', 'rangareddy', 'sangareddy', 'siddipet',
    'suryapet', 'vikarabad', 'wanaparthy', 'warangal', 'yadadri bhuvanagiri'
}

DISTRICT_CLEANUP_MAP = {
    'warangal urban': 'hanumakonda', 'warangal (urban)': 'hanumakonda',
    'warangal rural': 'warangal', 'warangal (rural)': 'warangal',
    'bhadradri': 'bhadradri kothagudem',
    'jayashankar': 'jayashankar bhupalpally',
    'jogulamba': 'jogulamba gadwal',
    'komaram bheem': 'komaram bheem asifabad', 'komaram bheem asifaba': 'komaram bheem asifabad',
    'rajanna': 'rajanna sircilla',
    'yadadri': 'yadadri bhuvanagiri', 'yadadri bhuvanagi': 'yadadri bhuvanagiri',
    'jangaon.': 'jangaon',
    'jagitial': 'jagtial', # Typo fix
    'medchal-malkajgiri': 'medchal–malkajgiri', 
    'medchal?malkajgiri': 'medchal–malkajgiri',
    'medchalâ\x88\x92malkajgiri': 'medchal–malkajgiri',
    'medchalâ\x80\x93malkajgiri': 'medchal–malkajgiri',
    'medchal−malkajgiri': 'medchal–malkajgiri', # U+2212 Minus Sign
    'medchal malkajgiri': 'medchal–malkajgiri', # Space fix
    'k.v. rangareddy': 'rangareddy',
    'k.v.rangareddy': 'rangareddy',
    'ranga reddy': 'rangareddy', # Space fix
    'rangareddi': 'rangareddy', # i ending
    'jangoan': 'jangaon', # Typo fix
    'mahabub nagar': 'mahabubnagar', 'mahbubnagar': 'mahabubnagar',
    'karim nagar': 'karimnagar'
}

def clean_district_name(name):
    if pd.isna(name): return None
    cleaned = str(name).strip().lower()
    if cleaned.endswith(' *'): cleaned = cleaned[:-2].strip()
    if cleaned.endswith('*'): cleaned = cleaned[:-1].strip()
    if cleaned.endswith('.'): cleaned = cleaned[:-1].strip()
    if cleaned in DISTRICT_CLEANUP_MAP: cleaned = DISTRICT_CLEANUP_MAP[cleaned]
    return cleaned

total_dropped = 0
for df in [enrol_df, demo_df, bio_df]:
    df['district_clean'] = df['district'].apply(clean_district_name)
    
    # Check what would be dropped
    # Handle dash fuzzy match just for validation print
    # Official set for faster lookup
    official_norm = {d.replace('–', '-') for d in OFFICIAL_DISTRICTS}
    
    # If clean name is NOT in official districts
    unknowns = []
    for d, clean_d in zip(df['district'], df['district_clean']):
         if pd.notna(clean_d):
             norm_clean = clean_d.replace('–', '-')
             if norm_clean not in official_norm:
                 if clean_d not in OFFICIAL_DISTRICTS: # Double check exact
                     unknowns.append(clean_d)
                     
    unknowns = list(set(unknowns))
    
    if len(unknowns) > 0:
        print(f"⚠️ Warning: These districts would be dropped: {unknowns}")
        total_dropped += len(unknowns)
        
    df.dropna(subset=['district_clean'], inplace=True)
    df['district'] = df['district_clean']
    df.drop(columns=['district_clean'], inplace=True)

if total_dropped == 0:
    print("✅ Success: No districts dropped!")
else:
    print(f"❌ Failure: {total_dropped} unmapped districts found.")

all_cleaned = set(enrol_df['district'].unique()) | set(demo_df['district'].unique()) | set(bio_df['district'].unique())
# Handle dash again for printing sorting
print(f'Final Districts ({len(all_cleaned)}):') # Just print count and list

if len(all_cleaned) != 33:
    print(f'⚠️ Warning: Expected 33 districts, found {len(all_cleaned)}.')
    diff = all_cleaned - OFFICIAL_DISTRICTS
    if diff:
        print(f"❌ EXTRA DISTRICTS FOUND: {diff}")
        print(f"Missing official districts: {OFFICIAL_DISTRICTS - all_cleaned}")
else:
    print('✅ Exactly 33 districts verified!')
