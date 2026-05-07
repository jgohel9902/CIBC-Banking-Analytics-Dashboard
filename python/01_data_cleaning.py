# ============================================================
# CIBC Banking Analytics Dashboard
# Phase 2: Data Exploration & Cleaning
# Dataset: Credit Card Customer Attrition
# Author: Your Name
# ============================================================

import pandas as pd
import numpy as np
import os

# ── 1. LOAD RAW DATA ────────────────────────────────────────
df = pd.read_csv('../data/raw/cibc_creditcard_raw.csv')

print("=" * 60)
print("INITIAL DATA EXPLORATION")
print("=" * 60)
print("\n📌 Shape:", df.shape)
print("\n📌 Columns:\n")
for col in df.columns:
    print(f"   {col}")
print("\n📌 Data Types:\n", df.dtypes)
print("\n📌 First 5 Rows:\n", df.head())
print("\n📌 Missing Values:\n", df.isnull().sum())
print("\n📌 Duplicates:", df.duplicated().sum())
print("\n📌 Basic Stats:\n", df.describe())