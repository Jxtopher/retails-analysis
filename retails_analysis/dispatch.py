# -----------------------------------------------------------
# Start the dispatch
# -----------------------------------------------------------
import plotly.graph_objects as go
import uvicorn

from dotenv import dotenv_values
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from os.path import exists
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from typing import Any, List


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
    + '/'
    + str(config['MONNGO_DB'])
    + '.'
    + str(config['MONNGO_COLL'])
    + '?authSource=admin'
)
mongodb_read_uri = (
    'mongodb://'
    + str(config['MONNGO_USER'])
    + ':'
    + str(config['MONNGO_PWD'])
    + '@'
    + str(config['MONNGO_HOST'])
    + '/'
    + str(config['MONNGO_DB'])
    + '.'
    + str(config['MONNGO_COLL'])
    + '?authSource=admin'
)

(
    SparkSession.builder.appName("Retails analysis")
    .master('spark://' + str(config['SPARK_MASTER_HOST']) + ':' + str(config['SPARK_MASTER_PORT']))
    .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.2')
    .config(
        'spark.mongodb.input.uri',
        mongodb_write_uri,
    )
    .config(
        'spark.mongodb.output.uri',
        mongodb_read_uri,
    )
    .getOrCreate()
)


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root() -> str:
    """Suggest consulting the documentation"""
    return "Please consult the doc at http://localhost/docs"


@app.get("/product_sold_most", response_class=JSONResponse)
async def product_sold_most() -> List[str]:
    """Get product sold the most"""
    df = SparkSession.getActiveSession().read.format("com.mongodb.spark.sql.DefaultSource").load()
    df_sum_quantities = df.groupBy('StockCode').agg(F.sum('Quantity').alias('Quantities'))
    df_max_quantity = df_sum_quantities.agg(F.max('Quantities').alias("Quantities"))
    df_joined = df_max_quantity.join(df_sum_quantities, "Quantities", "inner")
    return df_joined.toJSON().collect()


@app.get("/group_by_invoice", response_class=JSONResponse)
async def group_by_invoice() -> List[str]:  # List[Dict[str, Any]]
    """Group all transactions by invoice"""
    df = SparkSession.getActiveSession().read.format("com.mongodb.spark.sql.DefaultSource").load()
    df_total = df.withColumn('Total', df['Quantity'] * df['UnitPrice'])
    final = df_total.groupBy('InvoiceNo').sum('Total')
    return final.toJSON().collect()


@app.get("/customer_spent_most", response_class=JSONResponse)
async def customer_spent_most() -> List[str]:
    """Get the customer spent the most money"""
    df = SparkSession.getActiveSession().read.format("com.mongodb.spark.sql.DefaultSource").load()
    df_total = df.withColumn('S/Total', df['Quantity'] * df['UnitPrice'])
    df_customer_spending = df_total.groupBy('CustomerID').agg(
        F.round(F.sum('S/Total'), 4).alias('Total')
    )
    df_spent_most = df_customer_spending.agg(F.max('Total').alias("Total"))
    df_joined = df_spent_most.join(df_customer_spending, "Total", "inner")
    return df_joined.toJSON().collect()


@app.get("/ratio_between_price_quantity", response_class=JSONResponse)
async def ratio_between_price_quantity() -> List[str]:
    """Get the ratio between price and quantity for each invoice"""

    # TODO: The ratio  between price and quantity is not correctly calculated
    df = SparkSession.getActiveSession().read.format("mongodb").load()
    final = df.groupBy('InvoiceNo').agg(
        F.sum('Quantity').alias('Quantities'), F.sum('UnitPrice').alias('Prices')
    )
    df_total = final.withColumn('Ratio', final['Prices'] / final['Quantities'])

    df_total.show()
    return []


@app.get("/char_select_country", response_class=HTMLResponse)
async def char_select_country() -> Any:
    """List of all available countries"""
    df = SparkSession.getActiveSession().read.format("com.mongodb.spark.sql.DefaultSource").load()
    get_countries = df.groupBy('Country').agg(F.count('Country'))

    html = ""
    for country, _ in get_countries.collect():
        html += '<a href="/chart_distribution_of_products/' + country + '">' + country + '</a><br/>'
    return html


@app.get("/chart_distribution_of_products/{country}", response_class=HTMLResponse)
async def chart_distribution_of_products(country: str) -> Any:
    """Create the chart distribution of products for a country"""
    df = SparkSession.getActiveSession().read.format("com.mongodb.spark.sql.DefaultSource").load()
    get_countries = df.groupBy('Country').agg(F.count('Country'))

    if get_countries.filter(get_countries.Country == country).count() == 1:
        azer = df.filter(F.col('Country') == country)
        fig = go.Figure(
            data=[go.Bar(x=azer.toPandas()['StockCode'], y=azer.toPandas()['Quantity'])],
            layout=go.Layout(height=600, width=800),
            layout_title_text="Products distribution for " + country,
            layout_xaxis_title="Stock code",
            layout_yaxis_title="Quantity",
        )
        return fig.to_html()
    else:
        return "Country not found."


@app.get("/chart_distribution_of_prices", response_class=HTMLResponse)
async def chart_distribution_prices() -> Any:
    """Distribution of prices"""
    df = SparkSession.getActiveSession().read.format("com.mongodb.spark.sql.DefaultSource").load()
    distribution_prices = df.groupBy('UnitPrice').agg(F.sum('Quantity').alias('Quantities'))
    distribution_prices.show()

    # TODO: need to be fixed, the histogram does not consider the quantity
    fig = go.Figure(
        data=[
            go.Histogram(
                x=distribution_prices.toPandas()['UnitPrice'],
            )
        ],
        layout=go.Layout(height=600, width=800),
        layout_title_text="Distribution of prices",
        layout_xaxis_title="Prices",
        layout_yaxis_title="Quantity",
    )

    # TODO: Other proposal, not working at the moment
    # fig = go.Figure(
    #     data=[
    #         go.Bar(
    #             x=distribution_prices.toPandas()['UnitPrice'],
    #             y=distribution_prices.toPandas()['Quantities'],
    #         )
    #     ],
    #     layout=go.Layout(height=600, width=800),
    #     layout_title_text="Distribution of prices",
    #     layout_xaxis_title="Prices",
    #     layout_yaxis_title="Quantity",
    # )
    return fig.to_html()


def start() -> None:
    """Launched with `poetry run start` at root level"""
    uvicorn.run(
        "retails_analysis.dispatch:app",
        host=config["RATAILS_ANALYSIS_API_LISTEN_HOST"],
        port=int(str(config["RATAILS_ANALYSIS_API_LISTEN_PORT"])),
        reload=True,
    )
