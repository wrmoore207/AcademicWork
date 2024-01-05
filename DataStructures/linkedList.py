class Node:
    def __init__(self, data=None):
        self.data = data
        self.next_node = None

class LinkedList:
    def __init__(self):
        self.head=None
    
    def is_empty(self):
        return self.head is None
    
    def append(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
        else:
            current_node=self.head
            while current_node.next_node:
                current_node=current_node.next_node
            current_node.next_node= new_node
    
    def prepend(self, data):
        new_node = Node(data)
        new_node.next_node=self.head
        self.head=new_node
    
    def delete(self, data):
        # If there's nothing there, return 
        if self.is_empty():
            return
        # If the data you're deleting is the first node, 
        # delete it and assign head to next node
        if self.head.data==data:
            self.head = self.head.next_node
            return
        
        # Otherwise, iterate through the list until you find the node you're looking for
        current_node=self.head
        
        while current_node.next_node and current_node.next_node.data != data:
            current_node = current_node.next_node
        
        if current_node.next_node:
            current_node.next_node=current_node.next_node.next_node

    
    def display(self):
        current_node=self.head
        while current_node:
            print(current_node.data, end=" ->")
            current_node=current_node.next_node
        
        print("None")

my_list = LinkedList()
my_list.append(1)
my_list.append(2)
my_list.append(3)
my_list.prepend(0)
my_list.display()
my_list.delete(2)
my_list.display()