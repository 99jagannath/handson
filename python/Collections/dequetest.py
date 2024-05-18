from collections import deque

q = deque([1,2,3])

q.append(4)
q.appendleft(0)

print(q.pop())
print(q.popleft())

print(q)

q.rotate(2)
print(q)
q.rotate(-2)
print(q)


