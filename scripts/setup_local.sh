#!/usr/bin/env bash
set -e

NAME=${1?"Usage: $0 NAME"}

if [ ${CIRCLECI} ]; then
    echo "running on circle ci";
    DIP=neo4j

else
    echo "running locally";
    DIP=localhost

    nc -z ${DIP} 7687 && {
        echo "neo4j port already in use";
        $( dirname "$0" )/kill_neo.sh ${NAME};
    }

    docker run -d --name ${NAME} --publish=7474:7474 --publish=7687:7687 --env=NEO4J_AUTH=none neo4j:3.5

    until $(nc -z ${DIP} 7687)
    do
        echo "Waiting..."
        sleep 1
    done

    i=1
    sp="/-\|"
    until $(curl -s -I http://localhost:7474 | grep -q "200 OK")
    do
        printf "\b${sp:i++%${#sp}:1}"
        sleep 1
    done

    printf "\rStarted!\n"
fi
