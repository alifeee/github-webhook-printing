#!/bin/bash
# do not much
log="/var/www/cgi/do/log"

echo "" >> $log
date >> $log
env >> $log
input=$(cat /dev/stdin)
echo "${input}" >> $log

echo "Content-Type: text/plain"

echo ""
echo ""

if [ -z $input ]; then
  echo "nothing :("
  exit 0
fi

echo "${input}" | jq
