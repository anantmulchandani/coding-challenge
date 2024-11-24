# Use an official Python image
FROM python:3.10-slim

# Set environment variables to prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory inside the container
WORKDIR /app

# Copy the application code
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
# EXPOSE 6200

# Making entrypoint executable
#RUN chmod +x entrypoint.sh

# Set entrypoint
ENTRYPOINT ["sh","./entrypoint.sh"]
