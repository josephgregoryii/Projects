#simple stack class
class Stack:
    class Underflow(Exception):
        def __init__(self,data=None):
            super().__init__(data)

    class Node:
        def __init__(self, data = None):
            self.data = data
            self.next = None
    def __init__(self):
        self.head = None

    def push(self, data: "datum"):
        node = self.Node(data)
        node.next = self.head
        self.head = node

    def pop(self) -> "datum":
        if self.head == None:
            raise Stack.Underflow("Stack.pop() invoked on an empty stack.")
        node = self.head
        self.head = node.next
        return node.data

    def is_empty(self) -> bool:
        if self.head == None:
            return True
        else:
            return False



