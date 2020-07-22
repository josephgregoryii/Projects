from sys import argv

class Queue:
    class Underflow(Exception):
        def __init__(self, data=None):
            super().__init__(data)

    class Node:
        def __init__(self, data=None):
            self.data = data
            self.next = None

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def enqueue(self, x: "datum") -> None:
        n = self.Node(x)
        if self.head == None:
            self.head = n
        else:
            self.tail.next = n
        self.tail = n
        self.size += 1

    def dequeue(self) -> "datum":
        if self.head == None:
            raise Queue.Underflow("QueueError")
        n = self.head
        self.head = n.next
        if self.head == None:
            self.tail = None
        self.size -= 1
        return n.data

    def is_empty(self) -> bool:
        if self.head == None:
            return True
        else:
            return False

    def __len__(self):
        return self.size

class STNode:

    def __init__(self, x: str):
        self.key = x
        self.left = None
        self.right = None


class SyntaxTree:

    def init_helper(self, i: int, l: 'list of strings') -> STNode:
        if i >= len(l):
            return None

        node = STNode(l[i])
        node.left = self.init_helper(2 * i, l)
        node.right = self.init_helper(2 * i + 1, l)
        return node

    def __init__(self, l: 'list of strings') -> 'complete syntax tree':
        self.root = self.init_helper(1, l)

    # TODO: method to generate fully parenthesized expression

    def postorder_helper(self, n: STNode, l):
        if n != None:
            self.postorder_helper(n.left, l)
            self.postorder_helper(n.right, l)
            l.append(n.key)

    def preorder_helper(self, n: STNode, l: "list of keys"):
        if n != None:
            l.append(n.key)
            self.preorder_helper(n.left,l)
            self.preorder_helper(n.right,l)

    def inorder_helper(self, n: STNode, l: "list of keys"):
        if n != None:
            self.inorder_helper(n.left, l)
            l.append(n.key)
            self.inorder_helper(n.right, l)

    def stprint(self,node, result):
        if node != None:
            if node.left is None and node.right is None:
                result.append(node.key)
            else:
                result.append('(')
                self.stprint(node.left,result)
                result.append(node.key)
                self.stprint(node.right,result)
                result.append(')')
        return ''.join(result)


    def evaluate(self,root):
        if root is None:
            return 0

        if root.left is None and root.right is None:
            return int(root.key)

        left_sum = self.evaluate(root.left)

        right_sum = self.evaluate(root.right)

        if root.key == '+':
            return left_sum + right_sum

        elif root.key == '-':
            return left_sum - right_sum

        elif root.key == '*':
            return left_sum * right_sum

        else:
            return left_sum / right_sum


def driver():
    f = open(argv[1], "r")
    nl = int(f.readline().strip())
    symbol_list = [None] + f.readline().strip().split()
    ST = SyntaxTree(symbol_list)
    result = []
    print(ST.stprint(ST.root, result))
    print(ST.evaluate(ST.root))

if __name__ == '__main__':
    driver()
