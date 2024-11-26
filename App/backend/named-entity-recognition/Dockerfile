# Use an official Python runtime as a parent image
FROM python:3.8-slim AS build

# Upgrade pip to the latest version
RUN python -m pip install --upgrade pip

# Set the working directory in the container to /named_entity_recognition
WORKDIR /named_entity_recognition

# Create a virtual environment and activate it
RUN python -m venv /venv

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    python3-dev \
    libffi-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only the necessary files for building the application
COPY requirements.txt ./

# Install dependencies using pip
RUN /venv/bin/pip install -r requirements.txt

# Download the knowledge base for the entity linker
RUN /venv/bin/python -m spacy_entity_linker "download_knowledge_base"

# Optionally, remove the build dependencies if they are no longer needed
RUN apt-get purge -y --auto-remove gcc g++ python3-dev libffi-dev build-essential

# Start a new build stage
FROM python:3.8-slim AS final

# Set the working directory in the container to /named_entity_recognition
WORKDIR /named_entity_recognition

# Copy the virtual environment from the build stage
COPY --from=build /venv /venv

# Copy the application code into the container
COPY . .

# Declare the port that the application uses
EXPOSE 5051

# Use the shell form to allow environment variable expansion
CMD /venv/bin/python -m uvicorn app:app --host 0.0.0.0 --port 5051 --workers 2

# docker buildx build --platform linux/amd64 -t stiborv/ner:latest . --push