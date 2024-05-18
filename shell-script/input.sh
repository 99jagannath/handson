#! /bin/bash

echo "enter  names"
read name1 name2 name3

echo "names $name1, $name2, $name3"

# Taking input in the same line

read -p 'username : ' user_var
read -sp 'password : ' pass_var
echo
echo "username : $username"
echo "passwprd : $password"

# Taking input as array
echo "Enter names "
read -a names
echo "Names : ${names[0]}, ${names[1]}"

# the default variable is reply
read

echo "Name : $REPLY"