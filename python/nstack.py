from os import *
from sys import *
from collections import *
from math import *

class NStack:
    def __init__(self, n, s):
        # Write your code here
        self.arr = [-1] * s
        self.top = [-1] * n
        self.next = [-1] * s
        for i in range(0, s-1):
            self.next[i] = i + 1
        self.freeInd = 0


    # Pushes 'X' into the Mth stack. Returns true if it gets pushed into the stack, and false otherwise.
    def push(self, x, m):
        # Write your code here
        if self.freeInd == -1:
            return False

        index = self.freeInd
        self.freeInd = self.next[index]
        self.next[index] = self.top[m-1]
        self.top[m-1] = index
        self.arr[index] = x
        return True


    # Pops top element from Mth Stack. Returns -1 if the stack is empty, otherwise returns the popped element.
    def pop(self, m):
        # Write your code here
        if self.top[m-1] == -1:
            return -1

        index = self.top[m-1]
        self.top[m-1] = self.next[index]
        self.next[index] = self.freeInd
        self.freeInd = index
        return self.arr[index]

stack = NStack(3,6)
print( stack.next, stack.top, stack.freeInd)
stack.push(9,1)
print(stack.next, stack.top, stack.freeInd)
stack.push(8,1)
print(stack.next, stack.top, stack.freeInd)

stack.pop(1)

print(stack.next, stack.top, stack.freeInd)
stack.push(6,1)
print(stack.next, stack.top, stack.freeInd)
stack.push(3,2)
print(stack.next, stack.top, stack.freeInd)
stack.push(7,2)
print(stack.next, stack.top, stack.freeInd)
stack.pop(2)
print(stack.next, stack.top, stack.freeInd)

