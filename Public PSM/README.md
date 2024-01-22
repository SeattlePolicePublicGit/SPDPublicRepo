# PSM (Propensity Score Matching) - Behavioral Disparity (Race)

## Description

The goal of the PSM Project is to render robust estimates of disparate outcomes in investigative stops. To accomplish this, propensity scores are generated and used to weight treatment "Non-White" and control "White" observations (i.e., stops) to create a quasi experimental condition where all things being equal, the preceived race of the subject of the stop is the only variable. Time of day, day of week, location, incident type, and other measures reflecting prospective influences on officers perception of dangerousness are balanced. A more comprehensive process is used for internal performance management purposes as part of the departments Equity, Accountabiliy and Quality (EAQ) program. This version is configured to run public data as a demonstration of the technique and does not consider all measures.   

Propensity Score Matching (PSM) (or weighting in our case) is a technique to identify statistical anomalies between test and control populations of data. It is important to note that this is not a predictive model but a form of statistical preprocessing, designed to achieve a condition similar to a Randomized Controlled Trial (RCT). 

Source data is public Terry Stops data found at [Terry Stops Public Data](data.seattle.gov/Public-Safety/Terry-Stops/28ny-9ts8).

## Getting Started

### Dependencies

* Jupyter Notebook is required to run the PSM code

### Installing

* Download source Terry Stops data from [Terry Stops Public Data](data.seattle.gov/Public-Safety/Terry-Stops/28ny-9ts8) and save it as _Terry_Stops.csv_

### Executing program

PSM has two main Python notebooks to execute. Details for executing each notebook are in _PublicPSMFeatureEngineeringDocumentation_ and _PublicPSMModellingDocumentation_

1. Data and Feature Engineering: _public_psm_feature_engineering.ipynb_ 
    * Main code for running feature engineering. This notebook uses functions from public_psm_commonfunctions.py.
    * Imports source data Terry_Stops.csv and outputs model_features.csv

2. Modelling: _public_psm_app.ipynb_
    * Main code for running the PSM model. This notebook uses functions from public_acn_psm.py.
    * Imports model_features.csv and outputs results files propensities_results.csv and summaries_results.csv.