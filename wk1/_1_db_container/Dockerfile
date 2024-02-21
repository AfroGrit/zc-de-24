# Use official Python image
FROM python:3.12-slim-bullseye

# Set environment variable
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# pipeline
COPY pipeline.py pipeline.py

# Install Python libraries for DS
RUN pip install numpy pandas matplotlib scikit-learn jupyter pyarrow

# Run Jupyter by default
CMD ["jupyter", "lab", "--ip='0.0.0.0'", "--allow-root"]