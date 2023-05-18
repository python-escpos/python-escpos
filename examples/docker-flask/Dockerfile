# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

#Install the libcups library
RUN apt-get update -y && apt-get install libcups2-dev -y
# Install the Python packages
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install python-escpos --pre

# Install Git
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Copy the Flask app
COPY app.py .

# Expose the port the Flask app will run on
EXPOSE 8080

# Run the Flask app
CMD ["python", "app.py"]
