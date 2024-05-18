#! /bin/bash

flag="jaga"

case $flag in 
    "jaga")
        echo "jaga"
        ;;
    "kanhu")
        echo "kanhu"
        ;;
    *)
        echo "invalid"
        exit 1
        ;;
esac