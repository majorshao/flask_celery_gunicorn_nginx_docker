#!/bin/bash

echo "killing existing docker processes"
docker-compose rm -fs

echo "building docker containers"
docker-compose up --build -d
