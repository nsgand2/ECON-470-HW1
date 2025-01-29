# ECON-470-HW1
## Author: Nikhita Gandhe

# Importing Libraries
import pandas as pd

# Read datasets (ensure file paths are correct)
full_ma_data = pd.read_csv('../data/output/full_ma_data.csv')  # Replace with actual path
contract_service_area = pd.read_csv('../data/output/contract_service_area.csv')  # Replace with actual path

# Sample the data to inspect (Optional)
print(full_ma_data.sample(3))
print(contract_service_area.sample(3))

# Question 1: Total Observations in the Dataset
# Count total rows and unique combinations of 'contractid', 'planid', 'county', and 'year'
total_rows = full_ma_data.shape[0]
unique_combinations = full_ma_data[['contractid', 'planid', 'county', 'year']].drop_duplicates().shape[0]

print(f"Total observations: {total_rows}")
print(f"Unique combinations of contractid, planid, county, and year: {unique_combinations}")

# Question 2: Count of Plans by Plan Type
plan_counts = full_ma_data.groupby('plan_type').size().reset_index(name='count')
print(plan_counts)

# Question 3: Exclude SNP, EGHP, and "800-series" Plans and Recompute Plan Counts
# Filter out unwanted plan types
filtered_data = full_ma_data[
    (~full_ma_data['plan_type'].str.contains('SNP', na=False)) &
    (~full_ma_data['plan_type'].str.contains('EGHP', na=False)) &
    (~full_ma_data['plan_type'].str.startswith('800', na=False))
]

filtered_plan_counts = filtered_data.groupby('plan_type').size().reset_index(name='count')
print(filtered_plan_counts)

# Question 4: Average Enrollment by Plan Type
average_enrollment = filtered_data.groupby('plan_type')['avg_enrollment'].mean().reset_index(name='average_enrollment')
print(average_enrollment)

# Optional: Export results to CSV
plan_counts.to_csv('../submission1/results/plan_counts.csv', index=False)
filtered_plan_counts.to_csv('../submission1/results/filtered_plan_counts.csv', index=False)
average_enrollment.to_csv('../submission1/results/average_enrollment.csv', index=False)
