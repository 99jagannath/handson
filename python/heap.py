import math

class MaxHeap:
    def __init__(self, data=[]):
        self.arr = data
    
    def getHeapSize(self):
        return len(self.arr)
    
    def _heapifyDown(self, ind, size):

        left = 2 * ind + 1
        right = 2 * ind + 2
        maxInd = ind
        if left < size and self.arr[left] > self.arr[maxInd]:
            maxInd = left

        if right < size and self.arr[right] > self.arr[maxInd]:
            maxInd = right

        if maxInd != ind:
            self.arr[maxInd], self.arr[ind] = self.arr[ind], self.arr[maxInd]
            self._heapifyDown(maxInd, size)

    def _heapifyUp(self, ind):
        if ind <= 0:
            return
        parent_index = (int)(math.floor((float)((ind - 1)/2)))

        if parent_index >= 0 and self.arr[parent_index] < self.arr[ind]:
            self.arr[parent_index], self.arr[ind] = self.arr[ind], self.arr[parent_index]
            self._heapifyUp(parent_index)

    
    def buildHeap(self):
        size = self.getHeapSize()
        startIndex = size // 2 - 1

        for i in range(startIndex, -1, -1):
            self._heapifyDown(i, size)

    def printHeap(self):
        print(self.arr)

    def getMax(self):
        size = self.getHeapSize()
        if size > 0:
            return self.arr[0]
        else:
            return -1
        
    def popMax(self):
        maxNum = self.getMax()
        if maxNum != -1:
            size = self.getHeapSize()
            self.arr[0], self.arr[size - 1] = self.arr[size - 1], self.arr[0]
            self.arr.pop()
            newSize = self.getHeapSize()
            if newSize > 0:
                self._heapifyDown(0, newSize)
            return maxNum
        else:
            return -1
        
    def insertNum(self, num):
        self.arr.append(num)
        size = self.getHeapSize()
        self._heapifyUp(size - 1)

    def updateNum(self, key, val):
        size = self.getHeapSize()
        if key >= size:
            return -1
        
        if self.arr[key] > val:
            self.arr[key] = val
            self._heapifyDown(key, size)
        else:
            self.arr[key] = val
            self._heapifyUp(key)

    def heapSort(self):

        size = self.getHeapSize()
        for i in range(size - 1, -1, -1):
            self.arr[i], self.arr[0] = self.arr[0], self.arr[i]
            self._heapifyDown(0, i)

        


heap = MaxHeap([0,1,2,3,4,5])

heap.buildHeap()
heap.printHeap()
print(heap.getMax())
# print(heap.popMax())
# print(heap.getMax())
# heap.printHeap()
# while True:
#     maxNum = heap.popMax()
#     if maxNum == -1:
#         break
#     print(maxNum)

heap.insertNum(6)
heap.printHeap()
# print(heap.getMax())
heap.updateNum(3, -2)
# heap.printHeap()
# while True:
#     maxNum = heap.popMax()
#     if maxNum == -1:
#         break
#     print(maxNum)
    
heap.heapSort()
heap.printHeap()

