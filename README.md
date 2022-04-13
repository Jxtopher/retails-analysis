# Retails analysis (2022-04-11)


## Project deployment

The project is composed of 6 services:
- retails-analysis-api: http://localhost
- jupyter-notebook: http://localhost:8888
- spark-worker
- spark-master http://localhost:8080
- mongo
- mongo-express: http://localhost:8081

You can used the docker-compose for deployment the project as folllow:

1. First copy and edit the environment variables.

```bash
cp .env-example .env
```

2. Deployment the project

```bash
docker-compose build .
docker-compose up
```

3. Please create database in mongodb, corresponding to 'MONNGO_DB' in .env file


4. Import the dataset 'retails data', if it hasn't already been done. Only inside the container for this moment.

```bash
docker exec -it retails-analysis-api bash
poetry run import '/apps/dataset/Online Retail.xlsx'
```

5. Connect à http://localhost and use retails analysis api route

## Fonctionnalités

- [x] Statistics available through an API route
- [x] Import dataset only files on format xlsx
- [x] Continuous integration with GitHub Actions
- [x] Creation of the work environment: docker-compose and Dockerfile
- [ ] Improve how to import files, use an API route
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

## References
- MongoDB Connector for Spark: https://www.mongodb.com/docs/spark-connector/current/
- Jupyter tutorial: https://www.sicara.ai/blog/2017-05-02-get-started-pyspark-jupyter-notebook-3-minutes