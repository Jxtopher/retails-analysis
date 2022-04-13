FROM python:3.8

# hadolint ignore=DL3008
RUN pip install --no-cache-dir poetry==2.0.5 \
&& apt-get update -y \
&& apt-get install -yqq --no-install-recommends openjdk-11-jdk \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

CMD ["tail", "-f", "/dev/null"]