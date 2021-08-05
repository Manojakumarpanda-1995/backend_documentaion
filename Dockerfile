FROM ubuntu:18.04
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get update
# RUN a2enmod ssl
# RUN apt-get clean
# RUN apt-get update
# RUN apt-get -f install
RUN apt-get update && apt-get install -y apache2 apache2-utils
RUN apt-get install -y libmysqlclient-dev
RUN apt-get install -y libapache2-mod-wsgi-py3
RUN apt-get install -y supervisor
# RUN apt-get install -y libmysqlclient-dev
RUN mkdir -p /data/backend/backend
RUN apt-get -y install python3-pip
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install virtualenv
WORKDIR /data/backend
# RUN virtualenv -p python3 /data/backend/mmtxt
RUN virtualenv -p python3 mmtxt
RUN chmod +x /data/backend/
COPY ./000-default.conf /etc/apache2/sites-available/000-default.conf
COPY ./requirements.txt /data/backend/requirements.txt
COPY ./mysite-celery.conf /etc/supervisor/conf.d/backend-celery.conf
ADD ./backend /data/backend/backend
# RUN python3 -m pip install --upgrade pip
# RUN python3 -m pip install -r /data/backend/requirements.txt
RUN mmtxt/bin/pip install -r /data/backend/requirements.txt
RUN chmod +x /data/backend/backend
EXPOSE 80
COPY ./docker-entrypoint.sh /home/ubuntu/
RUN chmod +x /home/ubuntu/docker-entrypoint.sh
RUN ls /data/backend/backend
ENTRYPOINT ["/home/ubuntu/docker-entrypoint.sh"]

