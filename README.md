# ECON-470-HW1
## Author: Nikhita Gandhe

# Import Libraries
import pandas as pd

# Question 1 Load the Data Python

# Load Data
enrollment = pd.read_csv("data/monthly_plan_enrollment_2015.csv")
service_area = pd.read_csv("data/service_area_2015.csv")

# Inner Merge
merged_data = pd.merge(enrollment, service_area, on=["plan_id", "county_id"], how="inner")

# Question 2 Count of Plans by Plan Type
plan_counts = merged_data.groupby("plan_type").size().reset_index(name="count")
print(plan_counts)

# 3. Remove Special Plans (SNP, EGHP, "800-Series")

filtered_data = merged_data[~merged_data["plan_type"].str.contains("SNP|EGHP|800", na=False)]

plan_counts_filtered = filtered_data.groupby("plan_type").size().reset_index(name="count")
print(plan_counts_filtered)

avg_enrollment = filtered_data.groupby("plan_type")["enrollment"].mean().reset_index(name="average_enrollment")
print(avg_enrollment)

plan_counts.to_csv("submission1/results/plan_counts.csv", index=False)
