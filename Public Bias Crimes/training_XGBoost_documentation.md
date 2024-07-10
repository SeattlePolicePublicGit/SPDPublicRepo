# Bias Events - XGBoost Training

## Source Data and Objects

- train_final.csv (created in training_feature_engineering)
- test_final.csv (created in training_feature_engineering)
- countvectorizer.pkl (trained vectorizer from training_feature_engineering)

## Classification with XGBoost

SPD's fully productionized classification pipeline uses __[AWS' XGBoost built-in algorithm](https://docs.aws.amazon.com/sagemaker/latest/dg/xgboost.html)__. The data input of this algorithm requires 'rows representing observations, one column representing the target variable or label, and the remaining columns representing features.' If using columnar input and .csv format, the first column must be the label and the input should not have headers. 

We use asynchronous training and __[hyperparameter tuning jobs](https://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-ex-tuning-job.html)__ in AWS Sagemaker. We specifically implement __[Bayesian Optimization Hyperparameter Tuning](https://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-how-it-works.html)__.

For the sake of replication we show how to train your model locally using __[DMLC XGBoost](https://xgboost.readthedocs.io/en/stable/index.html)__ and __[scikit-optimize BayesSearchCV](https://scikit-optimize.github.io/stable/modules/generated/skopt.BayesSearchCV.html)__.

We heavily borrow the tuning implementation code from __[this tutorial](https://towardsdatascience.com/binary-classification-xgboost-hyperparameter-tuning-scenarios-by-non-exhaustive-grid-search-and-c261f4ce098d)__.

Our application's tuning and training strategies were selected based on the amount of data we work with and other data and computational efficiency considerations. The sizes of the example datasets are relatively small, creating issues with overfitting, hyperparameter sensitivity to subsamples and high variance, unreliable performance metrics, as well as poor generalization, when applying the same strategies we use on SPD's larger datasets. 

Again, we provide this code for demonstration purposes. Careful consideration should be given to your application's specific conditions and applicable best practices.

### *Class Imbalance*

Although not a problem with the example data, SPD's training dataset is highly imbalanced given that events with bias elements account for a very small portion of overall crime. We therefore train, tune hyperparameters, and select a classification threshold that optimize the F-1 score, to prioritize the correct classification of the minority class.

## Output

- Trained XGBoost model object used for inference.
- Optimal classification threshold used for inference.