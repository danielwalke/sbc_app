# Use an official Python runtime as a parent image
FROM python:3.9-slim

ENV OPENBLAS_NUM_THREADS=8
ENV GOTO_NUM_THREADS=8
ENV OMP_NUM_THREADS=8

# Set the working directory in the container
# WORKDIR ./

# Copy the current directory contents into the container at /app
RUN mkdir /app
RUN mkdir /app/extdata 
COPY . /app
COPY extdata/sbcdata.csv /extdata/.
WORKDIR ./app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define envBironment variable
ENV NAME World

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
