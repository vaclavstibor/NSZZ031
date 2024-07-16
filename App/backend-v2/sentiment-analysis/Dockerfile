# Define the builder stage with ARM architecture
#FROM --platform=linux/amd64 python:3.8-slim-buster AS build
FROM python:3.8-slim-buster AS build

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Set the working directory
WORKDIR /sentiment_analysis

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Install the dependencies with no-binary to ensure compatibility
#RUN pip install --no-binary :all: -r requirements.txt

# Define the final stage with ARM architecture
#FROM --platform=linux/amd64 python:3.8-slim-buster AS final
FROM python:3.8-slim-buster AS final

# Set the working directory
WORKDIR /sentiment_analysis

# Copy the installed packages from the builder stage
COPY --from=build /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

# Copy the rest of the application
COPY . .

# Expose the application port
EXPOSE 8080

# Only one worker to speed up on local
#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "2"]
CMD uvicorn app:app --host 0.0.0.0 --port 8080 --workers 2

#docker buildx create --use
#docker buildx build --platform linux/amd64 -t sa-asyncio:latest .