# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Expose port 8080 to the outside world
EXPOSE 8080

# Specify the command to run on container start
CMD ["python", "app.py"]
