from collections import defaultdict


d = defaultdict(list)

for i in range(4):
    d[i].append(i)

print(d)