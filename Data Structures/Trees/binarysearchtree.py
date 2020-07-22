from sys import argv

class Stack:
    class Underflow(Exception):
        def __init__(self, data=None):
            super().__init__(data)

    class Node:
        def __init__(self, data=None):
            self.data = data
            self.next = None

    def __init__(self):
        self.head = None
        self.size = 0

    def push(self, x: "datum") -> None:
        n = Node(x)
        n.next = self.head
        self.head = n
        self.size += 1

    def pop(self) -> "datum":
        if self.head == None:
            raise Stack.Underflow("Stack.pop() invoked on empty stack")
        n = self.head
        self.head = n.next
        self.size -= 1
        return n.data

    def is_empty(self) -> bool:
        if self.head == None:
            return True
        else:
            return False

    def __len__(self):
        return self.size

class Node:
    def __init__(self,x: "comparable", other = None):
        self.key = x
        self.other = other
        self.left = None
        self.right = None
        self.parent = None

class BinarySearchTree:
    class EmptyTree(Exception):
        def __init__(self,data=None):
            super().__init__(data)

    class NotFound(Exception):
        def __init__(self,data=None):
            super().__init__(data)

    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, key: Node):
        z = Node(key)
        y = None
        x = self.root
        while x != None:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y == None:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        self.size += 1

    def search_iterative(self, x: Node, k: "comparable"):
        while x != None and k != x.key:
            if k < x.key:
                x = x.left
            else:
                x = x.right
        return x

    def search(self, x: Node, k: "comparable"):
        z = self.search_iterative(x,k)
        if z == None:
            raise BinarySearchTree.NotFound('search({}) not found'.format(k))
        return z

    def minimum(self, x: Node):
        if x == None:
            raise BinarySearchTree.EmptyTree('minimum() invoked on empty tree')
        while x.left != None:
            x = x.left
        return x

    def maximum(self, x: Node):
        if x == None:
            raise BinarySearchTree.EmptyTree('maximum() invoked on empty tree')
        while x.right != None:
            x = x.right
            return x

    def transplant(self, u: Node, v: None):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v != None:
            v.parent = u.parent

    def delete(self, x: Node):
        z = self.search(self.root, x.key)
        if z == None:
            raise BinarySearchTree.EmptyTree("TreeError")
        else:
            if z.left == None:
                self.transplant(z, z.right)
            elif z.right == None:
                self.transplant(z, z.left)
            else:
                y = self.minimum(z.right)
                if y.parent != z:
                    self.transplant(y, y.right)
                    y.right = z.right
                    y.right.parent = y
                self.transplant(z, y)
                y.left = z.left
                y.left.parent = y
            self.size -= 1

    def preorder_helper(self, n: Node, l: "list of keys"):
        if n != None:
            l.append(n.key)
            self.preorder_helper(n.left,l)
            self.preorder_helper(n.right,l)

    def to_list_preorder(self):
        l = []
        self.preorder_helper(self.root,l)
        return l

    def inorder_helper(self, n: Node, l: "list of keys"):
        if n != None:
            self.inorder_helper(n.left, l)
            l.append(n.key)
            self.inorder_helper(n.right, l)

    def to_list_inorder(self):
        l = []
        self.inorder_helper(self.root,l)
        return l

    def postorder_helper(self, n: Node, l):
        if n != None:
            self.postorder_helper(n.left, l)
            self.postorder_helper(n.right, l)
            l.append(n.key)

    def to_list_postorder(self):
        l = []
        self.postorder_helper(self.root, l)
        return l

    def printpath(self,path):
        result = ''
        for i in range(len(path)):
            v = path[i]
            result = result +' ' + str(v)
        print(result)

    def best_path_value(self):
        if self.size == 0:
            raise BinarySearchTree.EmptyTree("TreeError")
        root = self.root
        sums = []
        path = [0]
        sum = 0
        stack = [iter([root])]
        while stack:
            for node in stack[-1]:
                path.append(node.key)
                sum += str(node.key).count("5")
                children = [n for n in (node.left, node.right) if n]
                stack.append(iter(children))
                if not children:
                    sums.append(sum)
                break
            else:
                sum -= str(path.pop()).count("5")
                stack.pop()
        return max(sums)


def driver():
    st = BinarySearchTree()
    f = open(argv[1], "r")
    nl = int(f.readline().strip())
    for i in range(nl):
        l = f.readline().strip()
        v = l.split()
        if v[0] == 'insert':
            k = int(v[1])
            st.insert(k)
        elif v[0] == 'remove':
            k = int(v[1])
            try:
                z = st.search(st.root, k)
                st.delete(z)
            except BinarySearchTree.NotFound as e:
                print("TreeError")
        elif v[0] == 'bpv':
            try:
                print(st.best_path_value())
            except BinarySearchTree.EmptyTree as e:
                print("TreeError")

if __name__ == '__main__':
    driver()


