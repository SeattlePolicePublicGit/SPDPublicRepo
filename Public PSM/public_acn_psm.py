from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sqlalchemy import column
import pandas as pd
from datetime import datetime
import xgboost as xgb
import logging
import time, os

region = "us-gov-west-1"

# set time zone
os.environ['TZ'] = 'US/Pacific'

class xgb_psm():
    """Custom Propensity Scoring Class using XGBoost.
    Authors: Carl Sharpe, Greg Ridgeway, Loren Atherley, Emma Heo
    This class uses XGboost to generate propensity scores for binary separable 
    data with multiple categorical and/or continuous variables. Created in 
    partnership with Seattle Police Department, the People's Republic of Carl Sharpe, 
    the Best of the Bests Emma Heo, and the University of Pennsylvania, the initial goal is to identify the 
    propensity score for white/non-white subjects who interact with the police.

    key variables:
    self.data: the dataframe loaded into the object
    self.X: dataframe of X features
    self.y: dataframe of y labels
    self.full_processor: the full sklearn processor with categorical and 
                         continuous variables
    self.evaluated_data: data with propensity scores, probabilities, and 
                         predictions
    XGBoost Classifier:
    self.xgb_cl

    Order of Execution:
    1. evaluator = xgb_psm(): Construct object 
    2. evaluator.load_dataframe(dataframe)
    3. evaluator.create_labels(label_col, label_val)
    4. evaluator.separate_X_y(drop_cols, y_col)
    5. evaluator.create_pipeline()
    6. evaluator.process_X_y()
    7. evaluator.fit_xgb()
    8. evaluator.predict()
    9. evaluator.generate_weights()
    
    To-Do:
    - Add more error handling around badly ordered operations will give generic errors.
    - Add more debugging.
    - Enable more configuration for the classifier constructor.
    - Enable more customization for fitting data to support test/train splits.

    """
    def __init__(self, verbosity=0):
        """Constructs the class, sets the verbosity (default 0). Uses Pythons'
        native logging capability
        verbosity = 1 <-- Warn
        verbosity = 2 <-- Info
        verbosity = 3 <-- Debug
        """
        logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt="%m/%d/%Y %I:%M:%S %p %Z")
        self.logger = logging.getLogger("Jarvis")
        if verbosity == 3:
            self.logger.setLevel(logging.DEBUG)
            self.logger.debug("Verbosity set to DEBUG")
        if verbosity == 2:
            self.logger.setLevel(logging.INFO)
            self.logger.info("Verbosity set to INFO")
        if verbosity == 1:
            self.logger.setLevel(logging.WARN)
            self.logger.warn("Verbosity set to WARN")
        if verbosity == 0:
            self.logger.setLevel(logging.ERROR)
        self.data = ""

    def load_dataframe(self, df):
        """
        loads the dataframe to be evaluated into self.data
        """
        if isinstance(df, pd.DataFrame):
            self.data = df
        else:
            print(
                "Passed variable not a dataframe... Please pass a dataframe.")

    def assign_label(self, input_label, value):
        """Method that takes the input label and assigns a 0 if match and 
        1 if non-match. Designed for performance to work with dataframe.map() and 
        lambda. See create_labels() for more info."""
        if input_label == value:
            return 0
        else:
            return 1

    def create_labels(self, source_column, label_value, label_col):
        """Creates the labels for the test and control groups. Used in conjunction 
        with assign_label()"""
        self.data[label_col] = self.data[source_column].map(
            lambda x: self.assign_label(x, label_value))

    def separate_X_y(self, X_drop_cols, y_col):
        """Separated X and y into discreet dataframes. Drops X_cols as requested."""
        columns = X_drop_cols
        columns.append(y_col)
        columns = list(set(columns))
        result = [item for item in columns if (item not in self.data.columns)]
        if len(result) > 0:
            print("The following column name(s) were not found:")
            for item in result:
                print(item)
            print(
                f"If one of these colums is {y_col} then try running make_labels before running this"
            )
        else:
            self.X = self.data.drop(columns=X_drop_cols)
            self.y = self.data[y_col]

    def create_pipeline(self):
        """Creates full processor by interrogating the X dataframe types for numeric and non-numeric
        datatypes to create categorical and continuous encoders."""
        if isinstance(self.data, pd.DataFrame):
            self.categorical_pipeline = Pipeline(steps=[
                ("impute", SimpleImputer(strategy="most_frequent")),
                ("oh-encode",
                 OneHotEncoder(handle_unknown="ignore", sparse=False)),
            ])
            self.numeric_pipeline = Pipeline(
                steps=[("impute", SimpleImputer(
                    strategy="mean")), ("scale", StandardScaler())])

            cat_cols = self.X.select_dtypes(exclude="number").columns
            num_cols = self.X.select_dtypes(include="number").columns

            self.full_processor = ColumnTransformer(transformers=[
                ("numeric", self.numeric_pipeline, num_cols),
                ("categorical", self.categorical_pipeline, cat_cols),
            ])
        else:
            print(
                "Object does not contain a dataframe, please use load_dataframe to load a dataframe"
            )

    def create_xgb(self, verbosity=0):
        """Constructs the XGBoost classifier. Parameters provided by Greg Ridgeway."""
        self.xgb_cl = xgb.XGBClassifier(max_depth=2,
                                        n_estimators=3000,
                                        objective="binary:logistic",
                                        learning_rate=0.01,
                                        eval_metric='logloss',
                                        verbosity=verbosity,
                                        use_label_encoder=False)

    def process_X_y(self):
        """Converts X and y dataframes to matrices to prepare them for fitting into the classifier"""
        self.X_processed = self.full_processor.fit_transform(self.X)
        self.y_processed = SimpleImputer(
            strategy="most_frequent").fit_transform(
                self.y.values.reshape(-1, 1))

    def fit_xgb(self):
        """Fits the classifier on X_processes and y_processed"""
        self.xgb_cl.fit(self.X_processed, self.y_processed, verbose=2)

    def predict(self):
        """Runs the prediction and probability calculations for the fitted classifier
        against X_processed and y_processed and stores them in:
        - evaluated_data: the original dataframe, and
        - prediction the binary prediction
        - probability_0: the probability that the prediction is 0
        - probability_1: the probability that the prediction is 1"""

        self.predictions = self.xgb_cl.predict(self.X_processed)
        self.probabilities = self.xgb_cl.predict_proba(self.X_processed)
        self.evaluated_data = self.data.copy()
        self.evaluated_data['prediction'] = self.predictions
        self.evaluated_data['probability_0'] = self.probabilities[:,
                                                                  0].tolist()
        self.evaluated_data['probability_1'] = self.probabilities[:,
                                                                  -1].tolist()

    def generate_weights(self, label_col):
        self.evaluated_data['weight'] = self.evaluated_data.apply(
            lambda x: 1 if x[label_col] == 1 else x['probability_1']/(1-x['probability_1']), axis = 1
        )

    def extract_model_weights(self):
        """Extracts the model weights from the fitted classifier and converts 
        them back into the original label names for human readability."""

        features = self.X.columns
        feature_map = self.full_processor.transformers_[1][1][
            'oh-encode'].get_feature_names(features).tolist()
        self.xgb_cl.get_booster().feature_names = feature_map
        feature_important = self.xgb_cl.get_booster().get_score(
            importance_type='weight')
        keys = list(feature_important.keys())
        values = list(feature_important.values())
        self.model_weights = pd.DataFrame(data=values,
                                          index=keys,
                                          columns=["weight"]).sort_values(
                                              by="weight", ascending=True)
    
    def absolute_difference(self, label_col):
        """
        The absolute difference is calculated at a per row basis per exsperiment. 
        The sum because it should be summed over each exsperiment?

        Function return the absolute difference:

        mean_control = sum((1-label)*weight*frisk) / sum((1-label)*weight)
        mean_treat = sum(label*frisk) / sum(label)
        
        absolute_difference = mean_treat - mean_control
        
        The sum is done per experiment. 
        """
        frisk_conversion = {'Y': 1,'N': 0}
        frisk = self.evaluated_data["Frisk Flag"].map(frisk_conversion)
        weight = self.evaluated_data['weight']
        label = self.evaluated_data[label_col]

        mean_control = (1-label)*weight*frisk / (1-label)*weight    
        mean_treat = (label*frisk) / label

        #     (0*1)/0 results in NAN value  
        self.evaluated_data['mean_control'] = mean_control.fillna(0)
        self.evaluated_data['mean_treat'] = mean_treat.fillna(0)

        self.evaluated_data["mean_control_sum"] = self.evaluated_data['mean_control'].sum()
        self.evaluated_data["mean_treat_sum"] = self.evaluated_data['mean_treat'].sum()
        self.evaluated_data["absolute_difference"] = self.evaluated_data["mean_treat_sum"] - self.evaluated_data["mean_control_sum"]

    def just_send_it(self, df, control_col, control_val, drop_cols, label_col):
        """Automatically runs all the required methods to prep the data, fit the 
        model, calculate the predictions and the probabilities, and the feature
        weights."""

        self.logger.info("Loading Dataframe")
        self.load_dataframe(df)
        self.logger.info("Creating Labels")
        self.create_labels(control_col, control_val, label_col)
        self.logger.info("Separating X and y")
        self.separate_X_y(drop_cols, label_col)
        self.logger.info("Creating Pipelines")
        self.create_pipeline()
        self.logger.info("Creating XGBoost Classifier")
        self.create_xgb()
        self.logger.info("Converting X and y to matrices")
        self.process_X_y()
        self.logger.info("Fitting Classifier on X and y")
        self.fit_xgb()
        self.logger.info("Calculating Predictions and Probabilities")
        self.predict()
        self.logger.info("Generating Weights")
        self.generate_weights(label_col)
        self.logger.info("Calculating absolute difference")
        self.absolute_difference(label_col)


def evaluate_all_stops(df):
    """Function tightly coupled to the xgb_psm class that enables bulk processing
    of all records in a given dataframe. Currently scoped to Precinct, Year, Month 
    intervals. 

    Args:
        df (pandas dataframe): the dataframe to be evaluated

    Returns:
        summary_df: a summary dataframe of the experiments that include:
                    - Precinct
                    - Year
                    - Month
                    - Total Records
                    - Attempted to Assess
                    - Label 0 Records
                    - Label 1 Records
                    - Run time
        propensity_df: a dataframe that includes the original input dataframe and
                       adds the following columns:
                       - Prediction
                       - Probability 0
                       - Probability 1
                       - PSM Weight

    """

    # Initialize the summary_df dataframe
    summary_df = pd.DataFrame({
        'total_records': pd.Series(dtype='int'),
        'attempted_to_assess': pd.Series(dtype='str'),
        'label_0_records_count': pd.Series(dtype='int'),
        'label_1_records_count': pd.Series(dtype='int'),
    })

    propensity_df = pd.DataFrame()

    # Setting up the default variables.

    control_col = 'Subject Perceived Race'
    control_val = 'White'
    drop_cols = [
        'Subject Perceived Race', 'GO / SC Num', 'Terry Stop ID',
        'Subject ID'
    ]
    label_col = 'label'
    print(f"Found {len(df)} potential records to evaluate...")

    precincts = ["NORTH", "EAST", "SOUTH", "WEST", "SOUTHWEST"]
    # Filter on Precinct
    time_assessed = datetime.today()
    for precinct in precincts:
        precinct_df = df[df.precinct == precinct]
        years = precinct_df.observation_year_d.unique()
        # Filter on year
        for year in years:
            year_df = precinct_df[precinct_df.observation_year_d == year]
            months = year_df.observation_month_d.unique()
            # Filter on Month
            for month in months:
                month_df = year_df[year_df.observation_month_d == month]
                # Check if it has more than 10 records
                if len(month_df) > 10:
                    eval_flag = True
                    start_time = datetime.now()
                    evaluator = xgb_psm(verbosity=0)
                    
                    evaluator.just_send_it(month_df,
                                           control_col=control_col,
                                           control_val=control_val,
                                           drop_cols=drop_cols,
                                           label_col=label_col)
                    
                    run_time = datetime.now() - start_time
                    high_prop = evaluator.evaluated_data.weight.max()
                    low_prop = evaluator.evaluated_data.weight.min()
                    mean_prop = evaluator.evaluated_data.weight.mean()
                    assessed = "Yes"
                else:
                    # If you skip the evaluation of records, write out the
                    # flags appropriately
                    eval_flag = False
                    assessed = "No"
                    run_time = None
                    high_prop = None 
                    low_prop = None
                    mean_prop = None

                num_0 = month_df[month_df['Subject Perceived Race'] == "White"].shape[0]
                num_1 = month_df[month_df['Subject Perceived Race'] != "White"].shape[0]
                row = {
                    "total_records": len(month_df),
                    "attempted_to_assess": assessed,
                    "label_0_records_count": num_0,
                    "label_1_records_count": num_1,
                    "highest_propensity_pred": high_prop,
                    "lowest_propensity_pred": low_prop,
                    "mean_propensity_pred": mean_prop,
                    "run_time": str(run_time),
                    "run_timestamp": time_assessed
                }
                summary_df = summary_df.append(row, ignore_index=True)
                if eval_flag:
                    propensity_df = propensity_df.append(
                        evaluator.evaluated_data
                    )
                    propensity_df['run_timestamp'] = time_assessed
                else:
                    pass
    return eval_flag, summary_df, propensity_df