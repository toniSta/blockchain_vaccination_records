#!/usr/bin/env bash
dir_name=${PWD##*/}
dir_name_stripped=${dir_name//_}
docker run --name a4 -it -p 9000 --network ${dir_name_stripped}_default -e "REGISTER_AS_ADMISSION=1"  -e "START_CLI=1" -e "NEIGHBORS_HOST_PORT=a3:9000,genesis_admission:9000" full_client_image
