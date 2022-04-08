# cf. pyspark https://www.data-transitionnumerique.com/pyspark/
# Plotly : https://plotly.com/python/v3/apache-spark/
from pyspark.sql.types import StructType, DateType, StringType, TimestampType, DoubleType
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql.functions import lit, count
from pyspark import SparkContext, SparkConf


conf = SparkConf().setAppName("PySpark App").setMaster("spark://master:7077")
sc = SparkContext(conf=conf)

sc.setLogLevel('DEBUG')

readSchema = ( StructType()
.add('Type', StringType())
.add('Date', TimestampType())
.add('Price', DoubleType())
)


ds = (spark
.readStream.format("csv")
.option("header", "true")
.schema(readSchema)
.load("daily*.csv"))


slidingWindows = (ds
.withWatermark("Date", "1 minute")
.groupBy(ds.Type, F.window(ds.Date, "7 day"))
.avg()
.orderBy(ds.Type,'window'))

dsw = (
slidingWindows
    .writeStream
    .format("mongodb")
    .queryName("7DaySlidingWindow")
    .option("checkpointLocation", "/tmp/pyspark/")
    .option("forceDeleteTempCheckpointLocation", "true")
    .option('spark.mongodb.connection.uri', 'MONGODB CONNECTION HERE')
    .option('spark.mongodb.database', 'Pricing')
    .option('spark.mongodb.collection', 'NaturalGas')
    .outputMode("complete"))

query = dsw.start()
query.processAllAvailable()
query.stop()