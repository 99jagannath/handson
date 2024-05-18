from collections import Counter


cntr = Counter([1,2,2,2,3,4])
for key, val in cntr.items():
    print(key, val)

print(list(dict(cntr)))