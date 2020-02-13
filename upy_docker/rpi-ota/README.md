    docker-compose -f ota.yml -p ota_esp build
    docker-compose -f ota.yml -p ota_esp up -d
    docker-compose -f ota.yml -p ota_esp down
    docker-compose -f ota.yml -p ota_esp down -v