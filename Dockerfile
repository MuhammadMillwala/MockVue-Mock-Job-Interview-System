# Use the official Python base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install OpenGL libraries
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx


# Install additional dependencies
RUN apt-get update && \
    apt-get install -y libglib2.0-0

# Install the app dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install DVC dependencies
RUN apt-get update && \
    apt-get install -y git && \
    pip install dvc

# Install spaCy and download 'en_core_web_sm' model
RUN pip install spacy && \
    python -m spacy download en_core_web_sm

# Copy the entire application to the container
COPY . .

# Set the environment variables
ENV FLASK_APP=server.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port on which the app will run
EXPOSE 5000

# Run the app when the container starts
CMD ["flask", "run"]