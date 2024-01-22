## Public PSM - Data & Feature Engineering
### Source Data
Terry_Stops.csv
data.seattle.gov/Public-Safety/Terry-Stops/28ny-9ts8
### Engineered Dataset / Abstracted Layer for Propensity Estimation:
#### Columns that exist in the raw dataset: 
 'Subject Age Group', 
 'Subject ID', 
 'GO / SC Num', 
 'Terry Stop ID', 
 'Stop Resolution', 
 'Weapon Type', 
 'Officer ID', 
 'Officer YOB', 
 'Officer Gender', 
 'Officer Race', 
 'Subject Perceived Race', 
 'Subject Perceived Gender', 
 'Reported Date',
 'Reported Time', 
 'Initial Call Type', 
 'Final Call Type', 
 'Call Type', 
 'Officer Squad', 
 'Arrest Flag', 
 'Frisk Flag', 
 'Precinct', 
 'Sector', 
 'Beat'
 
#### Engineered features in the abstraction layer:
 'weapon_type',
 'weapon_count',
 'observation_datetime_d',
 'observation_year_d'
 'observation_month_d',
 'observation_day_d',
 'observation_week_d',
 'observation_time_d',
 'observation_week_of_month_d',
 'watch', #calculated based on either precinct descriptions or time of event
 'precinct_watch',
 'n_person_stopped_3M',
 'n_person_stopped_6M',
 'n_person_stopped_1Y',
 'n_person_stopped_2Y',
 'n_person_stopped_3Y',
 'n_person_stopped_in_precinct_3M',
 'n_person_stopped_in_precinct_6M',
 'n_person_stopped_in_precinct_1Y',
 'n_person_stopped_in_precinct_2Y',
 'n_person_stopped_in_precinct_3Y',
 'n_race_stopped_in_precinct_3M',
 'n_race_stopped_in_precinct_6M',
 'n_race_stopped_in_precinct_1Y',
 'n_race_stopped_in_precinct_2Y',
 'n_race_stopped_in_precinct_3Y',
 'n_stops_in_precinct_3M',
 'n_stops_in_precinct_6M',
 'n_stops_in_precinct_1Y',
 'n_stops_in_precinct_2Y',
 'n_stops_in_precinct_3Y',
 'percent_race_stopped_in_precinct_3M',
 'percent_race_stopped_in_precinct_6M',
 'percent_race_stopped_in_precinct_1Y',
 'percent_race_stopped_in_precinct_2Y',
 'percent_race_stopped_in_precinct_3Y',
 'n_race_stopped_by_officer_3M',
 'n_race_stopped_by_officer_6M',
 'n_race_stopped_by_officer_1Y',
 'n_race_stopped_by_officer_2Y',
 'n_race_stopped_by_officer_3Y',
 'n_stops_by_officer_3M',
 'n_stops_by_officer_6M',
 'n_stops_by_officer_1Y',
 'n_stops_by_officer_2Y',
 'n_stops_by_officer_3Y',
 'percent_race_stopped_by_officer_3M',
 'percent_race_stopped_by_officer_6M',
 'percent_race_stopped_by_officer_1Y',
 'percent_race_stopped_by_officer_2Y',
 'percent_race_stopped_by_officer_3Y',
 'n_person_stopped_by_officer_3M',
 'n_person_stopped_by_officer_6M',
 'n_person_stopped_by_officer_1Y',
 'n_person_stopped_by_officer_2Y',
 'n_person_stopped_by_officer_3Y',
 'n_person_stopped_officer_frisk_3M',
 'n_person_stopped_officer_frisk_6M',
 'n_person_stopped_officer_frisk_1Y',
 'n_person_stopped_officer_frisk_2Y',
 'n_person_stopped_officer_frisk_3Y',
 'n_person_stopped_precinct_weapon_3M',
 'n_person_stopped_precinct_weapon_6M',
 'n_person_stopped_precinct_weapon_1Y',
 'n_person_stopped_precinct_weapon_2Y',
 'n_person_stopped_precinct_weapon_3Y',
 'n_person_stopped_by_officer_weapon_3M',
 'n_person_stopped_by_officer_weapon_6M',
 'n_person_stopped_by_officer_weapon_1Y',
 'n_person_stopped_by_officer_weapon_2Y',
 'n_person_stopped_by_officer_weapon_3Y'

### Output Data - Disparities Calculated by Model
#### Output Schema:

'watch_d', 'Precinct_watch_d', 'observation_datetime_d', 'observation_day_d', 'observation_week_d', 'observation_week_of_month_d', 'Officer Race', 'Subject Perceived Race', 'subject_race_label_d', 'subject_race_label_pred', 'probability_0_pred', 'probability_1_pred', 'weight_pred', 'mean_control_pred', 'mean_treat_pred', 'mean_control_sum_pred', 'mean_treat_sum_pred', 'disparity_pred', 'run_timestamp', 'Frisk Flag', 'Subject Age Group', 'Subject Perceived Race'

watch_d
precinct_watch_d
observation_datetime_d 
observation_day_d
observation_week_d
observation_week_of_month_d
Officer Race
Subject Perceived Race
Subject_race_label_d
Subject_race_label_pred
Probability_0_pred
probability_1_pred
weight_pred
mean_control_pred
mean_treat_pred
mean_control_sum_pred
mean_treat_sum_pred
disparity_pred
run_timestamp
Frisk Flag
Subject Age Group
Subject Perceived Race