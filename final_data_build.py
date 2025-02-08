# %% [markdown]
# ---
# title: "Homework 1"
# subtitle: "ECON 470"
# author: "Nikhita Gandhe"
# execute:
#   echo: false
# format:
#   pdf:
#     output-file: "Gandhe-b-hwk1-2"
#     output-exit: "pdf"
#     code-fold: true
#     highlight-style: github
#     include-in-header:
#       text: |
#         \addtokomafont{disposition}{\rmfamily}
#
# jupyter: python3
# ---
#
# Below are my answers to the homework questions.

# %% [markdown]
# ## **Step 1: Importing Libraries**
# First, we import necessary libraries for data analysis.

# %%
import pandas as pd
import os
from IPython.display import Markdown, display
import warnings

warnings.simplefilter("ignore")  # Suppress warnings for cleaner output

# %% [markdown]
# ## **Step 2: Loading Data**
# 
# The following datasets are used:
# - `CPSC_Enrollment_Info_2015_01.csv`: Medicare enrollment data.
# - `MA_Cnty_SA_2015_01.csv`: Service area information.

# %%
# Load datasets (ensure correct file paths)
contract_data = pd.read_csv(
    r'C:\Users\Nikhita Gandhe\OneDrive - Emory University\ECON 470\HW 1\Data Downloads\CPSC_Contract_Info_2015_01.csv',
    encoding='latin1', skiprows=1, names=[
        "contractid", "planid", "org_type", "plan_type", "partd", "snp", "eghp", "org_name",
        "org_marketing_name", "plan_name", "parent_org", "contract_date"
    ], dtype={"contractid": str, "planid": float, "snp": str, "eghp": str}
)

enrollment_data = pd.read_csv(
    r'C:\Users\Nikhita Gandhe\OneDrive - Emory University\ECON 470\HW 1\Data Downloads\CPSC_Enrollment_Info_2015_01.csv',
    skiprows=1, names=["contractid", "planid", "ssa", "fips", "state", "county", "enrollment"],
    dtype={"contractid": str, "planid": float, "ssa": float, "fips": float, "state": str, "county": str, "enrollment": float},
    na_values="*"
)

# %% [markdown]
# ## **Step 3: Data Cleaning**
# - **Remove duplicate contract IDs.**
# - **Merge enrollment data with contract data.**
# - **Fill missing FIPS codes.**

# %%
# Remove duplicate contracts
contract_data['idCount'] = contract_data.groupby(['contractid', 'planid']).cumcount() + 1
contract_data = contract_data[contract_data["idCount"] == 1].drop(columns=['idCount'])

# Merge datasets on "contractid" and "planid"
merged_data = contract_data.merge(enrollment_data, on=["contractid", "planid"], how="left")
merged_data['year'] = 2015  # Assign year for consistency

# Fill missing FIPS codes
merged_data['fips'] = merged_data.groupby(['state', 'county'])['fips'].ffill().bfill()

# Forward-fill missing plan attributes
for col in ['plan_type', 'partd', 'snp', 'eghp', 'plan_name']:
    merged_data[col] = merged_data.groupby(['contractid', 'planid'])[col].ffill().bfill()

# Forward-fill missing organization details
for col in ['org_type', 'org_name', 'org_marketing_name', 'parent_org']:
    merged_data[col] = merged_data.groupby(['contractid'])[col].ffill().bfill()

# Rename for clarity
merged_data.rename(columns={"enrollment": "avg_enrollment"}, inplace=True)

# Save cleaned data
comp_merged_data = pd.concat([merged_data], ignore_index=True)
# comp_merged_data.to_csv("data/output/compTotalData.csv")  # Uncomment to save

# %% [markdown]
# \newpage
# 
# # **Building the Data**
# 
# The cleaned dataset will now be used to compute and display the following tables.

# %% [markdown]
# ## **Question 1: Plan Count by Type**
# 
# The number of plans under each **Plan Type** in 2015.

# %%
# Load cleaned dataset
# comp_total_data = pd.read_csv("data/output/compTotalData.csv")  # Uncomment if needed

# Compute plan counts
plan_counts = comp_merged_data.pivot_table(index='plan_type', columns='year', values='planid', aggfunc='count')
display(Markdown("### **Plan Count by Type (Before Exclusions)**"))
display(Markdown(plan_counts.to_markdown()))

# %% [markdown]
# \newpage
# ## **Question 2: Excluding SNP, EGHP, and 800-Series Plans**
# 
# The dataset is filtered to exclude:
# - **Special Needs Plans (SNP)**
# - **Employer Group Plans (EGHP)**
# - **800-Series Plans** (plans with ID between 800-899).

# %%
# Apply exclusions
filtered_data = comp_merged_data[
    (comp_merged_data['snp'] == "No") &
    (comp_merged_data['eghp'] == "No") &
    ((comp_merged_data['planid'] < 800) | (comp_merged_data['planid'] >= 900))
]

# Compute updated plan counts
filtered_plan_counts = filtered_data.pivot_table(index='plan_type', columns='year', values='avg_enrollment', aggfunc='count')

# Display table
display(Markdown("### **Updated Plan Count by Type (After Exclusions)**"))
display(Markdown(filtered_plan_counts.to_markdown()))

# %% [markdown]
# \newpage
# ## **Question 3: Average Enrollments by Type**
# 
# Finally, we compute the **average enrollment per plan type** in 2015.

# %%
# Compute enrollment averages
enrollment_avg = filtered_data.pivot_table(index='plan_type', columns='year', values='avg_enrollment', aggfunc='mean')

# Display table
display(Markdown("### **Average Enrollment by Plan Type (2015)**"))
display(Markdown(enrollment_avg.to_markdown()))



# %%
