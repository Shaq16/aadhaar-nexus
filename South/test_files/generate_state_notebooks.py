import json
import os

# Configuration
STATES = [
    "andaman", "andhra", "goa", "karnataka", 
    "kerala", "lakshadweep", "tamilnadu", "telangana"
]
BASE_DIR = r"c:\Users\Admin\OneDrive\Documents\AADHAR Hackathon"

def create_notebook_content(state_name):
    title_state = state_name.title()
    
    # Define the code cells
    cells = []
    
    # 1. Imports
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import numpy as np\n",
            "import pandas as pd\n",
            "from glob import glob\n",
            "import matplotlib.pyplot as plt\n",
            "from sklearn.preprocessing import MinMaxScaler\n",
            "\n",
            "pd.set_option(\"display.max_rows\", 2000)\n",
            "pd.set_option(\"display.max_columns\", None)"
        ]
    })
    
    # 2. Load Data
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            f"state_name = '{state_name}'\n",
            f"base_path = r'{BASE_DIR}'\n",
            f"state_path = f'{{base_path}}\\{{state_name}}'\n",
            "\n",
            "# Construct file paths - handling potential naming variations\n",
            "def find_file(pattern):\n",
            "    files = glob(f'{state_path}\\{pattern}')\n",
            "    if not files:\n",
            "        # Try adding state prefix if not found directly\n",
            "        files = glob(f'{state_path}\\{state_name}_{pattern}')\n",
            "    if not files:\n",
            "        # Special case for lakshadweep spelling\n",
            "        if state_name == 'lakshadweep':\n",
            "            files = glob(f'{state_path}\\lakshwadeep_{pattern}')\n",
            "        # Special name for Andaman\n",
            "        if state_name == 'andaman':\n",
            "             files = glob(f'{state_path}\\andaman_1_{pattern}')\n",
            "\n",
            "    if files:\n",
            "        return files[0]\n",
            "    return None\n",
            "\n",
            "enrol_path = find_file('*enrollment.csv')\n",
            "demo_path = find_file('*demographic.csv')\n",
            "bio_path = find_file('*biometric.csv')\n",
            "\n",
            "print(f'Loading files for {{state_name}}:')\n",
            "print(f'Enrollment: {{enrol_path}}')\n",
            "print(f'Demographic: {{demo_path}}')\n",
            "print(f'Biometric: {{bio_path}}')\n",
            "\n",
            "enrol_df = pd.read_csv(enrol_path)\n",
            "demo_df = pd.read_csv(demo_path)\n",
            "bio_df = pd.read_csv(bio_path)\n",
            "all_dfs = [enrol_df, demo_df, bio_df]"
        ]
    })
    
    # 3. Data Cleaning & Standardization
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Date Parsing\n",
            "enrol_df['date'] = pd.to_datetime(enrol_df['date'], dayfirst=True)\n",
            "demo_df['date'] = pd.to_datetime(demo_df['date'], dayfirst=True)\n",
            "bio_df['date'] = pd.to_datetime(bio_df['date'], dayfirst=True)\n",
            "\n",
            "# District Name Cleanup Map (from UP Analysis)\n",
            "cleanup_map = {\n",
            "    \"Ambedkar Nagar *\": \"Ambedkar Nagar\",\n",
            "    \"Gautam Buddh Nagar\": \"Gautam Buddha Nagar\",\n",
            "    \"Auraiya *\": \"Auraiya\",\n",
            "    \"Chandauli *\": \"Chandauli\",\n",
            "    \"Chitrakoot *\": \"Chitrakoot\",\n",
            "    \"Gautam Buddha Nagar *\": \"Gautam Buddh Nagar\",\n",
            "    \"Jyotiba Phule Nagar *\": \"Amroha\",\n",
            "    \"Mahoba *\": \"Mahoba\",\n",
            "    \"Sant Kabir Nagar *\": \"Sant Kabir Nagar\",\n",
            "    \"Baghpat *\": \"Baghpat\",\n",
            "    \"Chandauli *\": \"Chandauli\",\n",
            "    \"Allahabad\": \"Prayagraj\",\n",
            "    \"Faizabad\": \"Ayodhya\",\n",
            "    \"Jyotiba Phule Nagar\": \"Amroha\",\n",
            "    \"Bara Banki\": \"Barabanki\",\n",
            "    \"Bulandshahar\": \"Bulandshahr\",\n",
            "    \"Kushi Nagar\": \"Kushinagar\",\n",
            "    \"Kushinagar *\": \"Kushinagar\",\n",
            "    \"Rae Bareli\": \"Raebareli\",\n",
            "    \"Siddharth Nagar\": \"Siddharthnagar\",\n",
            "    \"Shravasti\": \"Shrawasti\",\n",
            "    \"Mahrajganj\": \"Maharajganj\",\n",
            "    \"Bagpat\": \"Baghpat\",\n",
            "    \"Sant Ravidas Nagar\": \"Bhadohi\",\n",
            "    \"Sant Ravidas Nagar Bhadohi\": \"Bhadohi\",\n",
            "    # Add any state-specific cleanup here if discovered\n",
            "    \"Bijapur(KAR)\": \"Vijayapura\" # Known check for Karnataka\n",
            "}\n",
            "\n",
            "for df in all_dfs:\n",
            "    # Standardize District Names\n",
            "    df['district'] = df['district'].replace(cleanup_map)\n",
            "    df['district'] = df['district'].str.strip().str.lower()\n",
            "    \n",
            "    # Extract Month\n",
            "    df['month'] = df['date'].dt.month\n",
            "\n",
            "print('District Counts:')\n",
            "print(enrol_df['district'].nunique(), demo_df['district'].nunique(), bio_df['district'].nunique())"
        ]
    })
    
    # 4. Aggregation & Merging
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Aggregate by District and Month\n",
            "enrol_agg = enrol_df.groupby(['state', 'district', 'month'])[['age_0_5', 'age_5_17', 'age_18_greater']].sum().reset_index()\n",
            "demo_agg = demo_df.groupby(['state', 'district', 'month'])[['demo_age_5_17', 'demo_age_17_']].sum().reset_index()\n",
            "bio_agg = bio_df.groupby(['state', 'district', 'month'])[['bio_age_5_17', 'bio_age_17_']].sum().reset_index()\n",
            "\n",
            "# Merge Datasets\n",
            "combined_df = enrol_agg.merge(demo_agg, on=['state', 'district', 'month'], how='left') \\\n",
            "                       .merge(bio_agg, on=['state', 'district', 'month'], how='left')\n",
            "\n",
            "# Impute Missing Values with 0\n",
            "combined_df.fillna(0, inplace=True)\n",
            "combined_df.head()"
        ]
    })
    
    # 5. Base Metric Calculation
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Calculate Core Metrics\n",
            "combined_df['E'] = combined_df['age_0_5'] + combined_df['age_5_17'] + combined_df['age_18_greater']\n",
            "combined_df['DU'] = combined_df['demo_age_5_17'] + combined_df['demo_age_17_']\n",
            "combined_df['BU'] = combined_df['bio_age_5_17'] + combined_df['bio_age_17_']\n",
            "combined_df['U'] = combined_df['DU'] + combined_df['BU']\n",
            "combined_df['T'] = combined_df['E'] + combined_df['U']\n",
            "\n",
            "combined_df.head()"
        ]
    })
    
    # 6. Activity Analysis
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Monthly Activity Analysis\n",
            "district_monthly_counts = combined_df.groupby(['district', 'month']).agg(\n",
            "    total_months=('month', 'count'), \n",
            "    active_months=('T', lambda x: (x > 0).sum())\n",
            ").reset_index()\n",
            "\n",
            "district_monthly_counts['zero_months'] = district_monthly_counts['total_months'] - district_monthly_counts['active_months']\n",
            "district_monthly_counts['activity_ratio'] = district_monthly_counts['active_months'] / district_monthly_counts['total_months']\n",
            "district_monthly_counts['zero_month_ratio'] = district_monthly_counts['zero_months'] / district_monthly_counts['total_months']\n",
            "\n",
            "# Merge back activity ratios\n",
            "combined_df = combined_df.merge(\n",
            "    district_monthly_counts[['district', 'month', 'activity_ratio', 'zero_month_ratio']], \n",
            "    on=['district', 'month'], \n",
            "    how='left'\n",
            ")\n",
            "combined_df.head()"
        ]
    })
    
    # 7. Volume & Volatility Metrics
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Calculate Volume and Volatility Metrics per District\n",
            "district_volume_metrics = combined_df.groupby(['state', 'district']).agg(\n",
            "    avg_monthly_enrolment=('E', 'mean'),\n",
            "    monthly_valatility=('T', lambda x: x.std(ddof=0) / x.mean() if x.mean() > 0 else 0),\n",
            "    peak_load_ratio=('T', lambda x: x.max() / x.mean() if x.mean() > 0 else 0)\n",
            ").reset_index()\n",
            "\n",
            "combined_df = combined_df.merge(district_volume_metrics, on=['state', 'district'], how='left')\n",
            "combined_df.head()"
        ]
    })
    
    # 8. Update Burden Metrics
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Calculate Update Burden Metrics per District\n",
            "district_update_burden = combined_df.groupby(['state', 'district']).agg(\n",
            "    avg_monthly_enrollments=('E', 'sum'), \n",
            "    avg_monthly_demo_updates=('DU', 'sum'), \n",
            "    avg_monthly_bio_updates=('BU', 'sum')\n",
            ").reset_index()\n",
            "\n",
            "district_update_burden['U'] = district_update_burden['avg_monthly_demo_updates'] + district_update_burden['avg_monthly_bio_updates']\n",
            "district_update_burden['biometric_burden'] = district_update_burden['avg_monthly_bio_updates'] / (district_update_burden['avg_monthly_bio_updates'] + district_update_burden['avg_monthly_demo_updates'])\n",
            "district_update_burden['update_dominant'] = np.where(district_update_burden['U'] > district_update_burden['avg_monthly_enrollments'], 1, 0)\n",
            "district_update_burden['enrollment_update_balance'] = district_update_burden['avg_monthly_enrollments'] / (district_update_burden['avg_monthly_enrollments'] + district_update_burden['U'])\n",
            "\n",
            "# Fill potential NaNs from division by zero\n",
            "district_update_burden.fillna(0, inplace=True)\n",
            "\n",
            "combined_df = combined_df.merge(\n",
            "    district_update_burden[['state', 'district', 'biometric_burden', 'update_dominant', 'enrollment_update_balance']], \n",
            "    on=['state', 'district'], \n",
            "    how='left'\n",
            ")\n",
            "combined_df.head()"
        ]
    })
    
    # 9. Collapse to District Level
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Collapse to District Level (taking the first row since metrics are identical for the district)\n",
            "# Note: We keep the monthly columns but they will represent a snapshot. The actual district-level metrics \n",
            "# (avg_monthly, volatility, etc.) are already computed and joined.\n",
            "district_summary_df = combined_df.groupby(['state', 'district'], as_index=False).first()\n",
            "\n",
            "# Recalculate component basics that depend on Sums if needed, or use the pre-calculated ones.\n",
            "# The UP notebook approach used the 'first' of the merged df which contains the specific month's data for Age/E/DU/BU\n",
            "# BUT the score metrics (monthly_volatility etc) are correct.\n",
            "# HOWEVER, 'Inclusion' and 'Responsiveness' need SUMS over the period, not single month.\n",
            "# Let's recalculate those specifically using the 'district_update_burden' sums we made.\n",
            "\n",
            "# We need Sums of Age breakdown for Inclusion. Let's create a quick agg for that.\n",
            "age_sums = combined_df.groupby(['state', 'district'])[['age_0_5', 'age_5_17']].sum().reset_index()\n",
            "age_sums.rename(columns={'age_0_5': 'sum_age_0_5', 'age_5_17': 'sum_age_5_17'}, inplace=True)\n",
            "\n",
            "district_summary_df = district_summary_df.merge(age_sums, on=['state', 'district'])\n",
            "\n",
            "district_summary_df.head()"
        ]
    })
    
    # 10. Normalization & Scoring
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def normalize(x):\n",
            "    maxx, minx = x.max(), x.min()\n",
            "    if maxx == minx:\n",
            "        return x * 0 + 0.5\n",
            "    normalized = (x - minx) / (maxx - minx)\n",
            "    return normalized\n",
            "\n",
            "def inverse_normalize(x):\n",
            "    inversed = 1 - normalize(x)\n",
            "    return inversed\n",
            "\n",
            "# --- Component Calculations ---\n",
            "\n",
            "# Access: Activity Ratio + Normalized Avg Enrollment\n",
            "district_summary_df['access'] = (district_summary_df['activity_ratio'] + normalize(district_summary_df['avg_monthly_enrolment'])) / 2\n",
            "\n",
            "# Responsiveness: updates / total_activity (Using the district-wide burden U vs T implicit logic, or re-sum)\n",
            "# Logic: normalize( U / (E+U) )\n",
            "# We have district_update_burden['U'] and 'avg_monthly_enrollments' (which is sum E)\n",
            "# Rename for clarity before merge\n",
            "burden_subset = district_update_burden[['state', 'district', 'U', 'avg_monthly_enrollments']].rename(columns={'U': 'U_sum', 'avg_monthly_enrollments': 'avg_monthly_enrollments_sum'})\n",
            "district_summary_df = district_summary_df.merge(burden_subset, on=['state', 'district'])\n",
            "\n",
            "district_summary_df['T_sum'] = district_summary_df['avg_monthly_enrollments_sum'] + district_summary_df['U_sum']\n",
            "district_summary_df['responsiveness'] = normalize(district_summary_df['U_sum'] / district_summary_df['T_sum'])\n",
            "\n",
            "# Inclusion: (age_0_5 + age_5_17) / E\n",
            "district_summary_df['inclusion'] = normalize((district_summary_df['sum_age_0_5'] + district_summary_df['sum_age_5_17']) / district_summary_df['avg_monthly_enrollments_sum'])\n",
            "\n",
            "# Stability: Inverse Volatility + Inverse Peak Load\n",
            "district_summary_df['stability'] = (inverse_normalize(district_summary_df['monthly_valatility']) + inverse_normalize(district_summary_df['peak_load_ratio'])) / 2\n",
            "\n",
            "# Visibility: Activity Ratio\n",
            "district_summary_df['visibility'] = district_summary_df['activity_ratio']\n",
            "\n",
            "# --- Final Scores ---\n",
            "\n",
            "district_summary_df['DEI'] = (district_summary_df['access'] + district_summary_df['responsiveness'] + district_summary_df['inclusion'] + district_summary_df['stability'] + district_summary_df['visibility']) / 5\n",
            "\n",
            "district_summary_df['ASS'] = (inverse_normalize(district_summary_df['activity_ratio']) + inverse_normalize(district_summary_df['avg_monthly_enrolment'])) / 2\n",
            "district_summary_df['UBS'] = (normalize(district_summary_df['biometric_burden']) + normalize(district_summary_df['update_dominant'])) / 2\n",
            "district_summary_df['SRS'] = (normalize(district_summary_df['monthly_valatility']) + normalize(district_summary_df['zero_month_ratio'])) / 2\n",
            "\n",
            "district_summary_df.head()"
        ]
    })
    
    # 11. Save Outputs
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            f"# Save outputs for {{title_state}}\n",
            f"output_path_full = fr'{{state_path}}\\\\{{state_name}}_district_analysis.csv'\n",
            f"output_path_scores = fr'{{state_path}}\\\\{{state_name}}_district_final_scores.csv'\n",
            "\n",
            "district_summary_df.to_csv(output_path_full, index=False)\n",
            "\n",
            "final_df = district_summary_df[['state', 'district', 'DEI', 'ASS', 'UBS', 'SRS']]\n",
            "final_df.to_csv(output_path_scores, index=False)\n",
            "\n",
            "print(f'Saved analysis to {{output_path_full}}')\n",
            "print(f'Saved scores to {{output_path_scores}}')"
        ]
    })
    
    # Construct Notebook JSON
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.5"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    return notebook

def generate_notebooks():
    for state in STATES:
        print(f"Generating notebook for {state}...")
        nb_content = create_notebook_content(state)
        
        # Ensure state directory exists (it should, but good practice)
        state_dir = os.path.join(BASE_DIR, state)
        if not os.path.exists(state_dir):
            print(f"Warning: Directory {state_dir} does not exist. Skipping.")
            continue
            
        nb_path = os.path.join(state_dir, f"{state}_analysis.ipynb")
        
        with open(nb_path, 'w', encoding='utf-8') as f:
            json.dump(nb_content, f, indent=2)
            
        print(f"Created {nb_path}")

if __name__ == "__main__":
    generate_notebooks()
