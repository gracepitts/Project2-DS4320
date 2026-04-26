# -*- coding: utf-8 -*-
"""load_and_clean_data.ipynb"""

# The raw clinical trials dataset used for this project is available below:
https://myuva-my.sharepoint.com/:x:/g/personal/twg3sr_virginia_edu/IQA_f_kXzTXaSaenQThz6DxGAaHsA3ArD3IfAtOUxlQ7N1s?e=IkpVkY 
# After downloading, upload the file to your working directory and run the notebook. 

import logging

# Set up logging to track execution and debugging
# This helps with reproducibility and identifying issues if errors occur
logging.basicConfig(
    filename="load_and_clean_data.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True
)

logging.info("Load and clean data notebook started")
print("Logging set up successfully.")

import pandas as pd

# Load raw clinical trials data
# on_bad_lines="skip" prevents malformed rows from crashing the script
df = pd.read_csv(
    "/content/clin_trials.csv",
    engine="python",
    on_bad_lines="skip"
)

# Clean column names by removing extra whitespace
df.columns = df.columns.str.strip()

print(df.shape)
print(df.columns.tolist())

# Standardize categorical variables for consistency
# Try/except ensures the script doesn't break if columns are missing or malformed
try:
    if "Overall Status" in df.columns:
        df["Overall Status"] = df["Overall Status"].str.upper()

    if "Phases" in df.columns:
        df["Phases"] = df["Phases"].str.upper().replace({"": "UNKNOWN"})

    if "Study Type" in df.columns:
        df["Study Type"] = df["Study Type"].str.title()

    if "Primary Purpose" in df.columns:
        df["Primary Purpose"] = df["Primary Purpose"].str.title()

    logging.info("Categorical fields standardized successfully")

except Exception as e:
    # Log the error and stop execution so it can be fixed
    print("Error standardizing categorical fields:", e)
    logging.error(f"Categorical standardization failed: {e}")
    raise

# Repeat standardization to ensure consistency
if "Overall Status" in df.columns:
    df["Overall Status"] = df["Overall Status"].str.upper()

if "Phases" in df.columns:
    df["Phases"] = df["Phases"].str.upper().replace({"": "UNKNOWN"})

if "Study Type" in df.columns:
    df["Study Type"] = df["Study Type"].str.title()

if "Primary Purpose" in df.columns:
    df["Primary Purpose"] = df["Primary Purpose"].str.title()

# Create unique IDs and derived variables
# "success" is defined as trials with status COMPLETED
df = df.reset_index(drop=True)
df["trial_id"] = df.index + 1
df["success"] = df["Overall Status"].apply(lambda x: 1 if x == "COMPLETED" else 0)

# Parse start date and extract year for analysis
df["start_date_parsed"] = pd.to_datetime(df["Start Date"], errors="coerce")
df["start_year"] = df["start_date_parsed"].dt.year

# Create clinical_trials table with core trial information
clinical_trials = df[[
    "trial_id",
    "Brief Title",
    "Full Title",
    "Overall Status",
    "Study Type",
    "Phases",
    "Primary Purpose",
    "Start Date",
    "Outcome Measure",
    "success"
]].copy()

clinical_trials.columns = [
    "trial_id",
    "brief_title",
    "full_title",
    "overall_status",
    "study_type",
    "phases",
    "primary_purpose",
    "start_date",
    "outcome_measure",
    "success"
]

# Create organizations table to avoid redundancy
organizations = df[[
    "Organization Full Name",
    "Organization Class",
    "Responsible Party"
]].drop_duplicates().reset_index(drop=True).copy()

organizations["organization_id"] = organizations.index + 1

organizations = organizations[[
    "organization_id",
    "Organization Full Name",
    "Organization Class",
    "Responsible Party"
]]

organizations.columns = [
    "organization_id",
    "organization_full_name",
    "organization_class",
    "responsible_party"
]

# Merge organization IDs back into main dataset
df = df.merge(
    organizations,
    left_on=["Organization Full Name", "Organization Class", "Responsible Party"],
    right_on=["organization_full_name", "organization_class", "responsible_party"],
    how="left"
)

# Create conditions table by splitting multiple conditions into separate rows
condition_rows = []

for _, row in df.iterrows():
    raw_conditions = row.get("Conditions", "")
    if raw_conditions:
        for cond in str(raw_conditions).split(","):
            cond = cond.strip()
            if cond:
                condition_rows.append({
                    "trial_id": row["trial_id"],
                    "condition_name": cond
                })

conditions = pd.DataFrame(condition_rows).drop_duplicates().reset_index(drop=True)
conditions["condition_id"] = conditions.index + 1
conditions = conditions[["condition_id", "trial_id", "condition_name"]]

# Create interventions table and keep descriptions
intervention_rows = []

for _, row in df.iterrows():
    raw_interventions = row.get("Interventions", "")
    description = row.get("Intervention Description", "")
    if raw_interventions:
        for inter in str(raw_interventions).split(","):
            inter = inter.strip()
            if inter:
                intervention_rows.append({
                    "trial_id": row["trial_id"],
                    "intervention_name": inter,
                    "intervention_description": description
                })

interventions = pd.DataFrame(intervention_rows).drop_duplicates().reset_index(drop=True)
interventions["intervention_id"] = interventions.index + 1
interventions = interventions[["intervention_id", "trial_id", "intervention_name", "intervention_description"]]

# Recreate clinical_trials table including organization_id
clinical_trials = df[[
    "trial_id",
    "organization_id",
    "Brief Title",
    "Full Title",
    "Overall Status",
    "Study Type",
    "Phases",
    "Primary Purpose",
    "Start Date",
    "Outcome Measure",
    "success"
]].copy()

clinical_trials.columns = [
    "trial_id",
    "organization_id",
    "brief_title",
    "full_title",
    "overall_status",
    "study_type",
    "phases",
    "primary_purpose",
    "start_date",
    "outcome_measure",
    "success"
]

# Save cleaned datasets for use in MongoDB and analysis pipeline
import os
import csv

output_dir = "/content/cleaned_outputs"
os.makedirs(output_dir, exist_ok=True)

cleaned_main = os.path.join(output_dir, "clinical_trials_cleaned.csv")
trials_path = os.path.join(output_dir, "clinical_trials.csv")
orgs_path = os.path.join(output_dir, "organizations.csv")
conds_path = os.path.join(output_dir, "conditions.csv")
inters_path = os.path.join(output_dir, "interventions.csv")

# Save each dataset as a CSV file
df.to_csv(cleaned_main, index=False, quoting=csv.QUOTE_ALL)
clinical_trials.to_csv(trials_path, index=False, quoting=csv.QUOTE_ALL)
organizations.to_csv(orgs_path, index=False, quoting=csv.QUOTE_ALL)
conditions.to_csv(conds_path, index=False, quoting=csv.QUOTE_ALL)
interventions.to_csv(inters_path, index=False, quoting=csv.QUOTE_ALL)

print("Saved files:")
for p in [cleaned_main, trials_path, orgs_path, conds_path, inters_path]:
    print("-", p)

print("clinical_trials shape:", clinical_trials.shape)
print("organizations shape:", organizations.shape)
print("conditions shape:", conditions.shape)
print("interventions shape:", interventions.shape)
