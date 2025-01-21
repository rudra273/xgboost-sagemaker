# Stage 1: Build Stage (Using Alpine)
FROM python:3.9-alpine AS build

# Set the working directory
WORKDIR /src

# Install build dependencies for Alpine
RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev

# Copy only the requirements file first to leverage caching
COPY src/requirements.txt /src/

# Install dependencies in the build stage
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the entire source code (after installing dependencies)
COPY src/ /src/

# Stage 2: Final Stage (Using Slim Python)
FROM python:3.9-slim-bullseye

# Set the working directory
WORKDIR /src

# Copy installed dependencies from the build stage
COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

# Copy the source code from the build stage
COPY --from=build /src/ /src

# Clean up unnecessary files to reduce image size
RUN rm -rf /var/cache/apt/* /src/tests /src/docs /src/*.log /src/__pycache__

# Set the PYTHONPATH to include the src directory
ENV PYTHONPATH=/src

# Ensure Python output is not buffered
ENV PYTHONUNBUFFERED=TRUE

# Set the entrypoint for the container
ENTRYPOINT ["python3"]



# # Stage 1: Build Stage
# FROM python:3.9-alpine AS build

# # Set the working directory
# WORKDIR /src

# # Install dependencies and system packages
# RUN apk add --no-cache build-base

# # Copy requirements file
# COPY src/requirements.txt /src/

# # Install Python dependencies
# RUN pip3 install --no-cache-dir -r requirements.txt

# # Copy the source code
# COPY src/ /src/

# # Stage 2: Final Stage
# FROM python:3.9.21-bullseye

# # Set the working directory
# WORKDIR /src

# # Copy the installed dependencies from the build stage
# COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# # Copy the source code from the build stage
# COPY --from=build /src/ /src

# # Clean up unnecessary files
# RUN apk del build-base && rm -rf /var/cache/apk/* /src/tests /src/docs /src/*.log /src/__pycache__

# # Set the PYTHONPATH to include the src directory
# ENV PYTHONPATH=/src

# # Ensure Python output is not buffered
# ENV PYTHONUNBUFFERED=TRUE

# # Set the entrypoint for the container
# ENTRYPOINT ["python3"]

# FROM python:3.9.21-bullseye

# # Copy all project files, including the src directory
# COPY src/ src/

# # Install dependencies
# RUN pip3 install --no-cache-dir -r src/requirements.txt

# WORKDIR /src

# # Set the PYTHONPATH to include the src directory
# ENV PYTHONPATH=/src
# # ENV PYTHONPATH=/

# # Ensure Python output is not buffered
# ENV PYTHONUNBUFFERED=TRUE


# # Set the entrypoint for the container
# ENTRYPOINT ["python3"]

#__________

# # Stage 1: Build Stage
# FROM python:3.9-slim-bullseye AS build

# # Set the working directory
# WORKDIR /src

# # Copy only requirements file first to leverage caching
# COPY src/requirements.txt /src/

# # Install dependencies in the build stage
# RUN pip3 install --no-cache-dir -r requirements.txt

# # Copy the entire source code
# COPY src/ /src

# # Stage 2: Final Stage
# FROM python:3.9-slim-bullseye

# # Set the working directory
# WORKDIR /src

# # Copy installed dependencies from the build stage
# COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
# COPY --from=build /usr/local/bin /usr/local/bin

# # Copy the source code from the build stage
# COPY --from=build /src/ /src


# # Clean up unnecessary files to reduce image size
# RUN rm -rf /var/cache/apt/* /src/tests /src/docs /src/*.log /src/__pycache__

# # Set the PYTHONPATH to include the src directory
# ENV PYTHONPATH=/src

# # Ensure Python output is not buffered
# ENV PYTHONUNBUFFERED=TRUE

# # Set the entrypoint for the container
# ENTRYPOINT ["python3"]
