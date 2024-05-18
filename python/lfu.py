from abc import ABC, abstractclassmethod

class Node:

    def __init__(self, key, val, fre=1, Prev=None, Next=None) -> None:
        self.key = key
        self.val = val
        self.fre = fre
        self.prev = Prev
        self.next = Next


class ListClass:

    def __init__(self):
        self.head = Node(1,1)
        self.tail = Node(1, 1)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def add_front(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def remove_node(self, node):
        if self.size == 0:
            return
        
        node.next.prev = node.prev
        node.prev.next = node.next
        self.size -= 1

    def remove_from_end(self):
        self.remove_node(self.tail.prev)
        
class eviction_strategy(ABC):

    @abstractclassmethod
    def update_list(self):
        pass

    @abstractclassmethod
    def get(self):
        pass

    @abstractclassmethod
    def put(self):
        pass


class LFU_strategy:

    def __init__(self, max_size) -> None:
        self.fre_list = {}
        self.min_fre = 0
        self.max_size = max_size
        self.cur_size = 0
        self.storage = {}

    def update_list(self, node):
        cur_fre = node.fre + 1
        node_list = self.fre_list[node.fre]
        node_list.remove_node(node)
        if node_list.size == 0:
            del self.fre_list[node.fre]
        if node.fre == self.min_fre:
            self.min_fre += 1
        node.fre = cur_fre
        if node.fre not in self.fre_list:
            self.fre_list[node.fre] = ListClass()
        self.fre_list[node.fre].add_front(node)

    def get(self, key):
        if key not in self.storage:
            return -1
        node = self.storage[key]
        self.update_list(node)
        return self.storage[key].val

    def put(self, key, val):
        if key in self.storage:
            node = self.storage[key]
            node.val = val
            self.update_list(node)
        else:
            if self.cur_size == self.max_size:
                node = self.fre_list[self.min_fre].tail.prev
                self.fre_list[self.min_fre].remove_from_end()
                del self.storage[node.key]
                self.cur_size -= 1

            self.cur_size += 1
            node = Node(key, val)
            if self.min_fre not in self.fre_list: 
                self.min_fre = 1
                self.fre_list[self.min_fre] = ListClass()
            self.fre_list[self.min_fre].add_front(node)
            self.storage[key] = node


class eviction_factory:

    def get_eviction_strategy(eviction_policy, max_size):
        if eviction_policy == "LFU":
            return LFU_strategy(max_size)

class Cache:

    def __init__(self, eviction_policy, max_size) -> None:
        
        self.eviction_strategy = eviction_factory.get_eviction_strategy(eviction_policy, max_size)

    def get(self, key):
        return self.eviction_strategy.get(key)
    
    def put(self, key, val):
        self.eviction_strategy.put(key, val)


def main():
    cache = Cache("LFU", 2)
    cache.put(1, 1)
    cache.put(2, 3)
    cache.put(1, 2)
    cache.put(3, 1)
    print(cache.get(1))
    print(cache.get(2))

if __name__ in ['main', '__main__']:
    main()

    
    
