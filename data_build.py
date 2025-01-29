# ECON-470-HW1

## Author: Nikhita Gandhe

# Importing Libraries
import pandas as pd

# Read datasets (ensure file paths are correct)
# Use raw strings (r'') to avoid Unicode escape issues in file paths
full_ma_data = pd.read_csv(r'C:\Users\Nikhita Gandhe\OneDrive - Emory University\ECON 470\HW 1\Data Downloads\MA_Cnty_SA_2015_01.csv')
contract_service_area = pd.read_csv(r'C:\Users\Nikhita Gandhe\OneDrive - Emory University\ECON 470\HW 1\Data Downloads\CPSC_Contract_Info_2015_01.csv')

# Sample the data to inspect (Optional)
print("Sample from full_ma_data:")
print(full_ma_data.sample(3))

print("\nSample from contract_service_area:")
print(contract_service_area.sample(3))

# Question 1: Total Observations in the Dataset
# Count total rows and unique combinations of 'contractid', 'planid', 'county', and 'year'
total_rows = full_ma_data.shape[0]
unique_combinations = full_ma_data[['contractid', 'planid', 'county', 'year']].drop_duplicates().shape[0]

print(f"\nTotal observations in the dataset: {total_rows}")
print(f"Unique combinations of contractid, planid, county, and year: {unique_combinations}")

# Question 2: Count of Plans by Plan Type
plan_counts = full_ma_data.groupby('plan_type').size().reset_index(name='count')

print("\nPlan counts by type:")
print(plan_counts)

# Question 3: Exclude SNP, EGHP, and "800-series" Plans and Recompute Plan Counts
filtered_data = full_ma_data[
    (~full_ma_data['plan_type'].str.contains('SNP', na=False)) &
    (~full_ma_data['plan_type'].str.contains('EGHP', na=False)) &
    (~full_ma_data['plan_type'].str.startswith('800', na=False))
]

filtered_plan_counts = filtered_data.groupby('plan_type').size().reset_index(name='count')

print("\nFiltered plan counts by type:")
print(filtered_plan_counts)

# Question 4: Average Enrollment by Plan Type
average_enrollment = filtered_data.groupby('plan_type')['avg_enrollment'].mean().reset_index(name='average_enrollment')

print("\nAverage enrollment by plan type:")
print(average_enrollment)

# Export results to CSV (Optional)
filtered_plan_counts.to_csv(r'C:\Users\Nikhita Gandhe\OneDrive - Emory University\ECON 470\HW 1\Results\filtered_plan_counts.csv', index=False)
average_enrollment.to_csv(r'C:\Users\Nikhita Gandhe\OneDrive - Emory University\ECON 470\HW 1\Results\average_enrollment.csv', index=False)

print("\nResults exported to the Results folder.")