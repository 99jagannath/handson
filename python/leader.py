def printLeaders(arr, n):

    mx = -1e9

    for i in range(n-1, -1, -1):
        if arr[i] > mx:
            print(arr[i])
            mx = arr[i]


printLeaders([1,2,4,7,0,2,1], 7)