#!/bin/bash

manual="false"

while getopts ":m" arg $@; do
  case $arg in
    m) manual="true";;
   \?) echo "Invalid flag"; exit 1;;
  esac
done

if [ $manual == "true" ]; then
  echo -n "Enter a file to use (check the files directory): "
  read option

  echo -n "run in the background (Y/n)? "
  read bg

  if [ $bg == "Y" ]; then
    python bin/final.py -f files/$option &
  else
    python bin/final.py -f files/$option
  fi
else
  nohup python bin/final.py -f files/bots.tsv &
fi
