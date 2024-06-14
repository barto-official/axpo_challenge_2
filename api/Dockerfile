#!/usr/bin/env bash
# Use a multi-platform base image
FROM --platform=linux/amd64 python:3.10
# Use an official Python runtime as a parent image
#FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Expose port 3000 for the app
EXPOSE 3000

COPY . .
ENV MYSQL_USER=mirror_admin
ENV MYSQL_PASSWORD=B@rtek2000
ENV MYSQL_HOST=mirror.mysql.database.azure.com
ENV MYSQL_DATABASE=iot_testing

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
