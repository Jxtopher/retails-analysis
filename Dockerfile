FROM python:3.8

RUN echo "Acquire::http::Proxy \"http://192.168.1.2:8000\";" > /etc/apt/apt.conf.d/00aptproxy

# hadolint ignore=DL3008
RUN pip install --no-cache-dir poetry==2.0.5 \
&& apt-get update -y \
&& apt-get install -yqq --no-install-recommends openjdk-11-jdk \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

CMD ["tail", "-f", "/dev/null"]