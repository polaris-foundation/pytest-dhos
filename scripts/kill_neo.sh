#!/usr/bin/env bash
set -e

NAME=${1?"Usage: $0 NAME"}

if [ -z ${CIRCLECI} ]; then
    docker kill /${NAME}
    docker rm /${NAME}
fi
