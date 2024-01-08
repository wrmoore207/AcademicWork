class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, root, key):
        if root is None:
            return Node(key)
        else:
            if key < root.val:
                root.left = self._insert(root.left, key)
            else:
                root.right = self._insert(root.right, key)
        return root

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, root, key):
        if root is None or root.val == key:
            return root
        if key < root.val:
            return self._search(root.left, key)
        return self._search(root.right, key)


# Example usage:
bst = BinarySearchTree()

keys = [10, 5, 15, 3, 7, 12, 18]

for key in keys:
    bst.insert(key)

# Search for a key in the BST
search_key = 7
result = bst.search(search_key)

if result:
    print(f"{search_key} found in the BST.")
else:
    print(f"{search_key} not found in the BST.")