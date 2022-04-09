import uvicorn
from fastapi import FastAPI
from dotenv import dotenv_values
from typing import Optional, Dict, Any, List
from pyspark.sql import SparkSession
from os.path import exists
from fastapi.responses import HTMLResponse
from pyspark.sql import functions as F
from pyspark.context import SparkContext

# Loading environment vars
config = dotenv_values(".env")
if not exists(".env"):
    raise Exception('[-] File ' + ".env" + ' does not exist')

# Spark initialisation
mongodb_write_uri = (
    'mongodb://'
    + config['MONNGO_USER']
    + ':'
    + config['MONNGO_PWD']
    + '@'
    + config['MONNGO_HOST']
    + '/test.coll?authSource=admin'
)
mongodb_read_uri = (
    'mongodb://'
    + config['MONNGO_USER']
    + ':'
    + config['MONNGO_PWD']
    + '@'
    + config['MONNGO_HOST']
    + '/test.coll?authSource=admin'
)

(
    SparkSession.builder.appName("Retails analysis")
    .master("spark://spark-master:7077")
    .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector:10.0.0')
    .config(
        'spark.mongodb.write.connection.uri',
        mongodb_write_uri,
    )
    .config(
        'spark.mongodb.read.connection.uri',
        mongodb_read_uri,
    )
    .getOrCreate()
)


app = FastAPI()


@app.get("/test", response_class=HTMLResponse)
async def test() -> str:
    return '<svg height="100" width="100"> <circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" /> Sorry, your browser does not support inline SVG.</svg>'


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None) -> Dict[str, Any]:
    """Multiplication de deux nombres entiers.

    Cette fonction ne sert pas à grand chose.

    Parameters
    ----------
    item_id : int
        Le premier nombre entier.
    nombre2 : int
        Le second nombre entier.

        Avec une description plus longue.
        Sur plusieurs lignes.

    Returns
    -------
    int
        Le produit des deux nombres.
    """
    return {"item_id": item_id, "q": q}


@app.get("/product_sold_most")
async def product_sold_most() -> List[Dict[str, Any]]:
    df = (
        SparkSession.getActiveSession()
        .read.format("mongodb")
        .option("database", 'test')
        .option("collection", 'coll_full')
        .load()
    )
    df_group = df.groupBy('StockCode').sum('Quantity')
    final = df_group.agg(
        {'sum(Quantity)': 'max'},
    )

    return final.toJSON().collect()


@app.get("/group_by_invoice")
async def group_by_invoice() -> List[Dict[str, Any]]:
    df = (
        SparkSession.getActiveSession()
        .read.format("mongodb")
        .option("database", 'test')
        .option("collection", 'coll_full')
        .load()
    )
    df_total = df.withColumn('Total', df['Quantity'] * df['UnitPrice'])
    final = df_total.groupBy('InvoiceNo').sum('Total')
    return final.toJSON().collect()


def start() -> None:

    # Launched with `poetry run start` at root level
    uvicorn.run(
        "retails_analysis.dispatch:app",
        host=config["LISTEN_HOST"],
        port=int(config["LISTEN_PORT"]),
        reload=True,
    )
