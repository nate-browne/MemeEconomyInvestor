#!/bin/bash
# This script gets run once a day to move all of the log files to a nice directory for inspection

day=`date | awk '{print $2, $3, $6}'`
#day=`date +'%d %b %Y'`
mkdir "~/$day-logs"

mv ~/MemeEconomyInvestor/*.out ~/$day-logs
