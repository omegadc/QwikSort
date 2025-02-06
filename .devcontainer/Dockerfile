# use latest official debian image from docker hub
FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

# Set the working directory in the container
WORKDIR /workspace

# Copy pip requirements file
COPY requirements.txt ./

# Install system dependencies
# RUN sudo rm /bin/sh && sudo ln -s /bin/bash /bin/sh
# RUN sudo rm /bin/sh && sudo ln -s /bin/bash /bin/sh
RUN apt-get update && apt-get install -y bash \
    && rm -rf /var/lib/apt/lists/*
# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

#Default shell to Bash
CMD ["bash"]