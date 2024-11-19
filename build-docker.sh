#!/bin/bash

set -ex

########### ENV VARS ###########
NAME=chainscout
IMAGE=blockchain_${NAME}
FLAG=HTB{pl4c3h0ld3r}
PUBLIC_IP=127.0.0.1
HANDLER_PORT=8000
LOCAL_RPC_PORT=5000
PUBLIC_RPC_PORT=8888
FRONTEND_PORT=8080
ANVIL_LOGFILE=anvil_output.log
################################

docker rm -f $IMAGE
docker build --tag=$IMAGE:latest ./challenge/ && \
docker run --rm -it \
    -p "$PUBLIC_RPC_PORT:$LOCAL_RPC_PORT" \
    -p "$FRONTEND_PORT:$FRONTEND_PORT" \
    -p "$HANDLER_PORT:$HANDLER_PORT" \
    -e PUBLIC_IP=$PUBLIC_IP \
    -e PUBLIC_RPC_PORT=$PUBLIC_RPC_PORT \
    -e LOCAL_RPC_PORT=$LOCAL_RPC_PORT \
    -e HANDLER_PORT=$HANDLER_PORT \
    -e ANVIL_LOGFILE=$ANVIL_LOGFILE \
    -e FLAG=$FLAG \
    --name $IMAGE \
    $IMAGE:latest
