class Queue:
    class Underflow(Exception):
        def __init__(self, data = None):
            super().__init__(data)

    class Node:
        def __init__(self, data = None):
            self.data = data
            self.next = None

    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, data: "datum") -> None:
        node = self.Node(data)
        if self.head == None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node

    def dequeue(self) -> "datum":
        if self.head == None:
            raise Queue.Underflow("QueueError")
        node = self.head
        self.head = node.next
        if self.head == None:
            self.tail = None
        return node.data

    def is_empty(self) -> bool:
        if self.head == None:
            return True
        else:
            return False