FROM python:3.7-stretch
MAINTAINER contact@onde-bleue.fr

RUN apt-get update && \
    apt-get install -y supervisor

WORKDIR /tmp
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY app /usr/src/app

EXPOSE 8000

COPY supervisor.conf /etc/supervisor/conf.d/fablab.conf
CMD ["/usr/bin/supervisord"]


