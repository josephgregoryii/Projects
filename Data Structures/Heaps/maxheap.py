class MaxHeap:
    class Underflow(Exception):
        def __init__(self,data = None):
            super().__init__(data)

    def __init__(self,array = None):
        if array == None:
            self.heapsize = 0
            self.length = 1025
            self.array = [None] * self.length
        else:
            self.length = len(array) + 1
            self.array = [None] * self.length
            for i in range(len(array)):
                self.array[i+1] = array[i]
            self.heapsize = self.length - 1
            i = self.length // 2
            while i > 0:
                self.sift_down(i)
                i -= 1

    def __len__(self):
        return self.heapsize

    def __str__(self):
        return self.to_string(self.array[1:self.heapsize+1])

    def size(self) -> int:
        return self.heapsize

    def is_empty(self) -> bool:
        if self.heapsize == 0:
            return True
        else:
            return False

    def max(self):
        return self.array[1]

    def heap_size(self):
        return self.heapsize

    def to_string(self,array):
        if len(array) == 0:
            result = "Empty"
        else:
            v = []
            for i in range(1,self.heapsize+1):
                v.append(str(self.array[i]))
            result = "\n".join(v)
        return result

    def sift_down(self,i : int) -> None:
        left = 2*i
        right = left + 1
        largest = i
        if left <= self.heapsize and self.array[left] > self.array[largest]:
            largest = left
        if right <= self.heapsize and self.array[right] > self.array[largest]:
            largest = right
        if largest != i:
            x = self.array[i]
            self.array[i] = self.array[largest]
            self.array[largest] = x
            self.sift_down(largest)

    def sift_up(self, i: int) -> None:
        parent = i//2
        while i > 1 and self.array[parent] < self.array[i]:
            x = self.array[parent]
            self.array[parent] = self.array[i]
            self.array[i] = x
            i = parent
            parent = i//2

    def insert(self, x: "comparable") -> None:
        if self.heapsize >= self.length-1:
            nlength = 2*self.length
            narray = [None] * nlength
            for i in range(1,self.heapsize+1):
                narray[i] = self.arrray[i]
            self.length = nlength
            self.array = narray
        self.heapsize += 1
        self.array[self.heapsize] = x
        self.sift_up(self.heapsize)

    def remove(self) -> "comparable":
        if self.heapsize == 0:
            raise BinaryHeap.Underflow("Empty heap on remove()")
        minimum = self.array[1]
        self.array[1] = self.array[self.heapsize]
        self.heapsize -= 1
        self.sift_down(1)
        return minimum

    def look(self) -> "comparable":
        if self.heapsize == 0:
            raise BinaryHeap.Underflow("Empty heap on look()")
        return self.array[1]

    def print_elem(self):
        i = self.heapsize
        while i > 0:
            print(self.remove())
            i -= 1