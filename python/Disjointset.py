

class DisjointSet:

    def __init__(self, n) -> None:
        self.rank = [0] * (n+1)
        self.parent = [i for i in range(n+1)]

    def find_ultimate_parent(self, node):
        if self.parent[node] == node:
            return node
        
        self.parent[node] = self.find_ultimate_parent(self.parent[node])

        return self.parent[node]
    
    def unionByRank(self, u, v):
        p_u = self.find_ultimate_parent(u)
        p_v = self.find_ultimate_parent(v)

        if p_u == p_v:
            return

        if self.rank[u] > self.rank[v]:
            self.parent[p_v] = p_u

        elif self.rank[u] < self.rank[v]:
            self.parent[p_u] = p_v

        else:
            self.parent[p_v] = p_u
            self.rank[p_u] += 1

ds = DisjointSet(7)
ds.unionByRank(1, 2)
ds.unionByRank(2, 3)
ds.unionByRank(4, 5)
ds.unionByRank(6, 7)
ds.unionByRank(5, 6)

if ds.find_ultimate_parent(3) == ds.find_ultimate_parent(7):
    print("Same component")
else:
    print("not a component")

ds.unionByRank(3, 7)

if ds.find_ultimate_parent(3) == ds.find_ultimate_parent(7):
    print("Same component")
else:
    print("not a component")