#/bin/bash

log_dir="./logs/nginx"

if [ ! -d "$log_dir" ]; then
  echo "not exist"
  mkdir -p $log_dir
fi