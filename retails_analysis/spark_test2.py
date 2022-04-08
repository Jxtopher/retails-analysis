from pyspark import SparkContext
from pyspark import SparkConf, SparkContext

def test():

    sc = SparkContext()
    # conf = SparkConf().setAppName("PySpark App").setMaster("spark://localhost:7077")
    # sc = SparkContext(conf=conf)
    ma_liste = range(10000)
    print(ma_liste)
    rdd = sc.parallelize(ma_liste, 2)
    nombres_impairs = rdd.filter(lambda x: x % 2 != 0)


    print("*************")
    print(nombres_impairs.take(5))
    # print(nombres_impairs.collect())
    print(nombres_impairs.count())
    print("*************")
