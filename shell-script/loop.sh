#!/bin/bash

n=1

# while [ $n -le 10 ]; do
while (( $n <= 10 )); do
    echo -n $n
    (( ++n ))
    # n=`expr $n + 1`
    # n=$(( n+1 ))
    sleep 1
    done