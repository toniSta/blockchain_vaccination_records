#!/usr/bin/env bash
dir_name=${PWD##*/}
dir_name_stripped=${dir_name//_}
mytitle="a6"
echo -e '\033]2;'$mytitle'\007'
docker run --name a6 -it -p 9000 --network ${dir_name_stripped}_default -e "REGISTER_AS_ADMISSION=1"  -e "CONFIRM_BLOCKSENDING=1" -e "NEIGHBORS_HOST_PORT=a2:9000,genesis_admission:9000" full_client_image
