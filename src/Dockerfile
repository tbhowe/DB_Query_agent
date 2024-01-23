FROM python:3.11

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Make port available to the world outside this container
EXPOSE 80

# Run agent.py when the container launches
CMD ["python3", "agent.py"]
