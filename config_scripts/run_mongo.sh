#!/bin/bash
docker run -d --name my-mongo-container -e MONGO_INITDB_ROOT_USERNAME=test -e MONGO_INITDB_ROOT_PASSWORD=mongodb -p 27017:27017 mongo
