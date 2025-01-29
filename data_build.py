# ECON-470-HW1

## Author: Nikhita Gandhe

# Importing Libraries
import pandas as pd
import os

# Read datasets (ensure file paths are correct)
full_ma_data = pd.read_csv(
    r'C:\Users\Nikhita Gandhe\OneDrive - Emory University\ECON 470\HW 1\Data Downloads\MA_Cnty_SA_2015_01.csv',
    low_memory=False
)
contract_service_area = pd.read_csv(
    r'C:\Users\Nikhita Gandhe\OneDrive - Emory University\ECON 470\HW 1\Data Downloads\CPSC_Contract_Info_2015_01.csv',
    encoding='latin1'
)

# Inspect column names to ensure correctness
print("Columns in full_ma_data:", full_ma_data.columns)
print("Columns in contract_service_area:", contract_service_area.columns)

# Question 1: Total Observations in the Dataset
total_rows = full_ma_data.shape[0]
unique_combinations = full_ma_data[['Contract ID', 'County']].drop_duplicates().shape[0]

print(f"\nTotal observations in the dataset: {total_rows}")
print(f"Unique combinations of Contract ID and County: {unique_combinations}")

# Question 2: Count of Plans by Plan Type
plan_counts = full_ma_data.groupby('Plan Type').size().reset_index(name='count')

print("\nPlan counts by type:")
print(plan_counts)

# Question 3: Exclude SNP, EGHP, and "800-series" Plans and Recompute Plan Counts
filtered_data = full_ma_data[
    (~full_ma_data['Plan Type'].str.contains('SNP', na=False)) &
    (~full_ma_data['Plan Type'].str.contains('EGHP', na=False)) &
    (~full_ma_data['Plan Type'].str.startswith('800', na=False))
]

filtered_plan_counts = filtered_data.groupby('Plan Type').size().reset_index(name='count')

print("\nFiltered plan counts by type:")
print(filtered_plan_counts)

# Question 4: Average Enrollment by Plan Type
if 'Avg Enrollment' in full_ma_data.columns:
    average_enrollment = filtered_data.groupby('Plan Type')['Avg Enrollment'].mean().reset_index(name='average_enrollment')
    print("\nAverage enrollment by plan type:")
    print(average_enrollment)
else:
    print("\nColumn 'Avg Enrollment' not found. Skipping Question 4.")

# Create Results Directory
results_dir = r'C:\Users\Nikhita Gandhe\OneDrive - Emory University\ECON 470\HW 1\Results'
os.makedirs(results_dir, exist_ok=True)

# Export results to CSV
filtered_plan_counts.to_csv(os.path.join(results_dir, 'filtered_plan_counts.csv'), index=False)
if 'average_enrollment' in locals():
    average_enrollment.to_csv(os.path.join(results_dir, 'average_enrollment.csv'), index=False)

print("\nResults exported to the Results folder.")
