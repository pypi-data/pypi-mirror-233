import logging
import os
import json
import pandas as pd
from langchain.llms import AzureOpenAI
from langchain.agents import create_spark_dataframe_agent
from pyspark.sql import SparkSession
from ODP_DQ.business_contextNB import BusinessContext
from ODP_DQ.AnomalyDetectionNB import AnomalyDetection
from ODP_DQ.StandarizationNB import Standarization
import findspark


class DataQuality:
    def __init__(self,catalog_name,schema,input_table,choice,api_type=None,api_key=None,api_base=None,api_version=None,model_name=None,deployment_name=None,standarization_columns=None,inputfile=None, outputfile=None, column_types=None, columns_and_contamination=None,columns_and_null_handling=None, columns_and_dbscan_params=None):
        self.catalog_name=catalog_name
        self.schema=schema
        self.input_table=input_table

        self.api_type=api_type
        self.api_key=api_key
        self.api_base=api_base
        self.api_version=api_version
        self.model=model_name
        self.deployment=deployment_name
        self.choice=choice

        self.standarization_columns=standarization_columns

        self.inputfile=inputfile
        self.outputfile=outputfile
        self.column_types=column_types
        self.columns_and_contamination=columns_and_contamination
        self.columns_and_null_handling=columns_and_null_handling
        self.columns_and_dbscan_params=columns_and_dbscan_params

    

    def initiate_langchainFN(self):
        os.environ["OPENAI_API_TYPE"] = self.api_type
        os.environ["OPENAI_API_KEY"] = self.api_key
        os.environ["OPENAI_API_BASE"] = self.api_base
        os.environ["OPENAI_API_VERSION"] = self.api_version
        
       


        llm = AzureOpenAI(
            openai_api_type="azure",
            deployment_name="Sqlcreator",
            model_name="text-davinci-003",
            temperature=0.1)

        #agent = create_pandas_dataframe_agent(llm, df, verbose=False, max_iterations=10)
        return llm
    

    def main(self):

        spark = SparkSession.builder \
                .appName("UpdateTable") \
                .config("spark.catalog.catalogName", self.catalog_name) \
                .config("spark.catalog.schemaName", self.schema_name) \
                .getOrCreate()
        # spark.sql(f"USE CATALOG {self.catalog};USE SCHEMA {self.schema};")

        df = spark.sql(f"SELECT * FROM {self.input_table}")

        #Initialising langchain model--------
        llm=DataQuality.initiate_langchainFN(self)
        agent = create_spark_dataframe_agent(llm, df, verbose=False, max_iterations=10)

        
        
        if self.choice['BusinessContext']==1:
            businessContext= BusinessContext(agent,spark)
            result= businessContext.business_contextFN()
            result.write.option("catalog", self.catalog_name+'.'+self.schema).option("name", 'BusinessContext').saveAsTable('BusinessContext')
        if self.choice['DQRules']==1:
            businessContext= BusinessContext(agent,spark)
            result= businessContext.dq_rulesFN()
            result.write.option("catalog", self.catalog_name+'.'+self.schema).option("name", 'DQRules').saveAsTable('DQRules')

        if self.choice['AnomalyDetection']==1:
            result=AnomalyDetection(self.inputfile, self.outputfile, self.column_types, self.columns_and_contamination,
                 self.columns_and_null_handling, self.columns_and_dbscan_params).run_anomaly_detection(df)
            
            result.write.option("catalog", self.catalog_name+'.'+self.schema).option("name", 'AnomalyDetectionResult').saveAsTable('AnomalyDetectionResult')
        if self.choice['Standarization']==1:
            result=Standarization(llm,self.standarization_columns,spark).format_issue_detection()
            result.write.option("catalog", self.catalog_name+'.'+self.schema).option("name", 'StandarizationResult').saveAsTable('StandarizationResult')
