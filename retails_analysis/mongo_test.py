from pyspark.sql import SparkSession


def test() -> None:
    spark = (
        SparkSession.builder.appName("myApp")
        .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1')
        .config(
            "spark.mongodb.input.uri",
            "mongodb://root:f2U8K288capdYdYV9@172.21.0.3/test.coll?authSource=admin",
        )
        .config(
            "spark.mongodb.output.uri",
            "mongodb://root:f2U8K288capdYdYV9@172.21.0.3/test.coll?authSource=admin",
        )
        .getOrCreate()
    )

    people = spark.createDataFrame(
        [
            ("Bilbo Baggins", 50),
            ("Gandalf", 1000),
            ("Thorin", 195),
            ("Balin", 178),
            ("Kili", 77),
            ("Dwalin", 169),
            ("Oin", 167),
            ("Gloin", 158),
            ("Fili", 82),
            ("Bombur", None),
        ],
        ["name", "age"],
    )
    people.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").save()
