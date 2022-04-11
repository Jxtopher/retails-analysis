# import plotly.graph_objects as go
import uvicorn

from dotenv import dotenv_values
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from os.path import exists
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from typing import Optional, Dict, Any, List


# Loading environment vars
config = dotenv_values(".env")
if not exists(".env"):
    raise Exception('[-] File ' + ".env" + ' does not exist')

# Spark initialisation
mongodb_write_uri = (
    'mongodb://'
    + str(config['MONNGO_USER'])
    + ':'
    + str(config['MONNGO_PWD'])
    + '@'
    + str(config['MONNGO_HOST'])
    + '/test.coll?authSource=admin'
)
mongodb_read_uri = (
    'mongodb://'
    + str(config['MONNGO_USER'])
    + ':'
    + str(config['MONNGO_PWD'])
    + '@'
    + str(config['MONNGO_HOST'])
    + '/test.coll_full?authSource=admin'
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
    return '<svg height="100" width="100"></svg>'


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


@app.get("/product_sold_most", response_class=JSONResponse)
async def product_sold_most() -> List[str]:
    """Get product sold the most"""
    df = SparkSession.getActiveSession().read.format("mongodb").load()
    df_sum_quantities = df.groupBy('StockCode').agg(F.sum('Quantity').alias('Quantities'))
    df_max_quantity = df_sum_quantities.agg(F.max('Quantities').alias("Quantities"))
    df_joined = df_max_quantity.join(df_sum_quantities, "Quantities", "inner")
    return df_joined.toJSON().collect()


@app.get("/group_by_invoice", response_class=JSONResponse)
async def group_by_invoice() -> List[str]:  # List[Dict[str, Any]]
    """Group all transactions by invoice"""
    df = SparkSession.getActiveSession().read.format("mongodb").load()
    df_total = df.withColumn('Total', df['Quantity'] * df['UnitPrice'])
    final = df_total.groupBy('InvoiceNo').sum('Total')
    return final.toJSON().collect()


@app.get("/customer_spent_most", response_class=JSONResponse)
async def customer_spent_most() -> List[str]:
    """Get the customer spent the most money"""
    df = SparkSession.getActiveSession().read.format("mongodb").load()
    df_total = df.withColumn('S/Total', df['Quantity'] * df['UnitPrice'])
    df_customer_spending = df_total.groupBy('CustomerID').agg(
        F.round(F.sum('S/Total'), 4).alias('Total')
    )
    df_spent_most = df_customer_spending.agg(F.max('Total').alias("Total"))
    df_joined = df_spent_most.join(df_customer_spending, "Total", "inner")
    return df_joined.toJSON().collect()


# @app.get("/ratio_between_price_quantity", response_class=JSONResponse)
# async def ratio_between_price_quantity() -> List[str]:
#     """Get the ratio between price and quantity for each invoice"""
#     df = SparkSession.getActiveSession().read.format("mongodb").load()
#     final = df.groupBy('InvoiceNo').agg(
#         F.sum('Quantity').alias('Quantities'), F.sum('UnitPrice').alias('Prices')
#     )
#     df_total = final.withColumn('Ratio', final['Prices'] / final['Quantities'])

#     df_total.show()
#     return []


@app.get("/chart_distribution_prices", response_class=HTMLResponse)
async def chart_distribution_prices() -> Any:
    df = SparkSession.getActiveSession().read.format("mongodb").load()
    distribution_prices = df.groupBy('UnitPrice').agg(F.sum('Quantity').alias('Quantities'))
    distribution_prices.show()

    # fig = go.Figure(
    #     data=[
    #         go.Histogram(
    #             x=distribution_prices.toPandas()['UnitPrice'],
    #         )
    #     ],
    #     # data=[go.bar(distribution_prices.toPandas(), x='UnitPrice', y='Quantities')],
    #     layout_title_text="A Figure Displaying Itself",
    # )

    return "fig.to_html()"


def start() -> None:
    """Launched with `poetry run start` at root level"""
    uvicorn.run(
        "retails_analysis.dispatch:app",
        host=config["RATAILS_ANALYSIS_API_LISTEN_HOST"],
        port=int(str(config["RATAILS_ANALYSIS_API_LISTEN_PORT"])),
        reload=True,
    )
