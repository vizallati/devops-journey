FROM ubuntu:24.04

# Install common tools needed in playground environment
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv man-db \
    net-tools iputils-ping curl wget vim lsof htop whois sudo dnsutils gawk less \
    grep sed unzip tar gzip \bzip2 apt-utils && apt-get clean


COPY . /app

RUN python3 -m venv app/venv && app/venv/bin/pip install -r app/requirements.txt \
    && chmod u=rwx app/setup_db.py app/app.py app/static/images

EXPOSE 5000

CMD app/venv/bin/python app/setup_db.py; app/venv/bin/python app/app.py