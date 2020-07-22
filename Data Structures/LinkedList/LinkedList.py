class LinkedList(object):
    class Node(object):
        def __init__(self, data=None):
            self.data = data
            self.next = None
            self.prev = None

        def __repr__(self):
            return str(self.data)

    def __init__(self):
        self.size = 0
        self.sntl = self.Node()
        self.sntl.next = self.sntl
        self.sntl.prev = self.sntl

    def __len__(self):
        return self.size

    def __str__(self):
        v = []
        v.append('head')
        x = self.sntl.next
        while x != self.sntl:
            v.append('->')
            v.append(str(x.data))
            x = x.next

        return " ".join(v)

    def search(self, key):
        x = self.sntl.next
        while x != self.sntl and x.data != key:
            x = x.next
        if x == self.sntl:
            x = None
        return x

    def insert(self, x):
        node = self.Node(x)
        node.next = self.sntl.next
        self.sntl.next.prev = node
        self.sntl.next = node
        node.prev = self.sntl
        self.size += 1

    def insert_Q(self, x):
        node = self.Node(x)
        node.prev = self.sntl.prev
        node.next = self.sntl.prev.next
        self.sntl.prev.next = node
        node.next.prev = node
        self.size += 1

    def delete(self, x):
        x.prev.next = x.next
        x.next.prev = x.prev
        self.size -= 1
