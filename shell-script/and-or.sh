#! /bin/bash

age=10

if [ $age -gt 5 ] && [ $age -lt 15 ]; then
    echo "valid age"
fi
# For or ||
if [ $age -gt 5 -a $age -lt 15 ]; then
    echo "valid age"
fi
# For or -o
if [[ $age -gt 5 && $age -lt 15 ]]; then
    echo "valid age"
fi
# For or ||