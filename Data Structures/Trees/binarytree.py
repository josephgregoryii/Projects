import sys
import random
class BinaryTree:
    class TreeError(Exception):
        def __init__(self,data = None):
            super().__init__(data)
    class Node:
        def __init__(self, key=None):
            self.key = key
            self.parent = None
            self.child = None
            self.right = None
            self.left = None

    def __init__(self):
        self.root = None
        self.size = 0

    def treeMinimum(self,x):
        if x == None:
            raise BinaryTree.TreeError("Empty")
        while x.left != None:
            x = x.left
        return x.key

    def treeMaximum(self,x):
        if x == None:
            raise BinaryTree.TreeError("Empty")
        while x.right != None:
            x = x.right
        return x.key

    def treeSuccessor(self,x):
        if x.right != None:
            return treeMinimum(x.right)
        y = x.parent
        while y != None and x == y.right:
            x = y
            y = y.parent
        return y

    def search(self,x,k):
        return self.treeSearch(x,k)

    def treeSearch(self,x,k):
        if x == None or k == x.key:
            return x
        if k < x.key:
            return self.treeSearch(x.left,k)
        else:
            return self.treeSearch(x.right,k)

    def insert(self,x):
        node = BinaryTree.Node(x)
        y = None
        root = self.root
        while root != None:
            y = root
            if node.key < root.key:
                root = root.left
            else:
                root = root.right
        node.parent = y
        if y == None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node

    def transplant(self,u,v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v != None:
            v.parent = u.parent

    def treeDelete(self,x):
        z = self.treeSearch(self.root,x)
        if z.left == None:
            self.transplant(z,z.right)
        elif z.right == None:
            self.transplant(z,z.left)
        else:
            y = self.treeMinimum(z.right)
            if y.parent != z:
                transplant(y,y.right)
                y.right = z.right
                y.right.parent = y
            self.transplant(z,y)
            y.left = z.left
            y.left.parent = y

    def to_list_preorder(self,x):
        result = []
        if x != None:
            result.append(str(x.key))
            result += self.to_list_preorder(x.left)
            result += self.to_list_preorder(x.right)
        return result

    def to_list_inorder(self,x):#takes in argument x to start at the root
        result = []
        if x != None:
            result += self.to_list_inorder(x.left)
            result.append(str(x.key))
            result += self.to_list_inorder(x.right)
        return result

    def to_list_postorder(self,x):  #takes in argument x to start at the root
        result = []
        if x != None:
            result += self.to_list_postorder(x.left)
            result += self.to_list_postorder(x.right)
            result.append(str(x.key))
        return result

    def remove(self,x):
        if self.root == None:
            raise BinaryTree.TreeError("Empty Tree")
        self.treeDelete(x)

def driver():
    tree = BinaryTree()
    with open(sys.argv[1]) as f:
        n = int(f.readline().strip())
        for _ in range(n):
            in_data = f.readline().strip().split()
            action, value = in_data[0], in_data[1:]
            if action.lower() == "insert":
                tree.insert(int(value[0]))
            elif action.lower() == "remove":
                try:
                    tree.remove(int(value[0]))
                except BinaryTree.TreeError:
                    print("TreeError")
            elif action.lower() == "search":
                result = tree.search(tree.root,int(value[0]))
                if result:
                    print("Found")
                else:
                    print("NotFound")
            elif action.lower() == "max":
                try:
                    print(tree.treeMaximum(tree.root))
                except BinaryTree.TreeError:
                    print("Empty")
            elif action.lower() == "min":
                try:
                    print(tree.treeMinimum(tree.root))
                except BinaryTree.TreeError:
                    print("Empty")
            elif action.lower() == "preprint":
                result = tree.to_list_preorder(tree.root)
                if tree.root == None:
                    print("Empty")
                else:
                    print(' '.join(result))
            elif action.lower() == "inprint":
                result = tree.to_list_inorder(tree.root)
                if tree.root == None:
                    print("Empty")
                else:
                    print(' '.join(result))
            elif action.lower() == "postprint":
               result = tree.to_list_postorder(tree.root)
               if tree.root == None:
                   print("Empty")
               else:
                   print(' '.join(result))

if __name__ == "__main__":
    driver()
