FROM ubuntu:latest

RUN useradd -MN orpheus
RUN apt-get -y update
RUN apt-get -y install git

# Setting timezone
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV LC_ALL en_US.UTF-8

# Installing base dependencies
RUN apt-get update && \
    apt-get install build-essential -y --no-install-recommends && \
    apt-get install software-properties-common -y --no-install-recommends && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Installing requirements from ./requirements/system/build.txt
COPY requirements/system/build.txt /opt/build.txt
RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update
RUN apt-get install --no-install-recommends -y `grep -v '#' /opt/build.txt | xargs`

# Installing pip
ADD https://bootstrap.pypa.io/get-pip.py /opt/get-pip.py
RUN python3.11 /opt/get-pip.py && \
    pip install --upgrade setuptools wheel && \
    pip install --upgrade pip && \
    pip install --upgrade setuptools


COPY ./ /work/
RUN pip install -r /work/requirements/base/requirements.txt

WORKDIR /work
