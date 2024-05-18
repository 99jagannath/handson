

def binary_search(arr, l , r):
    while l<= r:
        m = l + (r - l) // 2
        ind = -1
        if arr[m] == 1:
            ind = m
            r = m -1
        else:
            l = m + 1

    return ind


def find1stoccurance(arr):
    l , r = 0, 1

    while arr[r] != 1:
        temp = r
        r += (r - l + 1)
        l = temp

    return binary_search(arr, l, r)

arr = [1,1,1,1,1,1,1,1,1,1,1]

def min_dif(arr, k):
    l, r = 0, len(arr) - 1
    while l <= r:
        m = l + (r - l) // 2
        if arr[m] == k:
            return 0
        elif arr[m] > k:
            r = m -1
        else:
            l = m + 1
    if l == 0:
        return arr[l] - k
    else:
        return min(arr[l] - k, k - arr[l -1])
    
def peak_in_bitonic(arr):
    l, r = 0, len(arr) - 1
    while l <= r:
        m = l + (r - l) // 2
        print(l, m, r)
        if m == 0 and arr[m] > arr[m + 1]:
            return arr[m]
        elif m == (len(arr) - 1) and arr[m] > arr[m - 1]:
            return arr[m]
        elif arr[m] > arr[m - 1] and arr[m] > arr[m + 1]:
            return arr[m]
        elif arr[m] < arr[m + 1]:
            l = m + 1
        else:
            r = m - 1
    return -1 
    
print(peak_in_bitonic([1,2,3,4]))
    
print(min_dif([1,2,3,4,5,7,9], 7))

def search_in_biotonic(arr, k):
    l, r = 0, len(arr) -1

    while l <= r:
        m = l + (r - l) // 2
        if arr[m] == k:
            return m





def a(arr):
    #arr = [1,2,3]
    arr[0] = 9
    return arr

def c(arr):
    arr.append(5)
    return arr

def b():
    arr =[0,0]
    print(a(arr))
    print(arr)
    print(c(arr))
    print(arr)
    

# b()

arr =[0,0]
print(a(arr))
print(arr)
print(c(arr))
print(arr)


def set_list(lt):
	lt = ["A", "B", "C"]
	return lt

def add(list):
	list.append("D")
	return list

my_list = ["E"]

print(set_list(my_list))
print(my_list)

print(add(my_list))
print(my_list)


ls = (23,)
print(type(ls))
        

suffix = ("ed", "ing")
word = "jfdhjdhed"

if  word.endswith(suffix):
    print("ends with")

print(print(3))

    