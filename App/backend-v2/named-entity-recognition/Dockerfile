# Use an official Python runtime as a parent image
FROM python:3.8-slim as builder

# Set the working directory in the container to /named_entity_recognition
WORKDIR /named_entity_recognition

# Set environment variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

# Create a virtual environment and activate it
RUN python -m venv /venv

# Copy only the necessary files for building the application
COPY requirements.txt ./
COPY . .

# Install dependencies using pip
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

# Download the knowledge base for the entity linker
RUN /venv/bin/python -m spacy_entity_linker "download_knowledge_base"

# Start a new build stage
FROM python:3.8-slim as final

# Set the working directory in the container to /named_entity_recognition
WORKDIR /named_entity_recognition

# Copy the virtual environment from the builder stage
COPY --from=builder /venv /venv

# Copy the application code into the container
COPY . .

# Declare the port that the application uses
EXPOSE 5000

# Run the application
ENTRYPOINT ["/venv/bin/python", "-m", "uvicorn"]
CMD ["app:app", "--host", "0.0.0.0", "--port", "5000", "--workers", "2"]