<p align="center">
  <img src="https://raw.githubusercontent.com/hanestuamante/OCD-Patient-Analysis-System/91d5fbf015f045699cc195df2523ff7780f2c885/The%20OCD%20Cycle.jpeg" width="500" alt="The OCD Cycle">
</p>


## Executive Summary

This project analyzes clinical OCD patient records to identify high-risk
segments, symptom association patterns, and operational signals for better care
triage. It uses a reproducible Python pipeline with data validation, feature
engineering, clustering, statistical testing, and executive-ready reporting.
The business value is clearer prioritization: focus clinical capacity on the
patient groups most likely to need intensive follow-up.

## Business Problem

OCD care teams often have limited visibility into which patient groups require
earlier intervention, closer follow-up, or deeper intake review. This project
turns raw patient data into a decision-support workflow that answers:

- Which patient segments show the highest symptom severity?
- Do demographic or clinical groups differ meaningfully in Y-BOCS scores?
- Which obsession and compulsion types frequently appear together?
- How should findings translate into care operations and ROI?

## Methodology

The workflow follows CRISP-DM:

1. Business Understanding: Define triage, severity, and capacity-planning goals.
2. Data Understanding: Inspect demographics, clinical scores, symptom types, and
   diagnosis timeline fields.
3. Data Preparation: Validate schema and ranges, clean categories, remove
   duplicate patients, and create Y-BOCS severity features.
4. Modeling: Segment patients with K-Means and mine symptom association rules
   with Apriori.
5. Evaluation: Use cluster profiles, ANOVA, p-values, and symptom-rule lift to
   separate evidence from noise.
6. Deployment: Export figures, run a Streamlit dashboard, and document
   actionable recommendations.

## Tech Stack

- Python 3.10+: pandas, NumPy, SciPy, scikit-learn
- Visualization: matplotlib, seaborn, NetworkX, Streamlit
- Pattern Mining: mlxtend Apriori association rules
- Data Access: SQLAlchemy, PyMySQL, MySQL connector
- Workflow: modular `src/` package, CLI pipeline, validation script

## Project Architecture

```text
OCD-Patient-Analysis-System/
├── app.py
├── main.py
├── requirements.txt
├── config/
│   ├── data_schema.yml
│   ├── project.yml
│   └── sql/
│       └── analysis_queries.sql
├── data/
│   ├── raw/
│   ├── processed/
│   └── external/
├── notebooks/
│   ├── exploration/
│   │   └── 1.0-eda-exploration.ipynb
│   ├── modeling/
│   │   └── 2.0-clustering-analysis.ipynb
│   └── visualization/
├── reports/
│   ├── figures/
│   ├── final/
│   ├── presentations/
│   └── ocd_strategic_insights.md
├── scripts/
│   └── validate_data.py
└── src/
    ├── analysis.py
    ├── cleaning.py
    ├── data_loader.py
    ├── features.py
    ├── pipeline.py
    ├── validation.py
    ├── visualization.py
    └── visualizer.py
```

## Key Findings

- Patient clustering creates interpretable risk segments based on age, total
  Y-BOCS score, and family-history signal.
- Marital-status ANOVA is used to test whether group-level Y-BOCS differences
  are statistically meaningful before turning them into recommendations.
- Symptom association rules reveal likely obsession-compulsion pairings that
  can improve intake forms and clinician review checklists.
- The most useful business metric is not only model output; it is the ability to
  prioritize high-severity cohorts and reduce avoidable manual review time.

## Actionable Insights

- Prioritize outreach for the cluster with the highest average Y-BOCS score.
- Monitor Extreme severity rate as a care-capacity and staffing signal.
- Use high family-history concentration to guide earlier screening and patient
  education.
- Add top symptom associations to intake review prompts.
- Pair every statistical result with an operational decision and measurement
  plan, such as reduced missed follow-ups or faster triage review.

## Usage Instructions

Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Validate a raw CSV before analysis:

```bash
python3 scripts/validate_data.py data/raw/ocd_patient_dataset.csv
```

Run the full pipeline from CSV:

```bash
python3 main.py --csv-path data/raw/ocd_patient_dataset.csv
```

Run the full pipeline from MySQL:

```bash
export OCD_DATABASE_URL="mysql+pymysql://user:password@host:3306/ocd_analysis"
python3 main.py
```

Launch the dashboard:

```bash
streamlit run app.py
```

## Data Governance

Raw and processed data are ignored by Git by default. Keep sensitive clinical
records in `data/raw/` locally or in a governed storage layer, never in source
control. Commit only code, configuration, notebooks, documentation, and
non-sensitive aggregate report artifacts.

## Key Metrics Guide

- Retention Rate: Use when longitudinal follow-up data exists. Report cohort
  size, retained count, retention rate, and movement versus prior cohort.
- ROI: Use operational savings or clinical throughput assumptions:
  `ROI = (benefit - cost) / cost`.
- SHAP Values: Add if a supervised risk model is introduced. Present global
  drivers, local case explanations, and a caveat that SHAP explains model
  behavior rather than causality.
- Cluster Metrics: Always show patient count, average age, average Y-BOCS score,
  family-history rate, and Extreme severity rate.
