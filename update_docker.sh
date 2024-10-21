#!/usr/bin/env bash

echo " Builing Docker"
docker-compose -f docker-compose.prod.yml build

echo 'START : shinwoohipo/sh-intranet-api:latest'
docker push shinwoohipo/sh-intranet-api:latest
echo 'END : shinwoohipo/sh-intranet-api:latest'

echo 'START : shinwoohipo/sh-intranet-ws:latest'
docker push shinwoohipo/sh-intranet-ws:latest
echo 'END : shinwoohipo/sh-intranet-ws:latest'

echo 'START : shinwoohipo/sh-intranet-web:latest'
docker push shinwoohipo/sh-intranet-web:latest
echo 'END : shinwoohipo/sh-intranet-web:latest'
