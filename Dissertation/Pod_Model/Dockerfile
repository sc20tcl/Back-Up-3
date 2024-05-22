# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
# Note: Make sure to create this file with your Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Install k6
RUN apt-get update && \
    apt-get install -y curl wget && \
    curl -s https://api.github.com/repos/grafana/k6/releases/latest | \
    grep browser_download_url | \
    grep amd64.deb | \
    cut -d '"' -f 4 | \
    wget -i - -O k6.deb && \
    dpkg -i k6.deb && \
    rm k6.deb && \
    apt-get remove -y curl wget && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME podTestOrchestrator

# Run testOrchestrator.py when the container launches
CMD ["python", "podTestOrchestrator.py"]
