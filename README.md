# retails-analysis

Run a master spark
$ docker run -p 8080:8080 -p 7077:7077 bitnami/spark


# MongoDB Connector for Spark
https://www.mongodb.com/docs/spark-connector/current/


Checks
$ poetry run mypy --config-file .config/mypy.cfg retails_analysis
$ poetry run black retails_analysis --config .config/black.cfg
$ poetry run flake8 --config .config/flake8.cfg
$ poetry run python -u -m unittest discover


# Mise en place de jupyter

https://www.sicara.ai/blog/2017-05-02-get-started-pyspark-jupyter-notebook-3-minutes