# ============================================================
# CIBC Banking Analytics Dashboard
# Phase 2: Full Data Cleaning & Feature Engineering
# Dataset: Credit Card Customer Attrition (10,127 records)
# Author: Your Name
# ============================================================

import pandas as pd
import numpy as np
import os

# ── 1. LOAD RAW DATA ────────────────────────────────────────
df = pd.read_csv('../data/raw/cibc_creditcard_raw.csv')

print("=" * 60)
print("CIBC BANKING ANALYTICS — DATA CLEANING STARTED")
print("=" * 60)
print(f"\n📌 Original Shape: {df.shape}")

# ── 2. DROP JUNK COLUMNS ────────────────────────────────────
# CLIENTNUM = just an ID, not useful for analysis
# Naive Bayes columns = model artifacts, not real data
cols_to_drop = [
    'CLIENTNUM',
    'Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_1',
    'Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_2'
]
df.drop(columns=cols_to_drop, inplace=True)
print(f"\n✅ Dropped junk columns. New shape: {df.shape}")

# ── 3. RENAME COLUMNS TO SNAKE_CASE ─────────────────────────
df.columns = (df.columns
              .str.strip()
              .str.lower()
              .str.replace(' ', '_')
              .str.replace('-', '_'))

print("\n✅ Columns renamed to snake_case:")
print(df.columns.tolist())

# ── 4. CLEAN CATEGORICAL VALUES ─────────────────────────────
# Standardize attrition flag to simple labels
df['attrition_flag'] = df['attrition_flag'].str.strip()
df['attrition_flag'] = df['attrition_flag'].map({
    'Existing Customer': 'Retained',
    'Attrited Customer': 'Churned'
})

# Standardize gender
df['gender'] = df['gender'].str.strip()
df['gender'] = df['gender'].map({
    'M': 'Male',
    'F': 'Female'
})

# Standardize card category to CIBC-style naming
df['card_category'] = df['card_category'].str.strip()
df['card_category'] = df['card_category'].map({
    'Blue':     'CIBC Classic',
    'Silver':   'CIBC Select',
    'Gold':     'CIBC Gold',
    'Platinum': 'CIBC Platinum'
})

print("\n✅ Categorical values cleaned and standardized")
print("\n📌 Attrition Distribution:")
print(df['attrition_flag'].value_counts())
print("\n📌 Card Category Distribution:")
print(df['card_category'].value_counts())

# ── 5. ADD CANADIAN PROVINCES ───────────────────────────────
# Dataset has no geography — we add realistic Canadian provinces
# based on CIBC's actual market presence
np.random.seed(42)
provinces = [
    'Ontario', 'Quebec', 'British Columbia',
    'Alberta', 'Manitoba', 'Nova Scotia'
]
weights = [0.35, 0.23, 0.16, 0.14, 0.07, 0.05]
df['province'] = np.random.choice(provinces, size=len(df), p=weights)

print("\n✅ Canadian provinces added:")
print(df['province'].value_counts())

# ── 6. REMOVE OUTLIERS (IQR METHOD) ─────────────────────────
def remove_outliers_iqr(dataframe, column):
    Q1 = dataframe[column].quantile(0.25)
    Q3 = dataframe[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    before = len(dataframe)
    dataframe = dataframe[
        (dataframe[column] >= lower) &
        (dataframe[column] <= upper)
    ]
    after = len(dataframe)
    print(f"   {column}: removed {before - after} outliers")
    return dataframe

print("\n📌 Removing outliers:")
df = remove_outliers_iqr(df, 'credit_limit')
df = remove_outliers_iqr(df, 'total_trans_amt')
df = remove_outliers_iqr(df, 'total_revolving_bal')
df = remove_outliers_iqr(df, 'customer_age')

# ── 7. FEATURE ENGINEERING ──────────────────────────────────

# Age Group segmentation
df['age_group'] = pd.cut(
    df['customer_age'],
    bins=[0, 25, 35, 45, 55, 65, 100],
    labels=['18-25', '26-35', '36-45', '46-55', '56-65', '65+']
)

# Credit Limit Tier
df['credit_tier'] = pd.cut(
    df['credit_limit'],
    bins=[0, 5000, 10000, 20000, 35000],
    labels=['Entry ($0-5K)', 'Standard ($5-10K)',
            'Premium ($10-20K)', 'Elite ($20K+)']
)

# Transaction Frequency Segment
df['transaction_segment'] = pd.cut(
    df['total_trans_ct'],
    bins=[0, 30, 60, 90, 200],
    labels=['Low', 'Medium', 'High', 'Very High']
)

# Churn binary flag (1 = churned, 0 = retained)
df['churn_flag'] = (df['attrition_flag'] == 'Churned').astype(int)

# Utilization Category
df['utilization_category'] = pd.cut(
    df['avg_utilization_ratio'],
    bins=[-0.01, 0.10, 0.30, 0.60, 1.01],
    labels=['Very Low (<10%)', 'Low (10-30%)',
            'Medium (30-60%)', 'High (>60%)']
)

print("\n✅ Feature engineering complete:")
print("\n📌 Age Group Distribution:")
print(df['age_group'].value_counts().sort_index())
print("\n📌 Credit Tier Distribution:")
print(df['credit_tier'].value_counts())
print("\n📌 Transaction Segment:")
print(df['transaction_segment'].value_counts())
print("\n📌 Utilization Category:")
print(df['utilization_category'].value_counts())

# ── 8. FINAL SUMMARY ────────────────────────────────────────
print("\n" + "=" * 60)
print("📊 FINAL CLEANED DATASET SUMMARY")
print("=" * 60)
print(f"Total Records   : {len(df):,}")
print(f"Total Columns   : {len(df.columns)}")
print(f"Churned         : {df['churn_flag'].sum():,} ({df['churn_flag'].mean()*100:.1f}%)")
print(f"Retained        : {(df['churn_flag']==0).sum():,} ({(1-df['churn_flag'].mean())*100:.1f}%)")
print(f"Avg Credit Limit: ${df['credit_limit'].mean():,.2f}")
print(f"Avg Trans Amount: ${df['total_trans_amt'].mean():,.2f}")
print(f"Avg Utilization : {df['avg_utilization_ratio'].mean()*100:.1f}%")

# ── 9. SAVE CLEANED DATA ────────────────────────────────────
os.makedirs('../data/cleaned', exist_ok=True)
df.to_csv('../data/cleaned/cibc_cleaned.csv', index=False)
print("\n✅ Cleaned data saved → data/cleaned/cibc_cleaned.csv")
print("\n🏦 Phase 2 Complete — Data Cleaning Done!")