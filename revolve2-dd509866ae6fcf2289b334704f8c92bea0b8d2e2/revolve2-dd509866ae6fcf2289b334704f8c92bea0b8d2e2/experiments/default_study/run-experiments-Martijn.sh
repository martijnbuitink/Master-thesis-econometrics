#!/bin/bash

study="default_study"
mainpath="/storage/mbuitink"

if ! [ -d ${mainpath}/${study} ]; then
  # Take action if $DIR exists. #
  echo "Installing config files in..."
  mkdir ${mainpath}/${study};
fi

#mkdir ${mainpath}/${study};
screen -d -m -S run_loop -L -Logfile ${mainpath}/${study}/setuploop.log ./experiments/${study}/setup-experiments-Martijn.sh;