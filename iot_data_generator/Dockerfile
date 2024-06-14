# Use an official Python runtime as a parent image
FROM --platform=linux/amd64 python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . .
EXPOSE 80

ENV EVENT_HUB_CONNECTION_STR=Endpoint=sb://axpo-eventhub.servicebus.windows.net/;SharedAccessKeyName=new;SharedAccessKey=Fsx6RJoXg1YMMerSVqcssh+I7NQI659t2+AEhN0gvxc=;EntityPath=testing-1
ENV EVENT_HUB_NAME=testing-1
ENV GENERAL_INTERVAL_MS=1000
ENV GENERAL_LOGGING_LEVEL=20

# Run run.py when the container launches
CMD ["python", "run.py"]
