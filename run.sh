#!/bin/bash

if [  "$1" == "build" ];
then

  docker build . -t discord-bot
fi

if [ "$1" == "run" ];
then

  docker run discord-bot -v ./:/app 

fi




