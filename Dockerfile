# Use an official Python runtime as a parent image
FROM python:latest

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /code
COPY . /code/

# Expose the port Django runs on
EXPOSE 8000


# Change directory to the Django project financetracker
WORKDIR /code/financetracker

# Run Django's development server
CMD sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
