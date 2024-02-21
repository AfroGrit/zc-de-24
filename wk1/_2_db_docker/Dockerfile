# Use official Python image
FROM python:3.12-slim-bullseye

# Set environment variable
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# ingest pipeline
COPY data_ingest.py data_ingest.py

# Install Python libraries for DS
RUN apt-get -y update
RUN apt-get install -y wget
RUN apt-get install -y libpq-dev gcc
RUN pip install pandas sqlalchemy psycopg2


# Run Jupyter by default
ENTRYPOINT [ "python", "data_ingest.py" ]