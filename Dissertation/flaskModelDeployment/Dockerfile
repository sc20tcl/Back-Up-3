FROM python:3.10

WORKDIR /app

# Install system libraries required by h5py
RUN apt-get update && apt-get install -y \
    libhdf5-dev \
    pkg-config \
    gcc \
    && rm -rf /var/lib/apt/lists/*


COPY . /app

RUN pip3 install Flask
RUN pip3 install numpy
RUN pip3 install tensorflow==2.16.1 
RUN pip3 install joblib
RUN pip3 install scikit-learn 

EXPOSE 5000

CMD ["python", "model_api.py"]