#!/bin/bash

NAME="podwebhooks_stormy_captain_hook_1"
SCRIPT="static_clone.py"
EXTRA="static_domains.py"

set -x

# copy stuff into container
docker cp ${SCRIPT} ${NAME}:/tmp/${SCRIPT} 
docker cp ${EXTRA} ${NAME}:/tmp/${EXTRA} 

# execute order 66
docker exec -it ${NAME} python /tmp/${SCRIPT}

# clean up
docker exec -it ${NAME} rm -f /tmp/${SCRIPT} /tmp/${EXTRA}

set +x


