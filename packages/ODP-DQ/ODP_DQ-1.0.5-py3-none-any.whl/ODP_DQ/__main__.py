import logging
import os
import json
import pandas as pd
import pyspark.pandas as ps
from ODP_DQ.business_contextNB import BusinessContext
from ODP_DQ.AnomalyDetectionNB import AnomalyDetection
from ODP_DQ.StandardizationNB import Standardization
import findspark



class DataQuality:
    def __init__(self,catalog_name,schema,input_table,choice,api_key=None,api_base=None,api_version=None,model_name=None,deployment_name=None,standarization_columns=None,inputfile=None, outputfile=None, column_types=None, columns_and_contamination=None,columns_and_null_handling=None, columns_and_dbscan_params=None):
        self.catalog_name=catalog_name
        self.schema=schema
        self.input_table=input_table


        self.api_key=api_key
        self.api_base=api_base
        self.api_version=api_version
        self.deployment_model=deployment_name
        self.model_name=model_name
        self.choice=choice

        self.standarization_columns=standarization_columns

        self.inputfile=inputfile
        self.outputfile=outputfile
        self.column_types=column_types
        self.columns_and_contamination=columns_and_contamination
        self.columns_and_null_handling=columns_and_null_handling
        self.columns_and_dbscan_params=columns_and_dbscan_params

    

    

    def main(self):

        
        df = ps.read_table(f"{self.catalog_name}.{self.schema}.{self.input_table}")
        
        
        if self.choice['BusinessContext']==1:
            businessContext= BusinessContext(self.api_key,self.api_base,self.api_version,self.deployment_model,self.model_name)
            result_bc= businessContext.business_contextFN(df)
            # df = self.spark.createDataFrame([Row(result=result_bc)])
            result_bc.to_table(f"{self.catalog_name}.{self.schema}.BusinessContext", overwriteSchema=True)
        if self.choice['DQRules']==1:
            businessContext= BusinessContext(self.api_key,self.api_base,self.api_version,self.deployment_model,self.model_name)
            result_dq= businessContext.dq_rulesFN(df)
            # df = self.spark.createDataFrame([Row(result=result_dq)])
            result_dq.to_table(f"{self.catalog_name}.{self.schema}.DQRules", overwriteSchema=True)

        if self.choice['AnomalyDetection']==1:
            result=AnomalyDetection(self.inputfile, self.outputfile, self.column_types, self.columns_and_contamination,
                 self.columns_and_null_handling, self.columns_and_dbscan_params).run_anomaly_detection(df)
            
            result.to_table(f"{self.catalog_name}.{self.schema}.AnomalyDetectionResult", overwriteSchema=True)
        if self.choice['Standardization']==1:
            result=Standardization(self.standarization_columns,df,self.api_key,self.api_base,self.api_version,self.deployment_model,self.model_name).format_issue_detection()
            result.to_table(f"{self.catalog_name}.{self.schema}.StandardizationResult", overwriteSchema=True)
