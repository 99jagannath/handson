from os import *
from sys import *
from collections import *
from math import *

class Node:
    
    def __init__(self):
        self.children = [None] * 26
        self.prefixCount = 0
        self.endCount = 0

    def isChildExist(self, ch):
        self.children[ord(ch) - ord('a')] != None

    def getChild(self, ch):
        return self.children[ord(ch) - ord('a')]

    def setChild(self, ch, node):
        self.children[ord(ch) - ord('a')] = node

    def incPrefixCounter(self):
        self.prefixCount += 1

    def incEndCounter(self):
        self.endCount += 1

    def decPrefixCounter(self):
        self.prefixCount -= 1

    def decEndCounter(self):
        self.endCount -= 1

    def getPrefixCounter(self):
        return self.prefixCount

    def getEndCounter(self):
        return self.endCount

class Trie:
    def __init__(self):
        # Write your code here.
        self.root = Node()

    def insert(self, word):
        # Write your code here.
        node = self.root
        for ch in word:
            if not node.isChildExist(ch):
                newNode = Node()
                node.setChild(ch, newNode)
            node = node.getChild(ch)
            node.incPrefixCounter()
        
        node.incEndCounter()
        print(node.getEndCounter())


    def countWordsEqualTo(self, word):
        node = self.root
        for ch in word:
            if not node.isChildExist(ch):
                return 0
            node = node.getChild(ch)
        return node.getEndCounter()

    def countWordsStartingWith(self, word):
        node = self.root
        for ch in word:
            if not node.isChildExist(ch):
                return 0
            node = node.getChild(ch)
        return node.getPrefixCounter()

    def erase(self, word):
        node = self.root
        for ch in word:
            if not node.isChildExist(ch):
                return
            node = node.getChild(ch)
            node.decPrefixCounter()
        node.decEndCounter()

t = Trie()

t.insert('apple')
t.insert('apple')
print (t.countWordsEqualTo("apple"))
