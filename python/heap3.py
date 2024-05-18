import math

class heap:

    def __init__(self) -> None:
        self.arr = []
        self.size = 0

    def __heapify_down(self, ind, size):
        max_ind = ind
        left = 2*ind + 1
        right = 2*ind + 2

        if left < size and self.arr[left] > self.arr[max_ind]:
                max_ind = left

        if right < size and self.arr[right] > self.arr[max_ind]:
                max_ind = right

        if max_ind != ind:
            self.arr[ind], self.arr[max_ind] = self.arr[max_ind], self.arr[ind]
            self.__heapify_down(max_ind, max_ind)

    def __heapify_up(self, ind):
        if ind <= 0:
             return
        parent = math.floor((ind-1)/2)
        if parent >= 0:
             if self.arr[parent] < self.arr[ind]:
                  self.arr[parent], self.arr[ind] = self.arr[ind], self.arr[parent]
                  self.__heapify_up(parent)
             
    def heap_sort(self):
        size = len(self.arr)
        for i in range(size-1, -1, -1):
             self.arr[0], self.arr[i] = self.arr[i], self.arr[0]
             self.__heapify_down(0, i)
         
