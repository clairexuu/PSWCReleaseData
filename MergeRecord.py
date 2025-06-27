import pandas as pd

# Define the columns to keep
columns_to_keep = ["admissions_case_year", "exams_age_unit", "exams_type", "exams_weight_unit",
                   "patient_locations_where_holding", "patients_address_found", "patients_admitted_at",
                   "patients_city_found", "patients_common_name", "patients_county_found", "patients_days_in_care",
                   "patients_disposition", "patients_disposition_county", "patients_disposition_lat",
                   "patients_disposition_lng", "patients_disposition_location", "patients_disposition_subdivision",
                   "patients_dispositioned_at", "patients_dispositioned_by", "patients_release_type",
                   "patients_subdivision_found", "species_class", "species_family", "species_genus",
                   "species_lay_groups", "species_native_distributions", "species_order", "species_species"]

# Load Excel files and keep only selected columns
df1 = pd.read_excel("patient-medical-record-2024.xlsx", usecols=columns_to_keep)
df2 = pd.read_excel("patient-medical-record-2025.xlsx", usecols=columns_to_keep)

# Concatenate the two
combined = pd.concat([df1, df2], ignore_index=True)

# Save the result
combined.to_excel("record_24to25.xlsx", index=False)