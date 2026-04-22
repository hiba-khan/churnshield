#!/usr/bin/env python
"""
Telco Customer Churn - Exploratory Data Analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style for visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Loading the telco churn dataset

data_path = Path("../data/WA_Fn-UseC_-Telco-Customer-Churn (3).csv")
df = pd.read_csv(data_path)

print(f"Dataset shape: {df.shape}")
print(f"\nFirst few rows:")
print(df.head())

# Dataset Overview & Info

print("\n" + "="*70)
print("DATA INFO:")
print("="*70)
print(df.info())
print("\n" + "="*70)
print("MISSING VALUES:")
print("="*70)
print(df.isnull().sum())
print("\n" + "="*70)
print("BASIC STATISTICS:")
print("="*70)
print(df.describe())


# Key Features vs Churn
key_features = ['tenure', 'MonthlyCharges', 'TotalCharges'] if 'tenure' in df.columns else []

if key_features:
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    for idx, col in enumerate(key_features[:3]):
        if col in df.columns:
            df.boxplot(column=col, by='Churn', ax=axes[idx])
            axes[idx].set_title(f'{col} vs Churn')
            axes[idx].set_xlabel('Churn')
            axes[idx].set_ylabel(col)
    
    plt.suptitle('')  # Remove default title
    plt.tight_layout()
    plt.show()

# Categorical Features Analysis
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

print("\n" + "="*70)
print("CATEGORICAL COLUMNS:")
print("="*70)
print(f"Categorical columns: {categorical_cols}")
print(f"\nNumerical columns: {numerical_cols}")

# Display unique value counts for categorical features
print("\n" + "="*70)
print("UNIQUE VALUE COUNTS:")
print("="*70)
for col in categorical_cols[:5]:  # Show first 5
    print(f"\n{col}: {df[col].nunique()} unique values")
    print(df[col].value_counts().head(10))

# Churn Distribution
if 'Churn' in df.columns:
    churn_counts = df['Churn'].value_counts()
    churn_pct = df['Churn'].value_counts(normalize=True) * 100
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Count plot
    churn_counts.plot(kind='bar', ax=ax1, color=['#2ecc71', '#e74c3c'])
    ax1.set_title('Churn Count', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Churn')
    ax1.set_ylabel('Count')
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=0)
    
    # Percentage plot
    churn_pct.plot(kind='pie', ax=ax2, autopct='%1.1f%%', colors=['#2ecc71', '#e74c3c'])
    ax2.set_title('Churn Distribution (%)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('')
    
    plt.tight_layout()
    plt.show()
    
    print("\n" + "="*70)
    print("CHURN DISTRIBUTION:")
    print("="*70)
    print(f"\nChurn Distribution (counts):\n{churn_counts}")
    print(f"\nChurn Distribution (%):\n{churn_pct}")
