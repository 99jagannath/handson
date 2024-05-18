
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def isLeaf(root):
    return not root.left and not root.right

def addLeftBoundary(root, res):
    cur = root.left
    while cur:
        if not isLeaf(cur):
            res.append(cur.data)
        if cur.left:
            cur = cur.left
        else:
            cur = cur.right

def addRightBoundary(root, res):
    cur = root.right
    tmp = []
    while cur:
        if not isLeaf(cur):
            tmp.append(cur.data)
        if cur.right:
            cur = cur.right
        else:
            cur = cur.left
    for i in range(len(tmp) - 1, -1, -1):
        res.append(tmp[i])

def addLeaves(root, res):
    if isLeaf(root):
        res.append(root.data)
        return
    if root.left:
        addLeaves(root.left, res)
    if root.right:
        addLeaves(root.right, res)

def printBoundary(root):
    res = []
    if not root:
        return res

    if not isLeaf(root):
        res.append(root.data)

    addLeftBoundary(root, res)
    addLeaves(root, res)
    addRightBoundary(root, res)
    return res

def main():
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.left.left = TreeNode(3)
    root.left.left.left = TreeNode(4)
    root.left.left.right = TreeNode(5)
    root.left.left.left.left = TreeNode(6)
    root.left.left.left.right = TreeNode(7)
    root.left.left.right.left = TreeNode(8)
    root.left.left.right.right = TreeNode(9)

    boundaryTraversal = printBoundary(root)

    print("The Boundary Traversal is:", boundaryTraversal)

if __name__ == "__main__":
    main()
