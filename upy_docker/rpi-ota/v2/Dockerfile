FROM rpi-python3/local:latest


RUN apt-get update && apt-get install -y \
     python3-setuptools \
     --no-install-recommends && \
     rm -rf /var/lib/apt/lists/*

RUN pip3 install wheel


RUN pip3 install aiohttp

# # RUN mkdir /opt
# COPY server /opt/
COPY server /opt/server

WORKDIR /opt/server

# Define default command
CMD ["python3", "/opt/server/ota_serverv2.py"]
