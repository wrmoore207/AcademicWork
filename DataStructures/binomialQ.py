class BinaryMinHeap:
    """Binary Min Heap Implementation"""

    CAPACITY = 10

    def __init__(self):
        """Initialize BinaryMinHeap"""
        self.heap_list = [0]
        self.current_size = 0

    def move_up(self, i):
        """Move a value up in the tree"""
        while i // 2 > 0:
            if self.heap_list[i] < self.heap_list[i // 2]:
                self.heap_list[i], self.heap_list[i // 2] = self.heap_list[i // 2], self.heap_list[i]
            else:
                break
            i = i // 2

    def insert(self, k):
        """Add an element to the heap"""
        if self.current_size == self.CAPACITY:
            print("Heap is Full")
            return
        self.heap_list.append(k)
        self.current_size += 1
        self.move_up(self.current_size)

    def move_down(self, i):
        """Move an element down into place"""
        while (i * 2) <= self.current_size:
            mc = self.min_child(i)
            if self.heap_list[i] > self.heap_list[mc]:
                self.heap_list[i], self.heap_list[mc] = self.heap_list[mc], self.heap_list[i]
            i = mc

    def min_child(self, i):
        """Find the minimum child of a given node"""
        if (i * 2) + 1 > self.current_size:
            return i * 2
        else:
            return i * 2 if self.heap_list[i * 2] < self.heap_list[(i * 2) + 1] else (i * 2) + 1

    def delete_min(self):
        """Remove the minimum value in the heap"""
        if len(self.heap_list) == 1:
            raise IndexError("Heap is empty")
        root = self.heap_list[1]
        self.heap_list[1] = self.heap_list[self.current_size]
        self.heap_list.pop()
        self.current_size -= 1
        self.move_down(1)
        return root


# Driver Code
my_heap = BinaryMinHeap()

my_heap.insert(5)
my_heap.insert(14)
my_heap.insert(25)
my_heap.insert(2)
my_heap.insert(13)
my_heap.insert(38)
my_heap.insert(79)
my_heap.insert(22)
my_heap.insert(-1)
my_heap.insert(131)

print(my_heap.current_size)

print(my_heap.delete_min())
