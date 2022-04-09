# https://stackoverflow.com/questions/59854917/reading-excel-xlsx-file-in-pyspark
from numpy import double
from pyspark.sql import SparkSession
from pyspark import SparkConf, SparkContext
from os.path import exists
from pyspark.sql.types import StructType, StructField, StringType, LongType, DoubleType, DateType

import pandas


def test() -> None:
    path_to_file = 'dataset/Online Retail.xlsx'
    if not exists(path_to_file):
        raise Exception('[-] File ' + path_to_file + ' does not exist')

    # sc = SparkConf().setAppName("PySpark App").setMaster("spark://spark-master:7077")
    # spark = SparkContext(conf=conf)
    spark = (
        SparkSession.builder.appName("Test")
        .master("spark://spark-master:7077")
        .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector:10.0.0')
        .config(
            "spark.mongodb.write.connection.uri",
            "mongodb://root:f2U8K288capdYdYV9@172.21.0.3/test.coll_full?authSource=admin",
        )
        .config(
            "spark.mongodb.read.connection.uri",
            "mongodb://root:f2U8K288capdYdYV9@172.21.0.3/test.coll_full?authSource=admin",
        )
        .getOrCreate()
    )

    pdf = pandas.read_excel(
        path_to_file,
        sheet_name=0,
        dtype={
            'InvoiceNo': str,
            'StockCode': str,
            'Description': str,
            'Quantity': int,
            'InvoiceDate': str,
            'UnitPrice': double,
            'CustomerID': str,
            'Country': str,
        },
        # parse_dates=['InvoiceDate'],
    )

    df_schema = StructType(
        [
            StructField("InvoiceNo", StringType(), True),
            StructField("StockCode", StringType(), True),
            StructField("Description", StringType(), True),
            StructField("Quantity", LongType(), True),
            StructField("InvoiceDate", StringType(), True),  # DateType()
            StructField("UnitPrice", DoubleType(), True),
            StructField("CustomerID", StringType(), True),
            StructField("Country", StringType(), True),
        ]
    )

    df = spark.createDataFrame(pdf, schema=df_schema)

    # df.show()
    df.write.format("mongodb").mode("append").save()
