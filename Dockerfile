FROM python:3.9-slim-bullseye as base

RUN apt-get update -y && \
    apt-get install -y \
       libblas-dev \
       liblapack-dev \
       libpng-dev \
       locales \
       libssl-dev \
       libffi-dev \
       libfreetype6-dev \
       vim

RUN mkdir -p /build/tests
RUN mkdir /applications

COPY requirements.txt /build/requirements.txt
RUN pip3 install -r /build/requirements.txt

#RUN pip3 install \ #  --no-color --progress-bar off \
    #-r /build/requirements.txt \
    #-r /build/requirements-test.txt # | ts -i '%.S'

COPY requirements-test.txt /build/requirements-test.txt
RUN pip3 install -r /build/requirements-test.txt

COPY .isort.cfg /build/.isort.cfg
COPY pytest.ini /build/pytest.ini
COPY .flake8 /build/.flake8

ENV APP_RESOURCE_DIR /applications
ENV PYTHONPATH /applications

ARG skip_tests

##### 1. Leaf Image: Style #####
FROM base as style

COPY style /build/style
COPY style-resources/tests /build/tests
COPY style-resources/resources /applications/resources
COPY style-resources/datasets /applications/datasets
COPY style-resources/models /applications/models



RUN \
    if [ "$skip_tests" = "" ] ; then \
        black \
           -t py39 -l 80 \
           --check $(find /build/style /build/tests -name "*.py") \
      && \
        # isort --df --settings-path=/build/.isort.cfg --check /build/style \
      #&& \
        flake8 --config=/build/.flake8 /build/style \
      && \
        pytest /build/tests ; \
      else \
        echo "Skipping tests" ; \
    fi

RUN mv /build/style /applications/style
EXPOSE 8080

COPY entrypoints/style-app-entrypoint.sh /applications/style-app-entrypoint.sh
ENTRYPOINT ["sh", "/applications/style-app-entrypoint.sh"]

##### 2. Leaf Image: inflation #####
FROM base as inflation

COPY common /applications/common
COPY inflation /build/inflation
COPY inflation-resources/tests /build/tests
COPY inflation-resources/data /build/data
RUN \
    if [ "$skip_tests" = "" ] ; then \
        black \
           -t py39 -l 80 \
           --check $(find /build/inflation /build/tests -name "*.py") \
      && \
        flake8 --config=/build/.flake8 /build/inflation \
      && \
        pytest /build/tests ; \
      else \
        echo "Skipping tests" ; \
    fi


RUN mkdir -p /applications/downloaded-files/
RUN mv /build/inflation /applications/inflation

EXPOSE 8000

COPY entrypoints/inflation-app-entrypoint.sh /applications/inflation-app-entrypoint.sh
ENTRYPOINT ["sh", "/applications/inflation-app-entrypoint.sh"]
