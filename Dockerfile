FROM python:3.4

ENV PYTHONUNBUFFERED 1
ENV DJANGO_CONFIGURATION Docker

RUN mkdir /app

# Set working dir
WORKDIR /app

ADD . /app

RUN apt-get update && apt-get install -y \
  gcc \
  # python-gdal \
  libgdal-dev \
  libgeos-dev \
  swig
  # npm \
  # nodejs

# install requirements
RUN pip install --upgrade pip
RUN pip install -r requirements/local.txt

## Node setup, runs postinstall script in package.json
# RUN ln -s /usr/bin/nodejs /usr/bin/node
# RUN npm install
# RUN npm run build

# static/media dirs
VOLUME /app/static
VOLUME /app/media

# build include paths env
ENV C_INCLUDE_PATH /usr/include/gdal/
ENV CPLUS_INCLUDE_PATH /usr/include/gdal/

ENV GEOS_LIBRARY_PATH /usr/lib/libgeos_c.so
ENV GDAL_LIBRARY_PATH /usr/lib/libgdal.so
