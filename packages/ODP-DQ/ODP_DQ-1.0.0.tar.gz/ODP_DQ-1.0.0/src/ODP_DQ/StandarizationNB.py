import os
import openai
from langchain.llms import AzureOpenAI
from langchain.llms import create_spark_dataframe_agent
import pandas as pd
import json
from pyspark.sql import SparkSession
from pyspark.sql import Row

class Standarization:
    def __init__(self,llm,columns,spark):
        self.llm=llm
        self.columns=columns
        self.spark=spark
    def format_issue_detection(self):
        prompt= """ For the column "{0}", extract the following information:
                represents: Describe What does the column "{0}" represents?
                
                exists:String variable. The value should be "True"/"False".\
                Check if all the values are in uniform formats or are there any standardization issues exists in the column "{0}"?
                Keeping in mind what the column represents , think logically about the possible standardization issues\
                it can have from the below listed ones.\
                standardization issues can be any of the below:
                - issue1: different languages
                - issue2: different formats
                - issue3: different capitalization 
                - issue4: different units of measurement
                - issue5: different representations
                - issue6: abbreviated and expanded form
                - issue7: different metrics
                - issue8: symbols like @ represented in different ways
                used for different values within the column. And use your common sense to detect other kind of standardization issues
                that exists in the column that are not listed above. Set the value to 'True' if any of the issues exists,\
                'False' if no issues exists or unknown. Don't resolve the formatting issues. Your task is to detect the issues.

                issue: If "exists:" is true, give brief description of what the issue is from your analysis. format is given below:\
                ["issue1": description, "issue2": description, "issue3": description, etc.]
                description should be formatted as Triple-Quoted Strings.
                if "exists' is false, the value should be [issue:'None']. 
                
                sample: If "exists" is true,\
                By analyzing the "issues" you have found above, identify the different formats present in the data and\
                output exactly one value from the data corresponding to each different formats.\
                Output a maximum of 7 different formats that are most frequent and 7 examples, one example per format.
                Remember, within a issue, different formats or representations may occur.\
                Make sure to use escape characters wherever necessary to not cause any errors
    
                Output structure is given below:\
                [format1:example1, format2:example2, format3:example3, ..,formatN:exampleN]
                where format is the different formats and example is the example for each formats. 
                You need to present the format in an intuitive manner/general form
                instead of simply giving the data itself as format. You can use the letter x if there is no other way to represent the format.
                
                if "exists' is false, set this to "None".


                percentage: out of the total data, accurately provide how much percentage of data is present in each of these formats you found above in a descending manner.
                [format1:percentage of data, format2:percentage of data, format3:percentage of data, ..,formatN:percentage of data]
                Format the Final answer as dictionary with the following keys:
                represents
                exist 
                issue
                sample
                percentage

                continue response generation until the json is complete
                """
        final=[]
        columns=self.columns
        for column in columns:
            if self.df[column].dtype == object:
                self.df[column] = self.df[column].str.strip()
            agent = create_spark_dataframe_agent(self.llm, self.df[[column]], verbose=True, max_iterations=15, early_stopping_method="generate")
            prompt_ = prompt.format(column)
            output = self.agent.run(prompt_)
            print(output)
            data_dict = json.loads(output)
            data_dict["column_name"] = column
            final.append(data_dict)
        columns_order=["column_name","represents", "exists", "issue", "sample", "percentage"]
        # final_df = pd.DataFrame(final, columns=columns_order)
        
        data = [Row(**dict(zip(columns_order, final)))]

        result_df = self.spark.createDataFrame(data)

        return result_df