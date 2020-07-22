import sys

class Leaf:

    def __init__(self):
        self.red = False
        self.parent = None

    def __bool__(self):
        return False

class RedBlackNode:


    def __init__(self,key):
        self.key = key
        self.red = True
        self.right = Leaf()
        self.left = Leaf()
        self.parent = None
        self.right.parent = self
        self.left.parent = self

    def __bool__(self):
        return True

    def __str__(self):
        return str(self.key)

class RedBlackTree:
    class EmptyTree(Exception):
        def __init__(self, data=None):
            super().__init__(data)

    def __init__(self):
        self.root = Leaf()

    def left_rotate(self,move):
        other = move.right
        move.right = other.left
        if other.left:
            other.left.parent = move
        other.parent = move.parent
        if not move.parent:
            self.root = other
        elif move == move.parent.right:
            move.parent.right = other
        else:
            move.parent.left = other
        other.left = move
        move.parent = other
        move.red = True
        other.red = False
        return other

    def right_rotate(self,move):
        other = move.left
        move.left = other.right
        if other.right:
            other.right.parent = move
        other.parent = move.parent
        if not move.parent:
            self.root = other
        elif move == move.parent.right:
            move.parent.right = other
        else:
            move.parent.left = other
        other.right = move
        move.parent = other
        move.red = True
        other.red = False
        return other

    def transplant(self,u,v):
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
            v.parent = u.parent

    def search(self,x):
        root = self.root
        while root and x != root.key:
            if x > root.key:
                root = root.right
            else:
                root = root.left
        return bool(root)

    def max(self):
        if not self.root:
            raise RedBlackTree.EmptyTree("TreeError")
        root = self.root
        while root.right:
            root = root.right
        return str(root.key)

    def min(self):
        if not self.root:
            raise RedBlackTree.EmptyTree("TreeError")
        root = self.root
        while root.left:
            root = root.left
        return str(root.key)

    def in_order(self,node):
        result = []
        if node != None:
            self.in_order(node.left)
            result.append(str(node.key))
            elf.in_order(node.right)
        return result

    def inprint(self, node, result):
        if not self.root:
            raise RedBlackTree.EmptyTree
        elif node:
            self.inprint(node.left, result)
            result.append(str(node.key))
            self.inprint(node.right,result)
        return result

    def insert(self, k):
        node = self.root
        parent = None
        while node:
            parent = node
            if k < node.key:
                node = node.left
            else:
                node = node.right
        node_2 = RedBlackNode(key = k)
        node_2.parent = parent

        if not parent:
            self.root = node_2
            self.root.red = False
            return
        elif k < parent.key:
            parent.left = node_2
        else:
            parent.right = node_2

        node = node_2
        parent = node.parent

        while node != self.root and parent.red:
            grandparent = parent.parent
            if parent == grandparent.left:
                uncle = grandparent.right
                if uncle.red:
                    parent.red = False
                    uncled.red = False
                    gparent.red = True
                    node = grandparent
                    parent - node.parent
                else:
                    if node == parent.right:
                        node = parent
                        self.leftRotate(node)
                        parent = node.parent
                    grandparent = parent.parent
                    self.right_rotate(grandparent)
            else:
                uncle = grandparent.left
                if uncle.red:
                    parent.red = False
                    uncle.red = False
                    grandparent.red = True
                    node = grandparent
                    parent = node.parent
                else:
                    if node == parent.left:
                        node = parent
                        self.right_rotate(node)
                        parent = node.parent
                    grandparent = parent.parent
                    self.left_rotate(grandparent)
        self.root.red = False

    def fix_remove(self,k):
        while not k.red and k != self.root:
            if k != k.parent.left:
                sibling = k.parent.left
                if sibling.red:
                    sibling.red = False
                    k.parent.red = True
                    self.right_rotate(k.parent)
                    sibling = k.parent.left
                if not sibling.left.red:
                    sibling.right.red = False
                    sibling.red = True
                    self.left_rotate(sibling)
                    sibling = k.parent.left
                elif not sibling.right.red and not sibling.left.red:
                    sibling.red = True
                    k = k.parent
                sibling.red = k.parent.red
                k.parent.red = False
                sibling.left.red = False
                self.right_rotate(k.parent)
                k = self.root
            else:
                sibling = k.parent.right
                if sibling.red:
                    sibling.red = False
                    k.parent.red = True
                    self.left_rotate(k.parent)
                    sibling = k.parent.right
                if not sibling.right.red:
                    sibling.left.red = False
                    sibling.red = True
                    self.right_rotate(sibling)
                    sibling = k.parent.right
                elif not sibling.right.red and not sibling.left.red:
                    sibling.red = True
                    k = k.parent
                sibling.red = k.parent.red
                k.parent.red = False
                sibling.right.red = False
                self.left_rotate(k.parent)
                k = self.root
        k.red = False
        return k

    def remove(self,k):
        if not self.root:
            raise RedBlackTree.EmptyTree("TreeError")
        while self.root:
            if k == self.root.key:
                k = self.root
                break
            elif k < self.root.key:
                node = self.root.left
            elif k > self.root.key:
                node = self.root.right

        k2 = k
        k2_c = k2.red

        if not k.right:
            k3 = k.left
            self.transplant(k,k.left)
        if not k.left:
            k3 = k.right
            self.transplant(k,k.right)
        else:
            k2 = k.right
            while k2.left:
                k2 = k2.left
            k2_c = k2.red
            k3 = k2.right
            if k2.parent == k:
                k3.parent = k2
            else:
                self.transplant(k2,k2.right)
                k2.right = k.right
                k2.right.parent = k2
            self.transplant(k,k2)
            k2.left = k.left
            k2.left.parent = k2
            k2.red = k.red
            if not k2_c:
                self.fix_remove(k3)

def driver():
    RBT = RedBlackTree()
    with open(sys.argv[1]) as f:
        n = int(f.readline().strip())
        for _ in range(n):
            in_data = f.readline().strip().split()
            action, value_option = in_data[0], in_data[1:]
            if action == "insert":
                value = int(value_option[0])
                RBT.insert(int(value))

            elif action == "remove":
                value = int(value_option[0])
                try:
                    RBT.remove(value)
                except RBT.EmptyTree:
                    print("TreeError")

            elif action == "inprint":
                try:
                    result = []
                    RBT.inprint(RBT.root, result)
                    print(' '.join(result))
                except RBT.EmptyTree:
                    print('Empty')

            elif action == "max":
                try:
                    result = RBT.max()
                    if result:
                        print(result)
                except RBT.EmptyTree:
                    print("Empty")

            elif action == "min":
                try:
                    result = RBT.min()
                    if result:
                        print(result)
                except RBT.EmptyTree:
                    print("Empty")

            elif action == "search":
                value = int(value_option[0])
                if RBT.search(value):
                    print('Found')
                else:
                    print('NotFound')

if __name__ == '__main__':
    driver()