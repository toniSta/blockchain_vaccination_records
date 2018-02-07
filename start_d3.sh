#!/usr/bin/env bash
dir_name=${PWD##*/}
dir_name_stripped=${dir_name//_}
docker run --name d3 -it -p 9000 --network ${dir_name_stripped}_default -e "START_CLI=1" -e "NEIGHBORS_HOST_PORT=d1:9000,a2:9000,d2:9000" full_client_image
