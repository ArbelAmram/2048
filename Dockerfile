# a Dockerfile tailored to use Conda for dependency management. 

# Use the Miniconda3 image as a base
FROM continuumio/miniconda3

# Set the working directory in the container
WORKDIR /app

# Copy the environment.yml file to the working directory
COPY environment.yml .

# Create the Conda environment
RUN conda env create -f environment.yml

# Make RUN commands use the new environment
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

# Copy the rest of the application code to the working directory
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 80

# Specify the command to run the app
CMD ["conda", "run", "--no-capture-output", "-n", "myenv", "python", "app.py"]
