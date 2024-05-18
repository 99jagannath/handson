#! /bin/bash

# THis is a comment
echo "Hello World!" # this is also a comment
echo $BASH
echo $HOME
echo $PWD
# variable name should not start with number
name=Jaga # space is not allowed in the local variables declaration
title=kanhu
echo The name is $name
name+=" ${title}"
echo $name