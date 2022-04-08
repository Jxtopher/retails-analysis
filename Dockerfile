FROM python:3.10.4

RUN pip install poetry

# hadolint ignore=DL3008
# RUN apt-get update -y \
# && apt-get install -yqq --no-install-recommends maven \
# && apt-get clean \
# && rm -rf /var/lib/apt/lists/*

#RUN git clone https://github.com/mongodb/mongo-spark.git \
#&& cd mongo-spark \
#&& ./gradlew clean check

CMD ["tail", "-f", "/dev/null"]