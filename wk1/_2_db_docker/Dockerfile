# Use official Python image
FROM python:3.12-slim-bullseye

# Set environment variable
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# ingest pipeline
COPY ingest_data.py ingest_data.py

# Install Python libraries for DS
RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2


# Run Jupyter by default
ENTRYPOINT [ "python", "ingest_data.py" ]