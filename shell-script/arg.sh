#! /bin/bash

# Here Zero points to file name
echo $0 $1 $2

args=("$@")
#here zero poin to 1st argument
echo ${args[0]} ${args[1]} 
# print the array
echo $@
# print the number of args
echo $#

shift # shift the arg to one place right now arg2 is arg1 , 0 will always be the file name
echo $0 $1 $2