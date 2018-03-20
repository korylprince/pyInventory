#!/bin/bash

version=$1

docker build --no-cache --build-arg "VERSION=$version" --tag "korylprince/pyinventory:$version" .

docker push "korylprince/pyinventory:$version"
