#!/bin/bash
while getopts "a:b:c:efg" flag;do
    echo "flag -$flag, Argument $OPTARG";
done