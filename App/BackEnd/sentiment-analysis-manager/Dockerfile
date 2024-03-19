# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container to sentiment analysis manager
WORKDIR /sentiment-analysis-manager

# Add the current directory contents into the container at /data-extraction-manager
ADD . /sentiment-analysis-manager

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org --no-cache-dir -r requirements.txt

# Make port 9070 available to the world outside this container
EXPOSE 9071

# Run app.py when the container launches
CMD ["python", "main.py"]