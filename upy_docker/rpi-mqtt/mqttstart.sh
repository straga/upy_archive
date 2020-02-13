#!/bin/bash

echo "Configuring mosquitto daemon ..."
cat > "/etc/mosquitto/mosquitto.conf" <<EOF
persistence true
persistence_location /mqtt/data/
EOF

echo "Starting mosquitto daemon ..."
mosquitto
