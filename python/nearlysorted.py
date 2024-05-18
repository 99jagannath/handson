
def binarySearch(arr, l, r, x):
    if r < l:
         return -1
    m = l + (r-l) // 2
    if arr[m] == x:
        return m
    elif m > 0 and arr[m-1] == x:
        return m -1
    elif m < r and arr[m+1] == x:
        return m + 1
    elif arr[m] < x:
         return binarySearch(arr, m+2, r, x )
    else:
         return binarySearch(arr, l, m-2, x)
    
		

	


# Driver Code
arr = [3, 2, 10, 4, 40]
n = len(arr)
x = 4
result = binarySearch(arr, 0, n - 1, x)
if (result == -1):
	print("Element is not present in array")
else:
	print("Element is present at index", result)

# This code is contributed by Smitha Dinesh Semwal.
