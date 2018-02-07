#!/usr/bin/env bash
dir_name=${PWD##*/}
dir_name_stripped=${dir_name//_}
docker run --name a5 -it -p 9000 --network ${dir_name_stripped}_default -e "REGISTER_AS_ADMISSION=1"  -e "CONFIRM_BLOCKSENDING=1" -e "NEIGHBORS_HOST_PORT=genesis_admission:9000,d1:9000" full_client_image
