# ECON-470-HW1

## Author: Nikhita Gandhe

# Importing Libraries
import pandas as pd
import os

# Read datasets (ensure file paths are correct)
enrollment_df = pd.read_csv(
    r'C:\Users\Nikhita Gandhe\OneDrive - Emory University\ECON 470\HW 1\Data Downloads\CPSC_Enrollment_Info_2015_01.csv',
    low_memory=False
)
service_area_df = pd.read_csv(
    r'C:\Users\Nikhita Gandhe\OneDrive - Emory University\ECON 470\HW 1\Data Downloads\MA_Cnty_SA_2015_01.csv',
    low_memory=False
)

# Rename columns to ensure consistency
enrollment_df = enrollment_df.rename(columns={
    "Contract Number": "Contract ID",
    "Plan ID": "Plan ID",
    "FIPS State County Code": "FIPS",
    "Enrollment": "Enrollment"
})
service_area_df = service_area_df.rename(columns={
    "FIPS": "FIPS"
})

# Convert columns to numeric where necessary
enrollment_df["Enrollment"] = pd.to_numeric(enrollment_df["Enrollment"], errors="coerce")
service_area_df["FIPS"] = pd.to_numeric(service_area_df["FIPS"], errors="coerce")

# Drop duplicates to clean the data
enrollment_df = enrollment_df.drop_duplicates()
service_area_df = service_area_df.drop_duplicates()

# Merge datasets on "Contract ID" and "FIPS"
merged_df = pd.merge(enrollment_df, service_area_df, on=["Contract ID", "FIPS"], how="inner")

# Table 1: Count of plans by type (before exclusions)
table_1 = merged_df.groupby("Plan Type")["Plan ID"].nunique().reset_index()
table_1.columns = ["Plan Type", "Plan Count"]

# Filter out SNP, EGHP, and 800-series plans
filtered_df = merged_df[
    (~merged_df["Plan Type"].str.contains("SNP", case=False, na=False)) &  # Exclude SNP
    (merged_df["EGHP"].isna()) &  # Exclude Employer Group Plans
    (~merged_df["Plan ID"].astype(str).str.startswith("8"))  # Exclude 800-series plans
]

# Table 2: Count of plans by type after exclusions
table_2 = filtered_df.groupby("Plan Type")["Plan ID"].nunique().reset_index()
table_2.columns = ["Plan Type", "Plan Count"]

# Table 3: Average enrollments per plan type
table_3 = filtered_df.groupby("Plan Type")["Enrollment"].mean().reset_index()
table_3.columns = ["Plan Type", "Average Enrollment"]

# Display tables
print("Plan Count by Type (Before Exclusions):")
print(table_1)
print("\nPlan Count by Type (After Exclusions):")
print(table_2)
print("\nAverage Enrollment by Plan Type:")
print(table_3)

# Save tables to CSV files
results_dir = r'C:\Users\Nikhita Gandhe\OneDrive - Emory University\ECON 470\HW 1\Results'
os.makedirs(results_dir, exist_ok=True)

table_1.to_csv(os.path.join(results_dir, 'plan_count_before_exclusions.csv'), index=False)
table_2.to_csv(os.path.join(results_dir, 'plan_count_after_exclusions.csv'), index=False)
table_3.to_csv(os.path.join(results_dir, 'average_enrollment_by_plan_type.csv'), index=False)
