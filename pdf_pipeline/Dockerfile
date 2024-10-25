# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Create the logs directory
RUN mkdir -p /logs

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies inside the container
RUN pip install -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the port MongoDB uses (optional, depends on your setup)
EXPOSE 27017

# Set the command to run the pipeline
CMD ["python", "src/pipeline_manager.py"]
