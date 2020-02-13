#FROM resin/armv7hf-debian-qemu:latest
FROM arm32v7/debian:buster-slim

# Install yaml from apt, to also install the cpp lib.
RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-pip \
    python3-yaml \
    python3-lxml \
    libxslt-dev \
    libxml2-dev \
    net-tools \
    nmap \
    openssh-client \
    mosquitto-clients \
    libpq-dev \
    build-essential \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*
