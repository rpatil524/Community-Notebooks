# How to build an RNA-seq logistic regression classifier

Check out other notebooks at our [Community Notebooks
Repository](https://github.com/isb-cgc/Community-Notebooks)!

-   **Title:** How to build an RNA-seq logistic regression classifier
-   **Author:** John Phan
-   **Created:** 2021-07-07
-   **Purpose:** Demonstrate a basic machine learning method to predict
    a cancer endpoint using gene expression data.
-   **URL:**
    <https://github.com/isb-cgc/Community-Notebooks/blob/master/MachineLearning/How_to_build_an_RNAseq_logistic_regression_classifier.Rmd>
-   **Note:** This example is based on the work published by [Bosquet et
    al.](https://molecular-cancer.biomedcentral.com/articles/10.1186/s12943-016-0548-9)

This notebook demonstrates how to build a basic machine learning model
to predict ovarian cancer treatment outcome. Ovarian cancer gene
expression data is pulled from a BigQuery table and formatted using
Pandas. The data is then split into training and testing sets to build
and test a logistic regression classifier using scikit-learn.

## Import Dependencies

``` r
library(bigrquery)
library(tidyr)
library(caret)
library(superml)
```

## Parameters

``` r
# set the google project that will be billed for this notebook's computations
google_project <- 'isb-project-zero'

# in this example, we'll be using the Ovarian cancer TCGA dataset
cancer_type <- 'TCGA-OV'

# gene expression data will be pulled from this BigQuery project
bq_project <- 'isb-cgc-bq'
```

## Get Gene Expression Data from BigQuery Table

Pull RNA-seq gene expression data from the TCGA RNA-seq BigQuery table
and join it with the clinical data table to create a labeled data frame.
In this example, we will label the samples based on therapy outcome.
“Complete Remission/Response” will be labeled as “1” while all other
therapy outcomes will be labeled as “0”. This prepares the data for
binary classification.

Prediction modeling with RNA-seq data typically requires a feature
selection step to reduce the dimensionality of the data before training
a classifier. However, to simplify this example, we will use a
pre-identified set of 33 genes (Bosquet et al. identified 34 genes, but
PRSS2 and its aliases are not available in the hg38 RNA-seq data).

``` r
# Build query to retrieve gene expression data
ge_query <- sprintf("
  SELECT
    ge.case_barcode AS sample,
    labels.response_label AS label,
    ge.gene_name AS gene_name,
    -- Multiple samples may exist per case, take the max value
    MAX(LOG(ge.HTSeq__FPKM_UQ+1)) AS gene_expression
  FROM `%s.TCGA.RNAseq_hg38_gdc_current` AS ge
  INNER JOIN (
    SELECT
      *
    FROM (
      SELECT
        case_barcode,
        primary_therapy_outcome_success,
        CASE
          -- Complete Reponse    --> label as 1
          -- All other responses --> label as 0
          WHEN primary_therapy_outcome_success = 'Complete Remission/Response' THEN 1
          WHEN (primary_therapy_outcome_success IN (
            'Partial Remission/Response','Progressive Disease','Stable Disease'
          )) THEN 0
        END AS response_label
        FROM `%s.TCGA_versioned.clinical_gdc_2019_06`
        WHERE
          project_short_name = '%s'
          AND primary_therapy_outcome_success IS NOT NULL
    )
  ) labels
  ON labels.case_barcode = ge.case_barcode
  WHERE gene_name IN ( -- 33 Gene signature, leave out PRSS2 (aka TRYP2)
    'RHOT1','MYO7A','ZBTB10','MATK','ST18','RPS23','GCNT1','DROSHA','NUAK1','CCPG1',
    'PDGFD','KLRAP1','MTAP','RNF13','THBS1','MLX','FAP','TIMP3','PRSS1','SLC7A11',
    'OLFML3','RPS20','MCM5','POLE','STEAP4','LRRC8D','WBP1L','ENTPD5','SYNE1','DPT',
    'COPZ2','TRIO','PDPR'
  )
  GROUP BY sample, label, gene_name
", bq_project, bq_project, cancer_type)

# Run the query
ge_table <- bq_project_query(google_project, ge_query, quiet = TRUE)

# Download the query result
ge_data <- bq_table_download(ge_table, quiet = TRUE)

# Show the dataframe
str(ge_data)
```

    ## tibble [8,712 × 4] (S3: tbl_df/tbl/data.frame)
    ##  $ sample         : chr [1:8712] "TCGA-25-1321" "TCGA-23-1022" "TCGA-WR-A838" "TCGA-10-0933" ...
    ##  $ label          : int [1:8712] 1 1 0 1 1 1 1 0 1 0 ...
    ##  $ gene_name      : chr [1:8712] "MATK" "PDGFD" "CCPG1" "PRSS1" ...
    ##  $ gene_expression: num [1:8712] 7.64 11.96 9.97 9.4 11.66 ...

## Reshape the Data

The data pulled from BigQuery is formatted such that each row
corresponds to a sample/gene combination. However, to use the data with
scikit-learn, it is more convenient to reshape the data such that each
row corresponds to a sample and each column corresponds to a gene. We’ll
use tidyr spread() function to pivot the data.

``` r
ge_data_pivot <- spread(ge_data, key = "gene_name", value = "gene_expression")
str(ge_data_pivot)
```

    ## tibble [264 × 35] (S3: tbl_df/tbl/data.frame)
    ##  $ sample : chr [1:264] "TCGA-04-1331" "TCGA-04-1341" "TCGA-04-1343" "TCGA-04-1347" ...
    ##  $ label  : int [1:264] 1 1 0 1 0 0 0 0 1 1 ...
    ##  $ CCPG1  : num [1:264] 10.5 10.6 10.9 10.7 10.2 ...
    ##  $ COPZ2  : num [1:264] 11.1 12 12.6 11.1 10.4 ...
    ##  $ DPT    : num [1:264] 10.01 10.22 11.12 9.65 6.81 ...
    ##  $ DROSHA : num [1:264] 12.3 12.5 11.8 12.2 12.4 ...
    ##  $ ENTPD5 : num [1:264] 10.78 10.35 10.41 9.97 11.52 ...
    ##  $ FAP    : num [1:264] 10.28 9.94 10.75 9.04 0 ...
    ##  $ GCNT1  : num [1:264] 12.59 9.11 9.79 10.76 10.62 ...
    ##  $ KLRAP1 : num [1:264] 11.37 10.55 9.74 10.46 9.82 ...
    ##  $ LRRC8D : num [1:264] 12.6 12.1 12.3 13 12.3 ...
    ##  $ MATK   : num [1:264] 8.5 10.12 11.18 7.92 8.17 ...
    ##  $ MCM5   : num [1:264] 12.7 12.3 12.6 12.6 11.8 ...
    ##  $ MLX    : num [1:264] 11.8 12.9 12.2 12.5 11.7 ...
    ##  $ MTAP   : num [1:264] 11.2 10.4 10.3 10.6 10.6 ...
    ##  $ MYO7A  : num [1:264] 8.26 11.44 9.63 8.87 9.13 ...
    ##  $ NUAK1  : num [1:264] 11.3 10.8 11.3 10.4 9.4 ...
    ##  $ OLFML3 : num [1:264] 12.9 12.5 13.3 14.1 11.9 ...
    ##  $ PDGFD  : num [1:264] 11.12 9.65 11.58 11.29 9.98 ...
    ##  $ PDPR   : num [1:264] 11.4 10.9 11.2 11.8 11.5 ...
    ##  $ POLE   : num [1:264] 11.9 11 11 11.2 10.5 ...
    ##  $ PRSS1  : num [1:264] 12.4 12.4 11.8 12.5 11.7 ...
    ##  $ RHOT1  : num [1:264] 11.3 11.4 11.2 11.8 11.7 ...
    ##  $ RNF13  : num [1:264] 12.5 12 12.2 12.5 12.3 ...
    ##  $ RPS20  : num [1:264] 16 17.7 16.9 17.6 17.7 ...
    ##  $ RPS23  : num [1:264] 13.8 16.1 16.2 15.8 16.2 ...
    ##  $ SLC7A11: num [1:264] 10.51 8.73 10.39 8.32 11.48 ...
    ##  $ ST18   : num [1:264] 5.03 0 6.02 4.84 5.02 ...
    ##  $ STEAP4 : num [1:264] 9.41 8.16 10.09 7.72 5.26 ...
    ##  $ SYNE1  : num [1:264] 9.05 8.48 8.86 8.53 7.52 ...
    ##  $ THBS1  : num [1:264] 12.3 12.4 13.1 12.3 11 ...
    ##  $ TIMP3  : num [1:264] 10.27 9.22 11.06 10.37 10.15 ...
    ##  $ TRIO   : num [1:264] 11.8 11.5 11.3 11.3 11.5 ...
    ##  $ WBP1L  : num [1:264] 12.7 12.7 13.1 13.1 13.6 ...
    ##  $ ZBTB10 : num [1:264] 11.9 11.7 11.5 11.1 12.6 ...

## Prepare the Data for Prediction Modeling

Prepare the data by splitting it into training and testing sets, and
scaling the data. It is important that prediction models are tested on
samples that are independent from the training samples in order to
accurately estimate performance.

``` r
# remove the sample names column from the data frame
ge_data_pivot_nosample <- subset(ge_data_pivot, select=-c(sample))

# use the caret createDataPartition function to create a balanced split of the data into train and test sets
set.seed(10)
train_rows = createDataPartition(ge_data_pivot_nosample$label, p=0.5, list=FALSE, times=1)
train_data <- ge_data_pivot_nosample[train_rows,]
test_data <- ge_data_pivot_nosample[-train_rows,]

# move labels to their own variables
train_y <- train_data$label
test_y <- test_data$label

# use caret's preProcess function to scale the data to 0 mean and unit variance
pre_proc_vals <- preProcess(subset(train_data, select=-c(label)), method=c('center', 'scale'))
train_x <- predict(pre_proc_vals, subset(train_data, select=-c(label)))
test_x <- predict(pre_proc_vals, subset(test_data, select=-c(label)))

# recombine the data and labels
train_data <- train_x
train_data$label <- train_y
test_data <- test_x
test_data$label <- test_y
```

## Train and Test the Prediction Model

We use a simple logistic regression classifier implemented in the
“SuperML” R package. SuperML was designed to be very similar to the
Python scikit-learn package for machine learning. More information about
the SuperML can be found
[here](https://rdrr.io/cran/superml/f/vignettes/introduction.Rmd). After
training the classifier using the “fit” function, we use the “predict”
function to predict a decision value for each sample in the test
dataset. Because the dataset may not be balanced in terms of the number
of samples in each class, we use AUC, or Area Under the ROC curve, to
assess prediction performance. The decision values are used to calculate
the AUC, with higher AUC values indicating better prediction
performance. An AUC of 1 indicates perfect prediction. More information
about accuracy, AUC, and other classification performance metrics can be
found in the [Google Machine Learning crash
course](https://developers.google.com/machine-learning/crash-course/classification/video-lecture).
Read about AUC
[here](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc).

``` r
# Create an instance of the model using the superml Linear Model trainer and 
# the binomial family for logistic regression classification
model <- LMTrainer$new(family = 'binomial')

# Fit the model with the training data
model$fit(X=train_data, y='label')
summary(model$model)
```

    ## 
    ## Call:
    ## stats::glm(formula = f, family = self$family, data = X, weights = self$weights)
    ## 
    ## Deviance Residuals: 
    ##     Min       1Q   Median       3Q      Max  
    ## -2.4077  -0.8051   0.3323   0.7529   1.7680  
    ## 
    ## Coefficients:
    ##             Estimate Std. Error z value Pr(>|z|)    
    ## (Intercept)  1.37915    0.29223   4.719 2.37e-06 ***
    ## CCPG1       -0.10863    0.40005  -0.272   0.7860    
    ## COPZ2        0.22430    0.56831   0.395   0.6931    
    ## DPT         -0.34782    0.51897  -0.670   0.5027    
    ## DROSHA       0.12363    0.36257   0.341   0.7331    
    ## ENTPD5       0.26706    0.34229   0.780   0.4353    
    ## FAP          0.17426    0.64122   0.272   0.7858    
    ## GCNT1        0.27284    0.32335   0.844   0.3988    
    ## KLRAP1      -0.01840    0.33708  -0.055   0.9565    
    ## LRRC8D       0.49565    0.30413   1.630   0.1032    
    ## MATK        -0.38799    0.33643  -1.153   0.2488    
    ## MCM5        -0.16778    0.36915  -0.455   0.6495    
    ## MLX          0.71550    0.45484   1.573   0.1157    
    ## MTAP         0.15597    0.28732   0.543   0.5872    
    ## MYO7A        0.04331    0.33216   0.130   0.8963    
    ## NUAK1       -0.42736    0.39572  -1.080   0.2802    
    ## OLFML3      -0.10515    0.39579  -0.266   0.7905    
    ## PDGFD        0.07814    0.38581   0.203   0.8395    
    ## PDPR         0.47315    0.35067   1.349   0.1772    
    ## POLE         0.73512    0.47320   1.553   0.1203    
    ## PRSS1       -0.26930    0.30626  -0.879   0.3792    
    ## RHOT1       -0.64278    0.34833  -1.845   0.0650 .  
    ## RNF13        0.64850    0.36796   1.762   0.0780 .  
    ## RPS20        1.00543    0.48870   2.057   0.0397 *  
    ## RPS23       -0.10848    0.42856  -0.253   0.8002    
    ## SLC7A11      0.36360    0.29058   1.251   0.2108    
    ## ST18        -0.41047    0.34837  -1.178   0.2387    
    ## STEAP4      -0.06865    0.30454  -0.225   0.8217    
    ## SYNE1       -0.01625    0.38984  -0.042   0.9668    
    ## THBS1        0.64406    0.54842   1.174   0.2402    
    ## TIMP3       -0.18786    0.47919  -0.392   0.6950    
    ## TRIO         0.30284    0.39266   0.771   0.4406    
    ## WBP1L       -0.51022    0.33678  -1.515   0.1298    
    ## ZBTB10       0.24819    0.31424   0.790   0.4296    
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## (Dispersion parameter for binomial family taken to be 1)
    ## 
    ##     Null deviance: 160.24  on 131  degrees of freedom
    ## Residual deviance: 119.14  on  98  degrees of freedom
    ## AIC: 187.14
    ## 
    ## Number of Fisher Scoring iterations: 5

``` r
# Predict samples in the test data
predictions <- model$predict(df=test_data)

# Evaluate performance using AUC
auc_value <- auc(actual=test_data$label, predicted=predictions)

print(sprintf('Prediction Performance (AUC): %s', auc_value))
```

    ## [1] "Prediction Performance (AUC): 0.713391739674593"

## Evaluate Prediction Performance

The prediction performance AUC of 0.71 is within the performance range
(0.7 to 0.8) of the models developed by Bosquet et al.. Note that if the
“random_state” value is changed in the train/test split step, prediction
performance will vary. Thus, a better method for assessing performance
would be to generate multiple permutations of train/test datasets,
calculate prediction performance for each permutation, and report the
mean and standard deviation of AUC.

``` r
num_iters <- 100
auc_vals <- c()

for (i in 1:num_iters) {

  # use the caret createDataPartition function to create a balanced split of the data into train and test sets
  train_rows = createDataPartition(ge_data_pivot_nosample$label, p=0.5, list=FALSE, times=1)
  train_data <- ge_data_pivot_nosample[train_rows,]
  test_data <- ge_data_pivot_nosample[-train_rows,]

  # move labels to their own variables
  train_y <- train_data$label
  test_y <- test_data$label

  # use caret's preProcess function to scale the data to 0 mean and unit variance
  pre_proc_vals <- preProcess(subset(train_data, select=-c(label)), method=c('center', 'scale'))
  train_x <- predict(pre_proc_vals, subset(train_data, select=-c(label)))
  test_x <- predict(pre_proc_vals, subset(test_data, select=-c(label)))

  # recombine the data and labels
  train_data <- train_x
  train_data$label <- train_y
  test_data <- test_x
  test_data$label <- test_y

  # Create an instance of the model using the superml Linear Model trainer and 
  # the binomial family for logistic regression classification
  model <- LMTrainer$new(family = 'binomial')

  # Fit the model with the training data
  model$fit(X=train_data, y='label')

  # Predict samples in the test data
  predictions <- model$predict(df=test_data)

  # Evaluate performance using AUC
  auc_val <- auc(actual=test_data$label, predicted=predictions)
  auc_vals[i] <- auc_val
}

print('AUC Values: ', str(auc_vals))
```

    ##  num [1:100] 0.634 0.678 0.641 0.614 0.586 ...
    ## [1] "AUC Values: "

``` r
print(sprintf('AUC Mean: %s', mean(auc_vals)))
```

    ## [1] "AUC Mean: 0.644747313780571"

``` r
print(sprintf('AUC Standard Deviation: %s', sd(auc_vals)))
```

    ## [1] "AUC Standard Deviation: 0.0380055481903336"

## Visualize and Interpret Results

We can use data visualization to help interpret the classifier’s
performance. Although our initial prediction result was 0.71, the
average prediction result over several random permutations of the data
is actually below 0.7, with a range spanning approximately 0.6 to 0.7.
An AUC of 0.7 can be interpreted as a 70% chance that the classifier’s
prediction (i.e., “Complete Remission/Response” or not) is correct.

``` r
# use a boxplot to visualize the AUC results
boxplot(auc_vals, xlab='Logistic Regression', ylab='AUC', horizontal=TRUE, ylim=c(0, 1))
```

## Next Steps

The model trained and stored in the “model” variable can now be used to
predict therapeutic outcome of future RNA-seq ovarian cancer samples. If
the model has been trained to generalize well to the problem of
predicting Ovarian cancer therapeutic outcome, we would expect that
future predictions would yield up to a 70% probability of being correct.
However, an inherent problem with estimating machine learning
performance is its dependence on the data. Thus, if future RNA-seq
samples differ from the training data (e.g., different biological
population, different sequencing method or instrument, or different data
normalization method), we cannot make any assumptions about the model’s
prediction of those samples. In addition, if the testing data in our
original assessment is different from the training data, then our
performance estimation of 0.7 AUC may not be reliable. See [Zhang et
al.](https://academic.oup.com/nargab/article/2/3/lqaa078/5909519) for
more information about RNA-seq batch effects.

As an example, suppose that we have a future sample to predict:

``` r
# For this example, we'll just take a single sample out of our previous test
# dataset. However, in practical applications, the future sample usually comes
# from new, independent datasets. 

# Use double brackets to maintain the matrix shape
future_sample = test_data[10,]

# Predict the therapeutic outcome of the future sample using the "predict" 
# function, which will give us a label of either 0 or 1
sample_prediction <- model$predict(df=future_sample)

# The predict function actually returns a decision value, which needs to be
# thresholded to obtain a prediction label. In this case the threshold is 0.5 and
# decision values >0.5 are labeled "1" while decision values <=0.5 are 
# labeled "0".
prediction_label <- if (sample_prediction > 0.5) 1 else 0
print(sprintf("Decision value: %s", sample_prediction))
```

    ## [1] "Decision value: 0.840207083418538"

``` r
print(sprintf("Prediction label: %s", prediction_label))
```

    ## [1] "Prediction label: 1"

A predicted label of “1” means that this future sample is predicted to
have “Complete Remission/Response”, while a predicted label of “0” means
that this future sample is predicted to have “No Response” to therapy.
This prediction process can be repeated for any number of future
samples.
