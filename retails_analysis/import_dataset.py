# -----------------------------------------------------------
# Import a dataset into the database
# -----------------------------------------------------------
from numpy import double
from pyspark.sql import SparkSession
from os.path import exists
from pyspark.sql.types import StructType, StructField, StringType, LongType, DoubleType

import puremagic
import pandas
import sys
from dotenv import dotenv_values


def import_retails_data(
    path_to_file: str,
    spark_host: str,
    spark_port: str,
    monngo_host: str,
    monngo_port: str,
    monngo_user: str,
    monngo_pwd: str,
    monngo_db: str,
    monngo_coll: str,
) -> None:
    """Import retails dataset in xls format"""
    mongodb_write_uri = 'mongodb://{monngo_user}:{monngo_pwd}@{monngo_host}:{monngo_port}/{monngo_db}.{monngo_coll}?authSource=admin'

    mongodb_read_uri = 'mongodb://{monngo_user}:{monngo_pwd}@{monngo_host}:{monngo_port}/{monngo_db}.{monngo_coll}?authSource=admin'
    print(mongodb_write_uri)
    spark = (
        SparkSession.builder.appName("Import retails dataset")
        .master('spark://' + spark_host + ':' + spark_port)
        .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector:10.0.0')
        .config(
            'spark.mongodb.write.connection.uri',
            'mongodb://'
            + monngo_user
            + ':'
            + monngo_pwd
            + '@'
            + monngo_host
            + ':'
            + monngo_port
            + '/'
            + monngo_db
            + '.'
            + monngo_coll
            + '?authSource=admin',
        )
        .config(
            'spark.mongodb.read.connection.uri',
            'mongodb://'
            + monngo_user
            + ':'
            + monngo_pwd
            + '@'
            + monngo_host
            + ':'
            + monngo_port
            + '/'
            + monngo_db
            + '.'
            + monngo_coll
            + '?authSource=admin',
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
    df.write.format("mongodb").mode("append").save()


def main() -> None:
    # Loading environment vars
    config = dotenv_values(".env")
    if not exists(".env"):
        raise Exception('[-] File ' + ".env" + ' does not exist')

    args = sys.argv[1:]
    # Check args
    if len(args) != 1:
        print("Usage poetry run import path/file.xls")
        exit(1)

    # Check file format
    path_to_file = args[0]
    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    mime_type_file = puremagic.magic_file(path_to_file)[0][3]
    if mime_type != mime_type_file:
        print("Only xls format can be imported.")
        exit(1)

    # Check if file exist
    if not exists(path_to_file):
        raise Exception('[-] File ' + path_to_file + ' does not exist')

    import_retails_data(
        path_to_file,
        str(config['SPARK_MASTER_HOST']),
        str(config['SPARK_MASTER_PORT']),
        str(config['MONNGO_HOST']),
        str(config['MONNGO_PORT']),
        str(config['MONNGO_USER']),
        str(config['MONNGO_PWD']),
        str(config['MONNGO_DB']),
        str(config['MONNGO_COLL']),
    )
    exit(0)
