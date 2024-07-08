# Bias Events NLP (Natural Language Processing) Classification Tool

## Description

The Bias Events Natural Language Processing (NLP) binary classifier is a machine learning algorithm that uses narratives and demographics from incident and offense (I/O) reports to determine whether a report contains bias elements or not. The goal of the tool is to improve the accuracy of hate crime data and the speed at which incidents with bias elements are identified. 

### *SPD Data Tracking*

SPD’s policy 15.120 outlines the documentation process of bias crimes and incidents in an offense report (Seattle Police Department, 2024). Patrol officers and a sergeant are dispatched to the scene, where the officers investigate the incident and write a report, identifying the appropriate type of bias event, which is reviewed by the patrol sergeant. The policy defines three different types of bias events:

- __Hate crime offense and malicious harassment__: Crimes in which the motivation for the suspect targeting a particular person was based on their belief about the victims' race, color, religion, national origin, sexual orientation, mental, physical, or sensory handicap, homelessness, marital status, age, parental status, gender, or political ideology.
- __Crimes with bias elements__: An event in which a crime is committed that is not bias-based and during the incident the suspect uses derogatory language directed at the victim's protected status or group.
- __Bias incident__: Offensive derogatory comments directed at a person's sexual orientation, race, or other protected status which cause fear and/or concern in the targeted community during a non-criminal incident.
 
Currently, officers use offense fields and other reporting fields in the Mark43 record management system (RMS) to indicate if an event contains bias elements. As such, reports in the training data are assigned a positive label (1) based on these fields.

We productionize the bias crime classification pipeline using AWS services for computational processing efficiency. However, to allow for replication and demonstration, we adjust the code in this repository to use free python modules/packages.

Briefly, every 24 hours, newly submitted I/O reports are passed through:

1. The ‘feature_engineering_inference’ job, where demographic and text features are extracted. The specific process is described in ‘feature_engineering_inference_documentation.’
2. The ‘daily_predictions’ job, where predicted labels are generated for each report using the trained classification model.
3. Although not provided in this repository, a call is made to a Mark43 API to create a task for every report associated to a positive prediction. We discuss a more manual alternative in the feature_engineering_training_documentation.

Every month:

1. The bias crimes data source is passed through the ‘feature_engineering_for_training’ job. The specific process is described in ‘feature_engineering_training_documentation.’
2. The classification model is retrained with the extended dataset in the ‘XGBOOST_training’ job. The specific process is described in ‘model_training_documentation.’

Note that we have two separate jobs for feature engineering, one for training and one for inference. The feature engineering for training uses a data source that is specifically built for training the classification model. This data source is created through a similar transformation/pivoting of offenses as the one performed in the feature engineering process for inference. We create separate processes given the data processing load size required to generate the training dataset, which is generated only once a month through an AWS Glue job.

## Getting Started

### *Dependencies*

- Jupyter Notebooks/Python IDLE

### *Required Files*

The following .csv files are provided:

- dummy_narrative_github.csv
- incident_offense.csv
- narratives.csv
- train_report_ids.csv
- test_report_ids.csv
- completed_tasks.csv
- offenses.csv
- final_reports.csv

### *Code Execution*

The bias crime identification tool is broken down into four Python notebooks: bias_crime_feature_engineering_for_training_github, bias_crime_feature_engineering_for_inference_github, bias_crime_XGBOOST_training_github, and bias_crime_XGBOOST_daily_predictions_github. Detailed descriptions are included in training_XGBoost_documentation, feature_engineering_training_documentation, and feature_engineering_inference_documentation. 

The NLP_Preprocessing.py file defines NLP preprocessing functions used for feature engineering.