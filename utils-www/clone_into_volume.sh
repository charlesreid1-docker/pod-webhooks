#!/bin/bash

SCRIPT="static_clone.py"

echo docker cp ${SCRIPT} ${NAME}:/tmp/${SCRIPT} 
echo docker exec -it ${NAME} python /tmp/${SCRIPT}


