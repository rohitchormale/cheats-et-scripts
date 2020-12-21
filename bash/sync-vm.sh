#!/bin/bash

LOCAL_DIR="/temp/foo"
EXCLUDE="--exclude 'foo' --exclude 'bar' --exclude 'baz/'"
REMOTE_HOST="user@remote-host"
REMOTE_DIR="/tmp/bar"
REMOTE_CONTAINER_DIR="<container-name/id>:/temp/foo"

rsync -urav $EXCLUDE $LOCAL_DIR/* "${REMOTE_HOST}:${REMOTE_DIR}"

ssh $REMOTE_HOST "rsync -e 'docker exec -i' -urav $EXCLUDE $REMOTE_DIR/* $REMOTE_CONTAINER_DIR"