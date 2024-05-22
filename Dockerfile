# use the official python image from docker hub
FROM python:3.10-slim

# set environment variables to avoid python buffering
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements.txt to the container
COPY requirements.txt /app/

# Intall the dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code to the container
COPY . /app/

# Expose the port the application runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]