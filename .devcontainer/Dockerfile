# use latest official debian image from docker hub
FROM debian:latest

# Set the working directory in the container
# WORKDIR /app

# Copy pip requirements file
# COPY requirements.txt

# Install system dependencies
# RUN sudo rm /bin/sh && sudo ln -s /bin/bash /bin/sh
RUN sudo rm /bin/sh && sudo ln -s /bin/bash /bin/sh
RUN apt update && apt upgrade -y
# Dependencies for debian
RUN apt install curl git python3 vim --no-install-recommends &&\
    apt-get clean 

RUN apt install python3-pip python3.12 -y

ENV VIRTUAL_ENV=/opt/venv

RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN source venv/bin/activate
RUN pip install -r requirements.txt --break-system-packages

# Run python program
CMD ["tail", "-f","/dev/null"]