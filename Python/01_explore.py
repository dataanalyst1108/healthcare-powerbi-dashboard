import pandas as pd
df= pd.read_csv(r'C:\Users\basud\OneDrive\Desktop\Healthcare_PowerBI_Project\DATA\raw_healthcare_dataset.csv')
print(df.shape)

print(df.dtypes)

print(df.isnull().sum())

print(df.head())

print(df['Medical Condition'].value_counts())

print(df['Admission Type'].value_counts())
