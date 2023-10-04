import openai
from langchain.llms import AzureOpenAI
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql import Row

class BusinessContext:
    def __init__(self,agent ,spark):
                
        
        """ Initialize the class
            Params:
            agent: Langchain agent which can be use to get the result from ai model using prompt as input.
        """
        
        # Setting this to true will print statements and display dataframes
        self.agent=agent
        self.spark=spark

    def business_contextFN(self,spark):

        prompt = """Understand the given dataset and generate the business context of the data.
            The Business context of the data will include the name, description, the domain of data and the entities or attributes associated with the data.
            The output should be in json structure with above mentioned points as keys. Please give a little detailed explanation in values and explain the attributes. 
            Return the final answer in json format.
            """
        business_context = self.agent.run(prompt)
        df = self.spark.createDataFrame([Row(result=business_context)])
        return df
    
    def dq_rulesFN(self,spark):
        prompt="""Understand the data and generate a json output which has data quality checks as key and the columns where these checks could be applied as values.
        Pattern check will have dictionary of columns and the regex pattern it should follow in it. For the regex pattern it should populate some basic regex for columns like Name, phone number etc.
        For Unique check you should identify the columns which should only have unique values, similarly for Null check, identify columns whose value cannot be null.
        Please use Unique, null and pattern check and generate result in below format and do not include any steps for implementation.
        The output should just be a dictionary which can be converted to json directly.
        {
        "Null check": ["Column1", "Column2", ...],
        "Unique check": ["Column3", "Column4", ...],
        "Pattern check":{"Column1":"pattern1","Column2":"pattern2",...}
        }
        
        """
        dq_rules=self.agent.run(prompt)
        df = self.spark.createDataFrame([Row(result=dq_rules)])
        return df