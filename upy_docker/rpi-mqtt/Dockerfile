FROM armhf/alpine:latest
MAINTAINER vostraga@gmail.com
USER root

RUN (apk add --update bash mosquitto mosquitto-clients && rm -rf /var/cache/apk/*)

ADD mqttstart.sh /bin/mqttstart.sh
RUN chmod -v +x /bin/mqttstart.sh

ENTRYPOINT [ "/bin/mqttstart.sh" ]
