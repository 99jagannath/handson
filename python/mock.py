def  prevPermuation(arr, n):
	left = n - 1
	while left > 0 and arr[left -1] <= arr[left]:
		left  = left - 1

	if  left == 0:
		return -1
	culpritIndx = left -1
	pivitIndex  = -1
	dif = 1000
	while left < n:
		if arr[left] < arr[culpritIndx ]:
			if dif > abs( arr[left] - arr[culpritIndx ]):
				dif  =  abs( arr[left] - arr[culpritIndx ])
				pivitIndex = left
		left += 1
	arr[culpritIndx], arr[pivitIndex ] = arr[pivitIndex ], arr[culpritIndx]
	arr[culpritIndx+1:] = reversed(arr[culpritIndx+1:] )

arr = [2,1,3,4,5]
prevPermuation(arr, 5)
print(arr)

