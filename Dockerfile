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

##### 1. Leaf Image: Style #####
FROM base as style

COPY style /build/style
COPY style-resources/tests /build/tests
COPY style-resources/resources /applications/resources
COPY style-resources/datasets /applications/datasets
COPY style-resources/models /applications/models

ENV APP_RESOURCE_DIR /applications
ENV PYTHONPATH /applications

ARG skip_tests

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

RUN pip install python-multipart
RUN mv /build/style /applications/style
EXPOSE 8080
COPY entrypoints/style-app-entrypoint.sh /applications/style-app-entrypoint.sh
ENTRYPOINT ["sh", "/applications/style-app-entrypoint.sh"]

##### 2. Leaf Image: Portfolio #####
#### 1. Builder
FROM node:latest as portfolio_build

RUN npm install react-scripts -g --silent

WORKDIR /applications

COPY portfolio/package.json /applications/
COPY portfolio/package-lock.json /applications/

RUN npm ci

ENV PATH /applications/node_modules/.bin:$PATH
COPY portfolio /applications/.

RUN npm run build

#COPY entrypoints/portfolio-app-entrypoint.sh /applications/portfolio-app-entrypoint.sh
#ENTRYPOINT ["sh", "/applications/portfolio-app-entrypoint.sh"]

#### 2. Leaf
FROM nginx:stable-alpine as portfolio
COPY --from=portfolio_build /applications/build /usr/share/nginx/html
COPY portfolio/nginx/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
