# setup

1. clone mistral
2. add plugin package
3. edit setup.cfg

mistral.actions =
    .
    .
    .
    custom.http = plugins.customactions:HTTPAction

4. In case of docker container, build container again
 docker build -t mistral:customeraction -f /tools/docker/Dockerfile .


5. In case of no docker then need to populate db
mistral-db-manage --config-file /etc/mistral/mistral.conf populate

6. check
pip install python-mistralclient
mistral action-list
