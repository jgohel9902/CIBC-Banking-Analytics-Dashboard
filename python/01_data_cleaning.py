# ============================================================
# CIBC Banking Analytics Dashboard
# Phase 2: Data Cleaning
# Author: Your Name
# ============================================================

import pandas as pd
import numpy as np
import os

# ── 1. LOAD RAW DATA ────────────────────────────────────────
df = pd.read_csv('../data/raw/bank_churn_raw.csv')

print("=" * 60)
print("CIBC BANKING ANALYTICS — DATA CLEANING")
print("=" * 60)

# ── 2. INITIAL INSPECTION ───────────────────────────────────
print("\n📌 Shape:", df.shape)
print("\n📌 Columns:\n", df.columns.tolist())
print("\n📌 Data Types:\n", df.dtypes)
print("\n📌 First 5 Rows:\n", df.head())
print("\n📌 Basic Stats:\n", df.describe())
print("\n📌 Missing Values:\n", df.isnull().sum())
print("\n📌 Duplicate Rows:", df.duplicated().sum())

# ── 3. DROP UNNECESSARY COLUMNS ─────────────────────────────
# RowNumber, CustomerId, Surname are not useful for analysis
cols_to_drop = ['RowNumber', 'CustomerId', 'Surname']
df.drop(columns=cols_to_drop, inplace=True)
print("\n✅ Dropped columns:", cols_to_drop)

# ── 4. RENAME COLUMNS TO SNAKE_CASE ─────────────────────────
df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
print("\n✅ Renamed columns to snake_case:", df.columns.tolist())

# ── 5. DROP DUPLICATES ───────────────────────────────────────
before = len(df)
df.drop_duplicates(inplace=True)
after = len(df)
print(f"\n✅ Duplicates removed: {before - after} rows dropped")

# ── 6. HANDLE MISSING VALUES ────────────────────────────────
print("\n📌 Missing values before fix:\n", df.isnull().sum())
# Fill numeric nulls with median (robust to outliers)
for col in df.select_dtypes(include=[np.number]).columns:
    if df[col].isnull().sum() > 0:
        df[col].fillna(df[col].median(), inplace=True)
# Fill categorical nulls with mode
for col in df.select_dtypes(include=['object']).columns:
    if df[col].isnull().sum() > 0:
        df[col].fillna(df[col].mode()[0], inplace=True)
print("✅ Missing values after fix:\n", df.isnull().sum())

# ── 7. FIX DATA TYPES ───────────────────────────────────────
df['hascrcard'] = df['hascrcard'].astype(int)
df['isactivemember'] = df['isactivemember'].astype(int)
df['exited'] = df['exited'].astype(int)
print("\n✅ Data types fixed")

# ── 8. REMOVE OUTLIERS (IQR METHOD) ─────────────────────────
def remove_outliers_iqr(dataframe, column):
    Q1 = dataframe[column].quantile(0.25)
    Q3 = dataframe[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    before = len(dataframe)
    dataframe = dataframe[(dataframe[column] >= lower) & (dataframe[column] <= upper)]
    after = len(dataframe)
    print(f"   {column}: removed {before - after} outliers")
    return dataframe

print("\n📌 Removing outliers:")
df = remove_outliers_iqr(df, 'creditscore')
df = remove_outliers_iqr(df, 'age')
df = remove_outliers_iqr(df, 'balance')
df = remove_outliers_iqr(df, 'estimatedsalary')

# ── 9. ADD DERIVED COLUMNS ──────────────────────────────────
# Age Group segmentation (used in dashboard)
df['age_group'] = pd.cut(
    df['age'],
    bins=[0, 25, 35, 45, 55, 100],
    labels=['18-25', '26-35', '36-45', '46-55', '55+']
)

# Balance Tier segmentation
df['balance_tier'] = pd.cut(
    df['balance'],
    bins=[-1, 1000, 50000, 100000, 150000, float('inf')],
    labels=['Zero/Low', 'Low-Mid', 'Mid', 'High', 'Premium']
)

# Churn Label (readable)
df['churn_label'] = df['exited'].map({0: 'Retained', 1: 'Churned'})

print("\n✅ Derived columns added: age_group, balance_tier, churn_label")

# ── 10. FINAL INSPECTION ────────────────────────────────────
print("\n" + "=" * 60)
print("📊 FINAL CLEANED DATASET SUMMARY")
print("=" * 60)
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print("\nChurn Distribution:\n", df['churn_label'].value_counts())
print("\nAge Group Distribution:\n", df['age_group'].value_counts())
print("\nBalance Tier Distribution:\n", df['balance_tier'].value_counts())
print("\nGeography Distribution:\n", df['geography'].value_counts())

# ── 11. SAVE CLEANED DATA ───────────────────────────────────
os.makedirs('../data/cleaned', exist_ok=True)
df.to_csv('../data/cleaned/cibc_cleaned.csv', index=False)
print("\n✅ Cleaned data saved to: data/cleaned/cibc_cleaned.csv")
print("\n🏦 Phase 2 Complete — Data Cleaning Done!")