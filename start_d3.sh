#!/usr/bin/env bash
dir_name=${PWD##*/}
dir_name_stripped=${dir_name//_}
mytitle="d3"
echo -e '\033]2;'$mytitle'\007'
docker run --name d3 -it -p 9000 --network ${dir_name_stripped}_default -e "START_CLI=1" -e "NEIGHBORS_HOST_PORT=d1:9000,a2:9000,d2:9000" full_client_image
