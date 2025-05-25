# Use the official Python image
FROM python:3.13-slim

# Set the working directory
WORKDIR /API_TESTER

# Copy the application code
COPY api.py .

# Install Flask
RUN pip install Flask

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "api.py"]