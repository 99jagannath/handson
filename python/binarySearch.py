
def binary_search(arr, l, r, k):
    
    while l <= r:
        m = l + (r-l) // 2
        if arr[m] < k:
            l = m + 1
        else:
            r = m - 1

    print(l,r)

def bisect_left(arr, l, r, k):

    bs_left = -1
    while l <= r:
        m = l + (r - l) // 2
        if arr[m] >= k:
            bs_left = m
            r = m - 1
        else:
            l = m + 1
    return bs_left

def bisect_right(arr, l, r, k):
    bs_right = -1
    while l <= r:
        m = l + (r - l) // 2
        if arr[m] > k:
            bs_right = m
            r = m - 1
        else:
            l = m + 1
    return bs_right


arr = [1,3,4,5,6,6,6,7,7,8,9]


print(bisect_right(arr, 0, len(arr)-1, 5))