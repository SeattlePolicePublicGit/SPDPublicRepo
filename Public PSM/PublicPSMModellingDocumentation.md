## Public PSM - Modelling
### Using XGBoost as estimator
Using XGBoost we split test and control along white/non-white for “Subject Perceived Race”, fit the model, extract probability, and then compute propensity.

1.  Filter the dataset based on a temporal (Year, Month) axis.

2.  Filter the dataset on a geospatial (Precinct) axis.

3.  Instantiate the Accenture model object.

4.  Load the filtered dataframe (created in steps 1 and 2) into the object.

5.  Choose the column and value to use to create the Test and Treatment labels. In this example we use the column "Subject Perceived Race" and the value "White". This means that:

    * any row with "White" in Subject Perceived Race will be given label 0.

    * any row with any other value (including blank, NaN, None) will be given label 1.

6.  Separate our X (features) and y (labels) into two new dataframes. Choosing which columns to drop from the features list. In the example below, we drop:

    * From X:
        * Subject Perceived Race
        * label
        * Terry Stop ID
        * Subject ID
        * GO / SC Num

    * For y, we use:
        * label

7.   Create the categorical and continuous pipelines and combine them into a processor.

8.   Create the XGBoost classifier.

9.   Convert X and y into matrices.

10.  Fit the classifier on X and y.

11.  Calculate the predictions and the probabilities for each row.

12.  Generate propensity weights.

13.  Review the output.