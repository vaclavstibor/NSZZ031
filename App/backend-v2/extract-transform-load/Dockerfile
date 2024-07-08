# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

ENV AIRFLOW_HOME=/extract-transform-load/airflow

# Copy requirements.txt
COPY requirements.txt /extract-transform-load/requirements.txt

# Set the working directory in the container
WORKDIR /extract-transform-load

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Add the current directory contents into the container
ADD . /extract-transform-load

# Expose the port
EXPOSE 8080