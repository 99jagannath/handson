
import sys
def selection_sort(arr):
    left, right = 0, len(arr) -1

    while left < right:
        mn = sys.maxsize
        mni= left
        for i in range(left, right+1):
            if arr[i] < mn:
                mn = arr[i]
                mni = i
        if mni != left:
            arr[mni], arr[left] = arr[left], arr[mni]
        left += 1

    return arr

def bubble_sort(arr):
    left, right = 0, len(arr) -1

    while left < right:
        for i in range(left, right):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
        right -= 1
    return arr

def insertion_sort(arr):
    left, right = 1, len(arr) -1
    
    while left <= right:
        for i in range(left, 0, -1):
            if arr[i] < arr[i - 1]:
                arr[i], arr[i -1] = arr[i - 1], arr[i]
            else:
                break
        left += 1
    return arr

def merge_sort_utils(arr, l, r):
    if l == r:
        return arr
    m = l + (r-l) //2

    left_arr = merge_sort_utils(arr[l:m+1], l, m)
    right_arr = merge_sort_utils(arr[m+1:r+1], m+1, r)

    a, b, i = 0, 0, 0
    while a < len(left_arr) and b < len(right_arr):
        if left_arr[a] < right_arr[b]:
            arr[i] = left_arr[a]
            a += 1
        else:
            arr[i] = right_arr[b]
            b += 1
        i += 1

    while a < len(left_arr):
        arr[i] = left_arr[a]
        a += 1
        i += 1

    while b < len(right_arr):
        arr[i] = right_arr[b]
        b += 1
        i += 1

    return arr


def merge_sort(arr):
    l, r = 0, len(arr) - 1
    return merge_sort_utils(arr, l, r)

def getPivot(arr, l, r):
    pivot = arr[l]

    i, j = l, r
    while i < j:
        while i < r and arr[i] <= pivot:
            i += 1

        while j > l and arr[j] >= pivot:
            j -= 1

        if i < j:
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[l], arr[j] = arr[j], arr[l]
    return j


def quick_sort_utils(arr, l, r):
    if l < r:
        p = getPivot(arr, l, r)
        quick_sort_utils(arr, l , p- 1)
        quick_sort_utils(arr, p + 1, r)
    return arr

def quick_sort(arr):
    l, r= 0, len(arr) -1
    return quick_sort_utils(arr, l, r)


print(quick_sort([3,2,4,7, 5, 6,7]))
