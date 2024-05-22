# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container to /app
WORKDIR /app

# Install system libraries required by h5py
RUN apt-get update && apt-get install -y \
    libhdf5-dev \
    pkg-config \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install Flask
RUN pip3 install pandas

# Make port 5001 available to the world outside this container
EXPOSE 5001

# Run model_api.py when the container launches
CMD ["python", "traffic_api.py"]