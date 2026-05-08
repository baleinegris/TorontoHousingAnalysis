#### Preamble ####
# Purpose: Clean the raw data downloaded from Open Data Toronto in 02-download_data.py
# Author: Oscar Heath
# Date: May 7th 2026
# Contact: oscar.heath@mail.utoronto.ca
# License: MIT
# Pre-requisites: 
  # - `pandas` must be installed (pip install pandas)
  # - 02-download_data.py must have been run to download the raw data into data/01-raw_data/pre2023_raw_data.csv and data/01-raw_data/post2023_raw_data.csv

import pandas as pd

# Load in raw data
pre2023_raw_df = pd.read_csv("../data/01-raw_data/pre2023_raw_data.csv")
post2023_raw_df = pd.read_csv("../data/01-raw_data/post2023_raw_data.csv")

# Combine the two datasets into one
raw_df = pd.concat([pre2023_raw_df, post2023_raw_df], ignore_index=True)

# Columns we're interested in: RSN, CONFIRMED_STOREYS, CONFIRMED_UNITS, SCORE, YEAR_BUILT
columns_of_interest = ["RSN","CONFIRMED_STOREYS", "CONFIRMED_UNITS", "SCORE", "YEAR_BUILT", "YEAR_REGISTERED","LATITUDE", "LONGITUDE"]

# We're opting to drop the missing values, as there are very few of them
raw_df = raw_df[columns_of_interest]

print(f"Number of rows in raw data: {len(raw_df)}")

# For every record with matching RSN, keep only the most recent one
# We aren't as interested in the evaluation scores, we care mostly about
# the building itself, meaning the year built, storeys, and units
raw_df.sort_values(by=["RSN", "YEAR_BUILT"], ascending=[True, False], inplace=True)
raw_df.drop_duplicates(subset=["RSN"], keep="first", inplace=True)

# keep only records with year built after 1900 and before 2021, we're interested
# in seeing amount of construction in my lifetime
raw_df = raw_df[(raw_df["YEAR_BUILT"] >= 1900) & (raw_df["YEAR_BUILT"] < 2020)]

# Save cleaned data
raw_df.to_csv("../data/02-analysis_data/analysis_data.csv", index=False)

print(f"Number of rows in cleaned data: {len(raw_df)}")