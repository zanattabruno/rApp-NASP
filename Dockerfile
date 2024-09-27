FROM python:3-slim-bullseye

# Update and upgrade system packages, and remove unnecessary packages in one step to reduce layers
RUN apt update && apt upgrade -y && apt autoremove -y && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy only requirements first for caching purposes
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN /usr/local/bin/python -m pip install --upgrade pip && \
    /usr/local/bin/python -m pip install -r requirements.txt

# Copy the rest of the source code
COPY src/ .

# Use an infinite loop to keep the container running
ENTRYPOINT ["tail", "-f", "/dev/null"]
