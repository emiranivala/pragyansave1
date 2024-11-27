# Use the official Python 3.10 slim image with Debian Buster as the base image
FROM python:3.10.4-slim-buster

# Update package list and install required dependencies
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y git curl wget bash neofetch ffmpeg software-properties-common \
    && apt-get clean

# Copy the requirements file to the image
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install wheel \
    && pip3 install --no-cache-dir -U -r requirements.txt

# Set the working directory inside the container
WORKDIR /app

# Copy the rest of the project files to the container
COPY . .

# Expose port for the Flask application
EXPOSE 8000

# Start both Flask and Gunicorn in a single CMD (use bash to run both commands)
CMD bash -c "flask run -h 0.0.0.0 -p 8000 & gunicorn app:app & python3 -m pragyan"
