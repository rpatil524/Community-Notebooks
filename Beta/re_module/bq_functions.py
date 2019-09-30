from google.cloud import bigquery
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import ipywidgets as widgets
from   ipywidgets import Layout


def runQuery ( client, qString, ParameterList, dryRun=False ):
#  """
#**`runQuery`**: a relatively generic BigQuery query-execution wrapper function which can be used to run a query in "dry-run"  mode or not:  the call to the `query()` function itself is inside a `try/except` block and if it fails we return `None`;  otherwise a "dry" will return an empty dataframe, and a "live" run will return the query results as a dataframe. This function was modify from previous notebooks to handle user-defined parameteres necessary for the purpose of this notbeook.
#  """
  
  print ( "\n in runQuery ... " )
  if ( dryRun ):
    print ( "    dry-run only " )
    
  ## set up QueryJobConfig object
  job_config = bigquery.QueryJobConfig()
    
  query_params = [
        bigquery.ArrayQueryParameter('PARAMETERLIST', 'STRING', ParameterList ),       
  ]
  job_config.query_parameters = query_params  
    
  job_config.dry_run = dryRun
  job_config.use_query_cache = True
  job_config.use_legacy_sql = False
  
  ## run the query
  try:
    query_job = client.query ( qString, job_config=job_config )
    ## print ( "    query job state: ", query_job.state )
  except:
    print ( "  FATAL ERROR: query execution failed " )
    return ( None )
  
  ## return results as a dataframe (or an empty dataframe for a dry-run) 
  if ( not dryRun ):
    try:
      df = query_job.to_dataframe()
      if ( query_job.total_bytes_processed==0 ):
        print ( "    the results for this query were previously cached " )
      else:
        print ( "    this query processed {} bytes ".format(query_job.total_bytes_processed) )
      if ( len(df) < 1 ):
        print ( "  WARNING: this query returned NO results ")
      return ( df )
    except:
      print ( "  FATAL ERROR: query execution failed " )
      return ( None )
    
  else:
    print ( "    if not cached, this query will process {} bytes ".format(query_job.total_bytes_processed) )
    ## return an empty dataframe
    return ( pd.DataFrame() )


def bqtable_data( MolecularFeature  ) :

    Features = { 'Gene Expression' : { 'table'  : 'pancancer-atlas.Filtered.EBpp_AdjustPANCAN_IlluminaHiSeq_RNASeqV2_genExp_filtered',
                                       'symbol' : 'Symbol',
                                       'data'   : 'AVG( LOG10( normalized_count + 1 ) ) ',
                                       'rnkdata': 'DENSE_RANK() OVER (PARTITION BY symbol ORDER BY data ASC)',
                                       'avgdat' : 'avgdata',  
                                       'barcode': 'SampleBarcode',
                                       'where'  : ''},

                 'Somatic Mutation': { 'table'  : 'pancancer-atlas.Filtered.MC3_MAF_V5_one_per_tumor_sample',
                                       'symbol' : 'Hugo_Symbol',
                                       'data'   : '#',
                                       'rnkdata': '#',
                                       'avgdat' : '#',  
                                       'barcode': 'Tumor_SampleBarcode',
                                       'where'  : ''}
               }

    feature = Features[MolecularFeature]
    return feature      


def get_feature2_table( study , feature2_name ) :

   feat =  bqtable_data( feature2_name   )
   table2= """
table2 AS (
SELECT
   symbol,
   {0} AS rnkdata,
   SampleBarcode
FROM (
   SELECT
      {1} AS symbol, 
      {2} AS data,
      {3} AS SampleBarcode
   FROM `{4}`
   WHERE Study = '{6}' AND {1} IS NOT NULL
         {5}  
   GROUP BY
      SampleBarcode, symbol
   )
)
""".format( feat['rnkdata'],feat['symbol'],feat['data'],feat['barcode'],feat['table'],feat['where'],study )

   return( table2 )


def get_summarized_table( feature ) :
  
    summ_table = '' 
    if ( feature == 'Gene Expression' )  :
        summ_table = """
summ_table AS (
SELECT 
   n1.symbol as symbol1,
   n2.symbol as symbol2,
   CORR(n1.rnkdata , n2.rnkdata) as rho
FROM
   table1 AS n1
INNER JOIN
   table2 AS n2
ON
   n1.SampleBarcode = n2.SampleBarcode
   AND n1.symbol <> n2.symbol  
GROUP BY
   symbol1, symbol2
ORDER BY rho DESC
)
""" 
    elif ( feature == 'Somatic Mutation'  ) :
        summ_table = """
summ_table AS (
SELECT 
   n1.symbol AS symbol1,
   n2.symbol AS symbol2,
   COUNT( n1.SampleBarcode ) as n_1,
   SUM( n1.data )  as sumx_1,
   SUM( n1.data * n1.data ) as sumx2_1
FROM
   table1 AS n1
INNER JOIN
   table2 AS n2
ON
   n1.SampleBarcode = n2.SampleBarcode
GROUP BY
   symbol1, symbol2 
)
"""

    return summ_table 



def get_stat_table( feature ) :
  
    stat_table = '' 
    
    if ( feature == 'Gene Expression' )  :
        stat_table = """
SELECT * 
FROM summ_table
"""
    elif ( feature == 'Somatic Mutation'  ) :
        stat_table = """
SELECT 
    symbol1, symbol2,
    n_1, n_2,
    avg1, avg2,
    ABS(avg1 - avg2)/ SQRT( var1 /n_1 + var2/n_2 )  as tscore
FROM (
SELECT symbol1, symbol2, n_1, 
       sumx_1 / n_1 as avg1,
       ( sumx2_1 - sumx_1*sumx_1/n_1 )/(n_1 -1) as var1, 
       n_t - n_1 as n_2,
       (sumx_t - sumx_1)/(n_t - n_1) as avg2,
       (sumx2_t - sumx2_1 - (sumx_t-sumx_1)*(sumx_t-sumx_1)/(n_t - n_1) )/(n_t - n_1 -1 ) as var2
FROM  summ_table
LEFT JOIN ( SELECT symbol, COUNT( SampleBarcode ) as n_t, SUM( data ) as sumx_t, SUM( data*data ) as sumx2_t
            FROM table1 
            GROUP BY symbol )
ON symbol1 = symbol      
)
WHERE
   n_1 > 5 AND n_2 > 5 AND var1 > 0 and var2 > 0
ORDER BY tscore DESC
"""
    return stat_table 

def makeWidgets():
  studyList = [ 'ACC', 'BLCA', 'BRCA', 'CESC', 'CHOL', 'COAD', 'DLBC', 'ESCA', 
                'GBM', 'HNSC', 'KICH', 'KIRC', 'KIRP', 'LAML', 'LGG', 'LIHC', 
                'LUAD', 'LUSC', 'MESO', 'OV', 'PAAD', 'PCPG', 'PRAD', 'READ', 
                'SARC', 'SKCM', 'STAD', 'TGCT', 'THCA', 'THYM', 'UCEC', 'UCS', 
                'UVM' ]

  study = widgets.Dropdown(
      options=studyList,
      value='UCEC',
      description='',
      disabled=False
      )


  FeatureList = [ 'Gene Expression', 'Somatic Mutation'] ;

  feature2 = widgets.Dropdown(
      options=FeatureList,
      value='Gene Expression',
      description='',
      disabled=False
      )

  gene_names = widgets.Text(
      value='IGF2, ADAM2',
      placeholder='Type gene names  ',
      description='',
      disabled=False
      )
 

  study_title = widgets.HTML('<em>Select a study </em>')
  display(widgets.HBox([study_title, study]))

  feature_title = widgets.HTML('<em>Select a molecular feature </em>')  
  display(widgets.HBox([ feature_title, feature2 ]))

  genes_title = widgets.HTML('<em>Type gene names </em>')
  display(widgets.HBox([ genes_title, gene_names  ]))


  return([study, feature2, gene_names  ])


def makeWidgetsPair() : 
  gene_name1 = widgets.Text(
      value='',
      placeholder='gene name',
      description='',
      disabled=False
      )

  gene_name2 = widgets.Text(
      value='',
      placeholder='gene name',
      description='',
      disabled=False
      )  
  
  gene1_title = widgets.HTML('<em>Type name 1 </em>')
  display(widgets.HBox([ gene1_title, gene_name1  ]))

  gene2_title = widgets.HTML('<em>Type name 2 </em>')
  display(widgets.HBox([ gene2_title, gene_name2  ]))

  return([gene_name1 , gene_name2  ])

 

def table_pair ( symbol, feature2_name , study, table_label ) :
   
   ft = bqtable_data( feature2_name ) 
                          
   query_table = table_label + """ AS (
SELECT
   symbol,
   {0} AS data,
   SampleBarcode
FROM (
   SELECT
      {1} AS symbol, 
      {2} AS avgdata,
      {3} AS SampleBarcode
   FROM `{4}`
   WHERE Study = '{5}' AND {1} = '{6}'
         {7}  
   GROUP BY
      SampleBarcode, symbol
   )
)""".format(ft['avgdat'],ft['symbol'],ft['data'],ft['barcode'],ft['table'], study, symbol ,ft['where'] )
   
   return( query_table )

    
    
def get_query_pair (name1, name2, study, feature1_name, feature2_name): 

   query_table1 =  table_pair(name1, feature1_name , study, 'table1' )
   query_table2 =  table_pair(name2, feature2_name , study, 'table2' )

   if ( feature2_name == 'Gene Expression' ):
      data2_str = 'n2.data' 
   elif ( feature2_name == 'Somatic Mutation' ):
      data2_str = 'IF( n2.SampleBarcode is null, 0, 1)'
   else :
      data2_str = 'n2.data'
   
   combine_str = """
SELECT 
    n1.data as data1,  
    {0} as data2,  
    n1.SampleBarcode
FROM
    table1 n1  
LEFT JOIN  table2   n2 
ON  n1.SampleBarcode = n2.SampleBarcode""".format( data2_str)
    
   query_pair = 'WITH\n' +  query_table1 + ',\n' + query_table2 + combine_str              
   return( query_pair )


def plot_statistics_pair ( mydf , feature2_name ) :  

    if (feature2_name == 'Gene Expression' ): 
         
         mydf.plot.scatter(x='data1', y='data2') 
         print(  stats.spearmanr(mydf['data1'],mydf['data2'])  )

    elif (feature2_name == 'Somatic Mutation' ): 
        sns.violinplot( x=mydf["data2"], y=mydf["data1"], palette="Blues")
 
        print( mydf.groupby('data2').mean() )
        
        Set1 = mydf[mydf['data2']==0]
        Set2 = mydf[mydf['data2']==1]
        print( stats.ttest_ind(Set1['data1'], Set2['data1'], equal_var=False ) )
      
    return 

