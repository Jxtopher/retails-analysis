# Retails analysis (2022-04-11)


## Project deployment

The project is composed of 6 services:
- retails-analysis-api: http://localhost
- jupyter-notebook http://localhost:81
- spark-worker
- spark-master
- mongo
- mongo-express

You can used the docker-compose for deployment the project as folllow:

```bash
docker-compose build .
docker-compose up
```

## Import the retails data

```bash
poetry run import path/file.xlsx
```


## Environment variables

Environment variables can be changed in file '.env'.


## Fonctionnalités

- [x] Statistics available through an API route
- [x] Import dataset only files on format xlsx
- [x] Continuous integration with GitHub Actions
- [x] Creation of the work environment: docker-compose and Dockerfile
- [ ] Set up Jupyter Notebook
- [ ] Better distinguish environment Prod and Dev
- [ ] More unit tests

## Retails analysis API

The API documentation is accessible at http://localhost/docs

Checks the project
```bash
poetry run mypy --config-file .config/mypy.cfg retails_analysis
poetry run black retails_analysis --config .config/black.cfg
poetry run flake8 --config .config/flake8.cfg
poetry run python -u -m unittest discover
```

## See
- MongoDB Connector for Spark: https://www.mongodb.com/docs/spark-connector/current/
- Jupyter tutorial: https://www.sicara.ai/blog/2017-05-02-get-started-pyspark-jupyter-notebook-3-minutes