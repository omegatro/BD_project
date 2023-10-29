#!/bin/bash
CONTAINER_ID=$(docker ps | grep my-mongo-container | while IFS=' ' read a b ; do echo $a; done)
docker stop $CONTAINER_ID
docker remove my-mongo-container