class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()

    def peek(self):
        if not self.is_empty():
            return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

def reverse_stack(stack):
    aux_stack = Stack()

    while not stack.is_empty():
        temp = stack.pop()
        aux_stack.push(temp)

    # Copy elements from aux_stack back to the original stack to reverse it
    while not aux_stack.is_empty():
        temp = aux_stack.pop()
        stack.push(temp)

# Example usage:
original_stack = Stack()
original_stack.push(1)
original_stack.push(2)
original_stack.push(3)
original_stack.push(4)

print("Original Stack:", original_stack.items)

reverse_stack(original_stack)

print("Reversed Stack:", original_stack.items)
