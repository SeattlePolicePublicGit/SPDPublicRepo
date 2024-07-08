# Bias Events - Feature Engineering for Inference

## Source Data and Objects
- incident_offense.csv
- final_reports.csv
- narratives.csv
- countvectorizer.pkl (trained vectorizer from training_feature_engineering)

## Engineered Features

141 resulting features including:

- 'victim_age_1','subject_age_1','East', 'North', 'precinct_OOJ', 'South', 'Southwest', 'West', 'precinct_Unknown',
 'Female','Gender Diverse (gender non-conforming and/or transgender)', 'Male', 'Vic_Gender_Unknown',
 'American Indian or Alaska Native', 'Asian', 'Black or African American', 'Native Hawaiian or Other Pacific Islander',
 'Vic_Race_Unknown', 'White', 'Hispanic Or Latino', 'Not Hispanic Or Latino', 'Vic_Ethni_Unknown',
 'subject_American Indian or Alaska Native', 'subject_Asian', 'subject_Black or African American',
 'subject_Native Hawaiian or Other Pacific Islander', 'subject_Sub_Race_Unknown', 'subject_White',
 'subject_Female', 'subject_Gender Diverse (gender non-conforming and/or transgender)',
 'subject_Male', 'subject_Sub_Gender_Unknown', 'subject_Hispanic Or Latino', 'subject_Not Hispanic Or Latino',
 'subject_Sub_Ethni_Unknown', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3', 'D1', 'D2', 'D3', 'E1', 'E2', 'E3', 'F1', 'F2',
 'F3', 'G1', 'G2', 'G3', 'H1', 'H2', 'H3', 'J1', 'J2', 'J3', 'K1', 'K2', 'K3', 'L1', 'L2', 'L3', 'M1', 'M2', 'M3',
 'N1', 'N2', 'N3', 'O1', 'O2', 'O3', 'Q1', 'Q2', 'Q3', 'R1', 'R2', 'R3', 'S1', 'S2', 'S3', 'U1', 'U2', 'U3',
 'beat_Unknown', 'W1', 'W2', 'W3', 'beat_OOJ'
 <br>
 
- 50 text features

## Main Dataset Description

The 'incident_offense.csv' file is a dummy dataset of SPD's incident_offense dataset, which contains a row per every unique offense in SPD's historical data. The offense_id column is a unique identifier for every offense. The original dataset has 3.9 million rows (offenses) and is updated daily, which increases the size of the dataset.

The dummy dataset was created with randomly generated unique identifiers. To minimize processing time, it only includes 39 rows. The dataset additionally includes columns for:

- __Report ID__: unique identifier of report where the offense was recorded.
- __Reporting event number__: unique identifier of event associated to the offense.
- __Suspect (subject) demographics__: A column is included for age, ethnicity, gender, and race
- __Victim demographics__: A column is included for age, ethnicity, gender, and race.
- __Event start date__: the date and time of occurrence.
- __Approval status__: the status of report approval, which can include 'Draft,' 'Rejected,' 'Pending Supervisor Review,' 'UCR Approved,' and 'Completed.' We only use approved/completed reports for training as other status indicates that reports might be modified/corrected.
- __Report submitted date__: The date on which report was modified/completed. We use this column to obtain the date after which new reports are read every 24 hours.
- __Report UCR Approved By__: The ID of the person that last approved the report. We use this column to filter out reports that have already been modified by the Bias Crime Unit.
- __Precinct__: precinct where event occurred.
- __Beat__: beat where event occurred. Beats are geographic divisions to which patrol officers are assigned. 
- __Crime Description__: The description of the first offense code in the report.

## Data Output

Since there is a separate process for feature engineering for training occurring every month that updates the dataset with all reports ever submitted, the output table from this notebook is regenerated and rewritten on a daily basis.