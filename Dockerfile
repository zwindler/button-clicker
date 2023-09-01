# Use the official Python image as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the application files to the container
COPY buttonclicker.py /app/
COPY templates /app/templates/
COPY static /app/static/

# Install the required Python packages
RUN pip install psycopg2-binary flask

# Expose the port the application will run on
EXPOSE 8080

# Define the command to run the application
CMD ["python", "buttonclicker.py"]
