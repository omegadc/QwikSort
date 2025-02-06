# use latest official debian image from docker hub
FROM python:latest

# Set the working directory in the container
WORKDIR /workspace

# Copy pip requirements file
COPY requirements.txt ./

# Install system dependencies
# RUN sudo rm /bin/sh && sudo ln -s /bin/bash /bin/sh
# RUN sudo rm /bin/sh && sudo ln -s /bin/bash /bin/sh
RUN apt update && apt upgrade -y
# Dependencies for debian
RUN apt install curl git python3 vim --no-install-recommends &&\
    apt-get clean 
RUN apt install neofetch
RUN apt install python3-pip python3.12 -y

RUN mkdir /opt/venv/ && chown root:student
ENV VIRTUAL_ENV=/opt/venv

RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN source venv/bin/activate
RUN pip install --no-cache-dir -r requirements.txt

# Run python program
CMD ["tail", "-f","/dev/null"]