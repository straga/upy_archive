FROM rpi-python3/local:latest


# # Install yaml from apt, to also install the cpp lib.
# RUN apt-get update && apt-get install -y \
#     python3-dev \
#     python3-pip \
#     python3-yaml \
#     python3-lxml \
#     libxslt-dev \
#     libxml2-dev \
#     net-tools \
#     nmap \
#     openssh-client \
#     libpq-dev \
#     build-essential \
#     --no-install-recommends && \
#     rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
     python3-setuptools \
     --no-install-recommends && \
     rm -rf /var/lib/apt/lists/*

# Install home assistant dependencies


RUN pip3 install \
    paho-mqtt \
    netdisco \
    psutil \
    speedtest-cli \
    python-mpd2 \
    python-nmap \
    fritzconnection \
    sqlalchemy \
    wheel

RUN pip3 install \
    aiohttp_cors \
    fuzzywuzzy \
    warrant \
    mutagen \
    netdisco \
    distro \
    xmltodict


# Install home assistant
#RUN pip install homeassistant==0.49.1
RUN pip3 install homeassistant
RUN mkdir /data
RUN mkdir /data/.homeassistant
WORKDIR /data

# Define default command
CMD ["hass", "--config", "/data/.homeassistant"]
