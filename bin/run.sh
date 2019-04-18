#!/bin/bash

manual="false"

while getopts ":m" arg $@; do
  case $arg in
    m) manual="true";;
   \?) echo "Invalid flag"; exit 1;;
  esac
done

# get rid of all of the parsed sections
shift $((OPTIND - 1))

if [ $manual == "true" ]; then
  echo -n "Enter a file to use (check the files directory): "
  read option

  echo -n "run in the background (Y/n)? "
  read bg

  if [ $bg == "Y" ]; then
    python ~/MemeEconomyInvestor/bin/final.py -f ~/MemeEconomyInvestor/files/$option --no-logging &
  else
    python ~/MemeEconomyInvestor/bin/final.py -f ~/MemeEconomyInvestor/files/$option --no-logging
  fi
else
  python ~/MemeEconomyInvestor/bin/final.py -f ~/MemeEconomyInvestor/files/bots0.tsv $1 &
fi
