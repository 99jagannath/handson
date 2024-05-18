#! /bin/python
num1=10
num2=5
num3=10.5

echo $(( num1 + num2 ))
echo $(expr $num1 + $num2 )
# but for multiplication
data=$(expr $num1 \* $num2 )
echo $data

echo "$num2+$num3" | bc
echo "scale=20:$num3/$num2" | bc
echo "scale=20:sqrt($num3)" | bc -l