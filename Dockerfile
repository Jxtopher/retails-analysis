FROM python:3.8

RUN pip install poetry

RUN echo "Acquire::http::Proxy \"http://192.168.1.2:8000\";" > /etc/apt/apt.conf.d/00aptproxy

# hadolint ignore=DL3008
RUN apt-get update -y \
&& apt-get install -yqq --no-install-recommends openjdk-11-jdk \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

#RUN git clone https://github.com/mongodb/mongo-spark.git \
#&& cd mongo-spark \
#&& ./gradlew clean check

CMD ["tail", "-f", "/dev/null"]