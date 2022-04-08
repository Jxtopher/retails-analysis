# https://stackoverflow.com/questions/59854917/reading-excel-xlsx-file-in-pyspark
from pyspark.sql import SparkSession
from pyspark import SparkConf, SparkContext

import pandas

def test():
    sc = SparkContext()
    # spark = SparkSession.builder.appName("Test").getOrCreate()

    # pdf = pandas.read_excel('excelfile.xlsx', sheet_name='sheetname', inferSchema='true')
    # df = spark.createDataFrame(pdf)

    # df.show()