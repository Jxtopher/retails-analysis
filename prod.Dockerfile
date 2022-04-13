FROM python:3.8

RUN echo "Acquire::http::Proxy \"http://192.168.1.2:8000\";" > /etc/apt/apt.conf.d/00aptproxy

# hadolint ignore=DL3008
RUN pip install --no-cache-dir poetry==1.1.13 notebook==5.0\
&& apt-get update -y \
&& apt-get install -yqq --no-install-recommends openjdk-11-jdk \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

COPY ./  /apps
WORKDIR /apps

RUN poetry install \
&& poetry run import './dateset/Online Retail.xlsx' \
&& useradd user \
&& mkdir -p /home/user/ \
&& chown user:user /home/user/

COPY --chown=user:user './.config/jupyter_notebook_config.py' '/home/user/.jupyter/jupyter_notebook_config.py'

CMD ["bash", "-c", "runuser -l user -c 'jupyter notebook' & poetry run start"]