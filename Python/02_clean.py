import pandas as pd

df = pd.read_csv(r'C:\Users\basud\OneDrive\Desktop\Healthcare_PowerBI_Project\DATA\raw_healthcare_dataset.csv')

# 1. Fix column names (remove spaces)
df.columns = df.columns.str.strip().str.replace(' ', '_')

# 2. Fix date columns
df['Date_of_Admission'] = pd.to_datetime(df['Date_of_Admission'])
df['Discharge_Date'] = pd.to_datetime(df['Discharge_Date'])

# 3. Create new calculated columns
df['Length_of_Stay'] = (df['Discharge_Date'] - df['Date_of_Admission']).dt.days

df['Admission_Month'] = df['Date_of_Admission'].dt.month_name()
df['Admission_Year'] = df['Date_of_Admission'].dt.year
df['Admission_Quarter'] = df['Date_of_Admission'].dt.to_period('Q').astype(str)

# 4. Create Age Groups
bins = [0, 18, 35, 50, 65, 100]
labels = ['0–18', '19–35', '36–50', '51–65', '65+']
df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels)

# 5. Round billing amount
df['Billing_Amount'] = df['Billing_Amount'].round(2)

# 6. Check for duplicates
print(f"Duplicates: {df.duplicated().sum()}")
df.drop_duplicates(inplace=True)

# 7. Check nulls again
print(df.isnull().sum())

# 8. Save clean file
import os
os.makedirs(r"C:\Users\basud\OneDrive\Desktop\Healthcare_PowerBI_Project\DATA\cleaned", exist_ok=True)
df.to_csv(r"C:\Users\basud\OneDrive\Desktop\Healthcare_PowerBI_Project\DATA\cleaned\healthcare_cleaned.csv", index=False)
print("✅ Clean file saved!")
