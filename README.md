# Healthcare Operations Analytics Dashboard

A Power BI dashboard built on top of a real hospital dataset — covers patient admissions, billing, clinical outcomes, and doctor/hospital performance across 54,966 records.

I built this as part of my data analytics portfolio. The idea was simple: take raw messy data, clean it properly in Python, and turn it into something a hospital manager could actually sit down and use without needing to know anything about data.

![Dashboard Preview](screenshots/01_executive_summary.png)

---

## Why I built this

I wanted to work on a domain that feels real — not just another sales dataset. Healthcare has genuinely complex data: you've got admissions, billing, doctors, test results, insurance providers all linked together, and there are actual business questions worth answering. That made it more interesting to work on.

The dashboard ended up with 4 pages, drill-through navigation, 5 interactive slicers, and conditional formatting on the matrices. Not because I was trying to tick boxes — those features just made sense given what the data had to say.

---

## What the project covers

**Data cleaning in Python** — the raw CSV had 55,500 rows with inconsistent column names, date columns stored as strings, and 534 duplicate records. I fixed all of that and added 5 new calculated columns before the data ever touched Power BI.

**DAX measures** — wrote all KPI measures from scratch including Emergency %, Abnormal Test %, Avg Billing, and Total Revenue. Kept them all in a separate measures table so the model stays clean.

**4-page dashboard:**
- Executive Summary — the big picture (KPIs, monthly trend, admission types, test results)
- Patient Demographics — age groups, gender split, blood types, insurance vs billing
- Hospital Operations — doctor performance, hospital billing, scatter of stay vs billing
- Patient Detail — drill-through page that filters to individual patient records by condition

---

## Tools used

- Python 3.10 with Pandas — data cleaning and feature engineering
- Power BI Desktop — dashboard development
- DAX — all measures and calculated columns
- Power Query — data type fixes before loading
- GitHub — version control

---

## Dataset

Source: [Healthcare Dataset on Kaggle by Prasad22](https://www.kaggle.com/datasets/prasad22/healthcare-dataset)

| | |
|---|---|
| Raw rows | 55,500 |
| After cleaning | 54,966 |
| Original columns | 15 |
| After feature engineering | 20 |

The 5 columns I added:

| Column | What it is |
|---|---|
| `Length_of_Stay` | Days between admission and discharge |
| `Admission_Month` | Month name from admission date |
| `Admission_Year` | Year from admission date |
| `Admission_Quarter` | Q1 / Q2 / Q3 / Q4 |
| `Age_Group` | Bucketed age: 0–18, 19–35, 36–50, 51–65, 65+ |

---

## Folder structure

```
Healthcare_PowerBI_Project/
│
├── DATA/
│   ├── raw/
│   │   └── raw_healthcare_dataset.csv
│   └── cleaned/
│       └── healthcare_cleaned.csv
│
├── Python/
│   ├── 01_explore.py
│   └── 02_clean.py
│
├── powerbi/
│   └── Healthcare_Dashboard.pbix
│
├── screenshots/
│   ├── 01_executive_summary.png
│   ├── 02_patient_demographics.png
│   ├── 03_hospital_operations.png
│   ├── 04_patient_detail_drillthrough.png
│   ├── 05_slicer_filter_demo.png
│   └── 06_drillthrough_demo.png
│
└── README.md
```

---

## Cleaning script — what it does

```python
import pandas as pd

df = pd.read_csv(r'path\to\raw_healthcare_dataset.csv')

# clean column names
df.columns = df.columns.str.strip().str.replace(' ', '_')

# fix dates
df['Date_of_Admission'] = pd.to_datetime(df['Date_of_Admission'])
df['Discharge_Date'] = pd.to_datetime(df['Discharge_Date'])

# new columns
df['Length_of_Stay'] = (df['Discharge_Date'] - df['Date_of_Admission']).dt.days
df['Admission_Month'] = df['Date_of_Admission'].dt.month_name()
df['Admission_Year'] = df['Date_of_Admission'].dt.year
df['Admission_Quarter'] = df['Date_of_Admission'].dt.to_period('Q').astype(str)

bins = [0, 18, 35, 50, 65, 100]
labels = ['0–18', '19–35', '36–50', '51–65', '65+']
df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels)

# remove duplicates
df.drop_duplicates(inplace=True)

df.to_csv(r'path\to\healthcare_cleaned.csv', index=False)
```

Final output: 54,966 rows, 20 columns, zero nulls.

---

## DAX measures

```dax
Total Patients = COUNTROWS(cleaned_healthcare_dataset)

Avg Billing Amount = AVERAGE(cleaned_healthcare_dataset[Billing_Amount])

Avg Length of Stay = AVERAGE(cleaned_healthcare_dataset[Length_of_Stay])

Total Revenue = SUM(cleaned_healthcare_dataset[Billing_Amount])

Emergency % =
DIVIDE(
    COUNTROWS(
        FILTER(cleaned_healthcare_dataset,
            cleaned_healthcare_dataset[Admission_Type] = "Emergency")
    ),
    COUNTROWS(cleaned_healthcare_dataset),
    0
) * 100

Abnormal Test % =
DIVIDE(
    COUNTROWS(
        FILTER(cleaned_healthcare_dataset,
            cleaned_healthcare_dataset[Test_Results] = "Abnormal")
    ),
    COUNTROWS(cleaned_healthcare_dataset),
    0
) * 100
```

---

## Dashboard pages

### Page 1 — Executive Summary
![Executive Summary](screenshots/01_executive_summary.png)

The first thing anyone sees. Five KPI cards at the top (total patients, avg billing, avg stay, total revenue, emergency %), a monthly trend line going back to 2019, admission type breakdown as a donut, top conditions by volume as a horizontal bar, and test result split.

---

### Page 2 — Patient Demographics
![Patient Demographics](screenshots/02_patient_demographics.png)

Breaks down the patient population. Stacked bar for age group and gender, clustered bar for medical condition by gender, matrix for insurance provider vs avg billing (with teal gradient conditional formatting), and blood type distribution.

---

### Page 3 — Hospital Operations
![Hospital Operations](screenshots/03_hospital_operations.png)

More operational focus. Top 10 doctors by volume, hospital-wise average billing, a scatter of length of stay vs billing amount coloured by admission type, a matrix of medical condition vs avg stay, and a column chart of billing by admission type.

---

### Page 4 — Patient Detail (Drill-Through)
![Patient Detail](screenshots/04_patient_detail_drillthrough.png)

Right-click any condition on Page 1 → Drill through → this page. Filters down to individual patient records for that condition. Three KPI cards update automatically, and the table shows name, age, gender, doctor, hospital, billing, stay length, and test result. Back button returns to Page 1.

---

## Interactive features

| Feature | How it works |
|---|---|
| Date Range slicer | Between-style slider filters all pages by admission date |
| Medical Condition | Dropdown filter — narrows all visuals to one condition |
| Admission Type | Tile buttons — Emergency / Elective / Urgent |
| Insurance Provider | Dropdown — filters by payer |
| Hospital | Dropdown — isolate a single hospital's data |
| Drill-through | Right-click any condition bar → jump to patient detail |
| Cross-filtering | Click any chart slice → everything else on the page filters |

---

## What I found in the data

- Emergency admissions are at 32.93% — roughly 1 in 3 patients
- Average billing is ₹25,540 per patient across all admission types
- Patients stay an average of 15.5 days regardless of the condition
- The six main conditions (Arthritis, Asthma, Cancer, Diabetes, Hypertension, Obesity) are almost perfectly evenly distributed — about 9,100–9,200 patients each
- Test results are split almost equally between Normal, Abnormal, and Inconclusive — which is worth flagging as unusual in a real hospital setting

---

## Design

Dark clinical theme throughout. Canvas background is `#0A0E1A`, visual backgrounds are `#111827`, accent and borders use `#06B6D4` teal. Emergency and abnormal metrics use `#EF4444` red. All fonts are Segoe UI.

I wanted it to look like something you'd actually see on a hospital operations screen — not a default Power BI report with the blue and orange theme everyone ships.

---

## How to run it yourself

You need Python 3.10+ and Power BI Desktop (free).

```bash
# 1. clone the repo
git clone https://github.com/yourusername/healthcare-powerbi-dashboard.git

# 2. install pandas if you don't have it
pip install pandas

# 3. download the dataset from Kaggle and put it in DATA/raw/

# 4. run the cleaning script
python Python/02_clean.py

# 5. open Healthcare_Dashboard.pbix in Power BI Desktop
# 6. update the data source path to your local cleaned CSV
```

---

## About me

I'm Basudev Panga, a BSc Data Science graduate from Mulund College of Commerce, University of Mumbai (2025). I'm actively looking for data analyst roles in Mumbai and Bengaluru.

Microsoft PL-900 certified. IBM DevOps Fundamentals certified.

I work across Python, SQL, Power BI, Tableau, Looker Studio, and have some experience with GCP BigQuery and Streamlit deployments.

(https://www.linkedin.com/in/basudev-panga)) • [GitHub](https://github.com/dataanalyst1108)

---

