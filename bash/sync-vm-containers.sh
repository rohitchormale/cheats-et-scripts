#!/bin/bash

LOCAL_DIR="/temp/foo"
EXCLUDE="--exclude .idea/ --exclude env/ --exclude .pytest_cache/ --exclude *.pyc --exclude *egg-info --exclude *.log --exclude *.dat"
REMOTE_HOST="user@remote-host"
REMOTE_DIR="/tmp/bar"
REMOTE_CONTAINER="<container-name/id>"
REMOTE_CONTAINER_DIR="${REMOTE_CONTAINER}:/temp/foo"


echo "[*] Syncing $LOCAL_DIR with $REMOTE_DIR..."
echo ""
rsync -urav $EXCLUDE $LOCAL_DIR/* ${REMOTE_HOST}:${REMOTE_DIR}
resp1=$?

if [ $resp1 -ne 0 ]
then
	echo "[*] Failed. Aborting container syncing..."
	exit $resp1
fi


echo "[*] Syncing $REMOTE_DIR with container $REMOTE_CONTAINER_DIR..."
echo ""
ssh $REMOTE_HOST "rsync -e 'docker exec -i' -urav $EXCLUDE $REMOTE_DIR/* $REMOTE_CONTAINER_DIR"
resp2=$?

if [ $resp2 -ne 0 ]
then
	exit $resp2
else
	exit 0
fi

