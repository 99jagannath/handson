import heapq

arr =[1, 2, 3, 4, 5, 6]

heapq.heapify(arr)
heapq.heappush(arr, 7)

print(heapq.heappop(arr))
print(len(arr))

print(heapq.heappushpop(arr, 13))
print(heapq.heapreplace(arr, 15))
print(heapq.nlargest(3, arr))
print(heapq.nsmallest(3, arr))

arr2 = [(1,4), (2,3), (3,2), (4,1)]

heapq.heapify(arr2)
print(heapq.nlargest(len(arr), arr2))
print(heapq.nlargest(len(arr), arr2, key= lambda x : x[1]))