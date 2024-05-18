#! /bin/bash

while getopts d:p:a:n:c:s:u:b:emrh flag; do
  case $flag in
    d)
      echo $flag
      ;;
    p)
      echo $flag
      ;;
    a)
      echo $flag
      ;;
    n)
      echo $flag
      ;;
    c)
      echo $flag
      ;;
    s)
      echo $flag
      ;;
    u)
      echo $flag
      ;;
    b)
      echo $flag
      ;;
    e)
      echo $flag
      ;;
    m)
      echo $flag
      ;;
    r)
      echo $flag
      ;;
    h)
      echo $flag
      exit
      ;;
    *)
      echo "Should not occur"
      ;;
  esac
done