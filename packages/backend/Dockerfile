# build context: 'backend/'
# set base image
FROM python:3.7

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
RUN mkdir /backend
WORKDIR /backend

# install dependencies
COPY requirements.txt ./
RUN apt-get update && apt-get install -y postgresql-client
RUN python3 -m pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

# Copy project
COPY . ./

# Expose application port
EXPOSE 8000