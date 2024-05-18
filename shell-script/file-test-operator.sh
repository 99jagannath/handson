#! /bin/bash

echo -e "Enter the name of the file : \C"
read file_name

if [ -f $file_name ]; then
    echo "File exist"
    if [ -w $file_name ]; then 
        echo "Type some data. To quit press Ctrl+D"
        cat >> $file_name
    else
        echo "File has not write permission"
    fi    
else
    echo "File doesn't exist"
fi
# -d for checking dirs
# -r for readble file or not
# -w for  writable file or not
# -s empty or not
# -b blob specified file
# -c char based file