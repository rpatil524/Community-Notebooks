# ISB-CGC Community Notebooks

```
Title:   Quick Start Guide to ISB-CGC
Author:  Lauren Hagen
Created: 2019-06-20
Purpose: Painless intro to working in the cloud
```
***

Quick Start Guide for ISB-CGC
================

[ISB-CGC](https://isb-cgc.appspot.com/)

This Quick Start Guide is intended give an overview of the data
available, a walk-though of the steps of setting up your accounts, and
get started with a basic example in R.

## Access Requirements

  - Google Account to access ISB-CGC
  - [Google Cloud Account](console.cloud.google.com)
  - Some knowledge of SQL

## Access Suggestions

  - Favored Programming Language (R or Python)
  - Favored IDE (RStudio or Jupyter)

## Outline for this Notebook

  - Quick Overview of ISB-CGC
  - About the Data on ISB-CGC
  - Overview How to Access Data
  - Account Set up
  - ISB-CGC Web Interface
  - Google Cloud Platform (GCP) and BigQuery Overview
  - Example of Accessing Data with Python
  - Where to go next

## Overview of ISB-CGC

## Overview of ISB-CGC

The ISB-CGC provides both interactive and programmatic access to data
hosted by institutes such as the Genomic Data Commons (GDC) of the
National Cancer Institute (NCI) and the Wellcome Trust Sanger Institute
while leveraging many aspects of the Google Cloud Platform. You can also
import your own data to analyze it side by side with the datasets from
ISB-CGC and share your data when you see fit. For more information, a
Quick Introduction to the ISB-CGC Platform can be downloaded
[here](https://github.com/isb-cgc/readthedocs/raw/master/docs/include/workshop-intro-Aug2016.pdf).

### Introduction to ISB-CGC Video

There 12 minute video goes over an introduction to ISB-CGC that can be
viewed [here](https://www.youtube.com/watch?v=RQsLKDTciWk) For more
videos check out: [ISB-CGC Video Tutorial
Series](https://isb-cgc.appspot.com/videotutorials/)

## About the Data on ISB-CGC

The main data that ISB-CGC hosts is the Cancer Genome Atlas (TCGA) data
which was a large-scale multi-disciplinary collaboration started by the
National Cancer Institute (NCI) and the National Human Genome Research
Institute (NHGRI). Some of the hosted data types and files include
RNA-Seq FASTQ, DNA-Seq and RNA-Seq BAM Files, Genome-Wide SNP6 array CEL
files, and Variant-calls in VCF files. ISB-CGC now also hosts a number
of other datasets including Therapeutically Applicable Research to
Generate Effective Treatments (TARGET) data and Cancer Cell Line
Encyclopedia (CCLE) data. ISB-CGC is adding more data sets all the time,
so if you have suggestions for a datasets to be added please email:
<feedback@isb-cgc.org>

For more information, please visit: [Cloud-Hosted Data
Sets](https://isb-cancer-genomics-cloud.readthedocs.io/en/latest/sections/Hosted-Data.html),
[Data Types in Cloud
Storage](https://isb-cancer-genomics-cloud.readthedocs.io/en/latest/sections/data/data2/data_in_GCS.html),
and [Data in
BigQuery](https://isb-cancer-genomics-cloud.readthedocs.io/en/latest/sections/data/data2/data_in_BQ.html)

## Overview of How to Access Data

There are several ways to access the Data that is hosted by ISB-CGC.

  - APIs
      - ISB-CGC WebApp
          - Provides a graphical interface to the ISB\*CGC metadata
            stored in CloudSQL, and consists of several “endpoints”,
            implemented using Google Cloud Endpoints.
          - Does not require knowledge of programming languages
      - ISB-CGC APIs
      - Provides programmatic access to data and metadata stored in
        CloudSQL
      - Google Cloud Platform
          - Allows you to use GCP APIs such as BigQuery, Cloud Datalab,
            Colaboratory
          - Allows you to host your own data on the Cloud
  - BigQuery
      - A GCP Allows you to use SQL to access some data
  - Supported Programming Languages
      - SQL
          - Can be used directly in BigQuery
      - Python
          - [gsutil tool](https://cloud.google.com/storage/docs/gsutil)
            is a Python tool to access data via the command line
          - Jupyter Notebooks
              - Google Colabratory or Cloud Datalab use Jupyter as a
                base
      - R
          - RStudio
  - Command Line Interfaces
      - Cloud Shell via Project Console
      - [CLOUD SDK](https://cloud.google.com/sdk/)

## Account Set-up

*If not completed prior to reading this guide*

1.  Log in or
    [create](https://accounts.google.com/signup/v2/webcreateaccount?dsh=308321458437252901&continue=https%3A%2F%2Faccounts.google.com%2FManageAccount&flowName=GlifWebSignIn&flowEntry=SignUp#FirstName=&LastName=)
    a Gmail account +Can be use your institutional email if it is a
    Google Identity

2.  Create a GCP Project using a GMail account

<!-- end list -->

  - Required to use all of the data, tools and the Google Cloud
  - New accounts get a one-time [300 Google
    Credit](https://cloud.google.com/free/)

<!-- end list -->

3.  Authorize your account for dbGaP in the ISB-CGC WebApp (required for
    viewing controlled access data)

<!-- end list -->

  - To access controlled data, users must first be authenticated by NIH
    (via the ISB-CGC web-app). Upon successful authentication, user
    dbGaP authorization will be verified. These two steps are required
    before the user’s Google identity is added to the access control
    list (ACL) for the controlled data. At this time, this access must
    be renewed every 24 hours.
  - Please view [Accessing Controlled-Access
    Data](https://isb-cancer-genomics-cloud.readthedocs.io/en/latest/sections/webapp/Gaining-Access-To-Contolled-Access-Data.html)
    if you need help with this step.

<!-- end list -->

4.  Register your GCP project in the ISB-CGC WebApp

<!-- end list -->

  - Please view [Registering your Google Cloud Project Service
    Account](https://isb-cancer-genomics-cloud.readthedocs.io/en/latest/sections/webapp/Gaining-Access-To-Contolled-Access-Data.html#requirements-for-registering-a-google-cloud-project-service-account)
    if you need help with this step.

<!-- end list -->

5.  Enable the following required Google Cloud APIs:

<!-- end list -->

  - Google Compute Engine
  - Google Genomics
  - Google BigQuery
  - Google Cloud Logging
  - Google Cloud Pub/Sub

[Google Tutorial on Enabling/Disabling GC
APIs](https://cloud.google.com/apis/docs/enable-disable-apis)

6.  Install optional software such as:

<!-- end list -->

  - [Cloud SDK](https://cloud.google.com/sdk/)
  - [Anaconda Python](https://www.anaconda.com/distribution/)
  - [Jupyter Notebook](https://jupyter.org/)
  - [R](https://cran.r-project.org/)
  - [RStudio](https://www.rstudio.com/)
  - [Chrome](https://www.google.com/chrome/)
  - [Docker](https://www.docker.com/)

## ISB-CGC Web Interface

The ISB-CGC Web Interface is an [interactive web-based
application](https://isb-cgc.appspot.com/) to access and explore the
rich TCGA, TARGET, CCLE, and COSMIC datasets with more datasets being
added regularly. Through the WebApp you can create Cohorts, lists of
Favorite Genes, miRNA, and Variables. The Cohorts and Variables can be
used in Workbooks to allow you to quickly analyze and export datasets by
mixing and matching the selections. The ISB-CGC Web Interface also
allows you to view and analyze available pathology and radiology images
associated with selected cohort data.

# Google Cloud Platform and BigQuery Overview

The [Google Cloud Platform Console](https://console.cloud.google.com/)
is the web-based interface to your GCP Project. From the Console, you
can check the overall status of your project, create and delete Cloud
Storage buckets, upload and download files, spin up and shut down VMs,
add members to your project, acces the [Cloud Shell command
line](https://cloud.google.com/shell/docs/), etc. Click
[here](https://raw.githubusercontent.com/isb-cgc/readthedocs/master/docs/include/intro_to_Console.pdf)
to download a quick tour from ISB-CGC of the GCP Console. You’ll want to
remember that any costs that you incur are charged under your *current*
project, so you will want to make sure you are on the correct one if you
are part of multiple projects.
[Here](https://isb-cancer-genomics-cloud.readthedocs.io/en/latest/sections/DIYWorkshop.html#google-cloud-platform-console)
is how to check which project is your *current* project.

“BigQuery is a serverless, highly-scalable, and cost-effective cloud
data warehouse with an in-memory BI Engine and machine learning built
in.” [*Source*](https://cloud.google.com/bigquery/) ISB-CGC has uploaded
multiple cancer genomic datasets into BigQuery tables that are
open-source such as TCGA and TARGET Clinical, Biospecimen and Molecular
Data along with dataset megadata. This data can be accessed from the
Google Cloud Platform Console web-UI, programmatically with R, and
programmatically with python through Cloud Datalab or Colab.

More indepth walk throughs:

  - [Walkthrough of Google
    BigQuery](https://isb-cancer-genomics-cloud.readthedocs.io/en/latest/sections/progapi/bigqueryGUI/WalkthroughOfGoogleBigQuery.html)
  - [Introduction to GCE (Google Compute
    Engine)](https://docs.google.com/presentation/d/13ORIDboGC27uCMf_C9w9WIi0cK9tGO7cqgp6vwA2miE/edit?usp=sharing)
  - [Google Genomics “Pipelines”
    Service](https://docs.google.com/presentation/d/1_rRvlhNuA0_SQuO2SOru7ttjPvzlygW3ALILcQ-JEjg/edit?usp=sharing)
  - [ISB-CGC Pipelines
    Framework](https://docs.google.com/presentation/d/1akqoZImzei2D47O8rcWrcEzsWPYxUtL-2-eUdiBzzgo/edit?usp=sharing)
    and [github repository of
    pipelines](https://github.com/isb-cgc/ISB-CGC-pipelines)

## Example of Accessing Data with R

Load Libraries Required for using BigQuery in R

``` r
library(bigrquery)
library(dplyr)
```

    ## 
    ## Attaching package: 'dplyr'

    ## The following objects are masked from 'package:stats':
    ## 
    ##     filter, lag

    ## The following objects are masked from 'package:base':
    ## 
    ##     intersect, setdiff, setequal, union

### View Datasets and Tables in BigQuery

Let us look at the available data sets within the ISB-CGC.

But first we will need to authorize our access by running a code block
that connects to BigQuery. This will come up with a question if you want
to cache your credentials between R sessions, in the R Console type your
response and press enter. Then a new browser tab will open to authorize
the use of your Google Account. Follow the prompts on the site and then
copy the code back into the R Console and press enter. If you do not
cache your credentials or have restarted your computer, you will be
asked to do this at the start of a session.

``` r
# Let us view which datasets are availabe from ISB-CGC through BigQuery
list_datasets("isb-cgc") # isb-cgc is the project name
```

    ##  [1] "CCLE_bioclin_v0"     "GDC_metadata"        "GTEx_v7"            
    ##  [4] "QotM"                "TARGET_bioclin_v0"   "TARGET_hg38_data_v0"
    ##  [7] "TCGA_bioclin_v0"     "TCGA_hg19_data_v0"   "TCGA_hg38_data_v0"  
    ## [10] "Toil_recompute"      "ccle_201602_alpha"   "genome_reference"   
    ## [13] "hg19_data_previews"  "hg38_data_previews"  "metadata"           
    ## [16] "platform_reference"  "tcga_201607_beta"    "tcga_cohorts"       
    ## [19] "tcga_seq_metadata"

``` r
# Let us look which tables are in the TCGA_bioclin_v0 dataset
list_tables("isb-cgc", "TCGA_bioclin_v0") # the convention is project name then dataset
```

    ## [1] "Annotations" "Biospecimen" "Clinical"    "clinical_v1"

``` r
project <- 'isb-cgc-02-0001' # Insert your project ID in the ''
theTable <- "isb-cgc.TCGA_bioclin_v0.Clinical" # The convention for calling a table is project.dataset.table
# Create the SQL query
sql <- "SELECT
  program_name,
  case_barcode,
  project_short_name
FROM
  `isb-cgc.TCGA_bioclin_v0.Clinical`
LIMIT
  5"
# Use BigQuery to run the SQL query on the Clincal table from the TCGA_bioclin_v0 dataset
# which then may be downloadedinto a tibble.
result <- bq_project_query(project, sql)
result <- bq_table_download(result)
print(result)
```

    ## # A tibble: 5 x 3
    ##   program_name case_barcode project_short_name
    ##   <chr>        <chr>        <chr>             
    ## 1 TCGA         TCGA-01-0628 TCGA-OV           
    ## 2 TCGA         TCGA-01-0630 TCGA-OV           
    ## 3 TCGA         TCGA-01-0631 TCGA-OV           
    ## 4 TCGA         TCGA-01-0633 TCGA-OV           
    ## 5 TCGA         TCGA-01-0636 TCGA-OV

Now that wasn’t so difficult\! Have fun exploring and analyzing the
ISB-CGC Data\!

## Where to Go Next

Explore, Discover, and Analyze the Data provided by ISB-CGC along with
side by side with your own\! :)

ISB-CGC Links:

  - [ISB-CGC Landing Page](https://isb-cgc.appspot.com/)
  - [ISB-CGC
    Documentation](https://isb-cancer-genomics-cloud.readthedocs.io/en/latest/)
  - [How to Get Started on
    ISB-CGC](https://isb-cancer-genomics-cloud.readthedocs.io/en/latest/sections/HowToGetStartedonISB-CGC.html)
  - [GitHub Repository of Python
    Examples](https://github.com/isb-cgc/examples-Python)
  - [GitHub Repository of R
    Examples](https://github.com/isb-cgc/examples-R)
  - [Query of the
    Month](https://isb-cancer-genomics-cloud.readthedocs.io/en/latest/sections/QueryOfTheMonthClub.html)
  - [Quick
    Links](https://isb-cancer-genomics-cloud.readthedocs.io/en/latest/sections/QuicklinksOneTable.html)

Google Tutorials:

  - [Google’s What is
    BigQuery?](https://cloud.google.com/bigquery/what-is-bigquery)
  - [Google Cloud Client Library for
    Python](https://googleapis.github.io/google-cloud-python/latest/index.html)

ISB-CGC Tutorials:

  - [Walkthrough of Google
    BigQuery](https://isb-cancer-genomics-cloud.readthedocs.io/en/latest/sections/progapi/bigqueryGUI/WalkthroughOfGoogleBigQuery.html)
  - [Introduction to GCE (Google Compute
    Engine)](https://docs.google.com/presentation/d/13ORIDboGC27uCMf_C9w9WIi0cK9tGO7cqgp6vwA2miE/edit?usp=sharing)
  - [Google Genomics “Pipelines”
    Service](https://docs.google.com/presentation/d/1_rRvlhNuA0_SQuO2SOru7ttjPvzlygW3ALILcQ-JEjg/edit?usp=sharing)
  - [ISB-CGC Pipelines
    Framework](https://docs.google.com/presentation/d/1akqoZImzei2D47O8rcWrcEzsWPYxUtL-2-eUdiBzzgo/edit?usp=sharing)
    and [github repository of
    pipelines](https://github.com/isb-cgc/ISB-CGC-pipelines)
