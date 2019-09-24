FROM ubuntu:18.04
LABEL maintainer="Henrique Breim <henrique@breim.com.br>"

# See http://bugs.python.org/issue19846
ENV LANG C.UTF-8

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN apt-get install -y libsm6 libxext6 libxrender-dev

RUN pip3 --no-cache-dir install --upgrade \
    pip \
    setuptools

RUN pip3 install tensorflow

COPY bashrc /etc/bash.bashrc
RUN chmod a+rwx /etc/bash.bashrc

RUN mkdir -p /data/app
COPY server.py /data/app
COPY requirements.txt /data/app

WORKDIR /data/app
RUN pip3 install -r requirements.txt

ENV PORT 8080
EXPOSE 8080

CMD python server.py
