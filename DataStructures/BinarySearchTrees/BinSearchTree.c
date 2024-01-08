#include <stdio.h>
#include <stdlib.h>

// Create a node data struct to store data within
// our BST. In our case, we will store 'integers'
typedef struct bstnode {
    int data;               // data each node holds
    struct bstnode* leftChild; // pointer to the left child (if any)
    struct bstnode* rightChild; // pointer to the right child (if any)
} bstnode_t;

// Our BST data structure
// Our BST holds a pointer to the root node in our BST.
typedef struct bst {
    unsigned int size;  // Size keeps track of how many items are in the BST.
                        // Size should be incremented when we add.
    bstnode_t* root;    // root points to the root node in our BST.
} bst_t;

// Function prototypes
bstnode_t* makeNode(int data);
bst_t* bst_create();
int bst_empty(bst_t* t);
int bst_add(bst_t* t, int item);
int addHelper(bstnode_t* existingNode, bstnode_t* newNode);
void bst_print(bst_t* t, int order);
void prePrint(bstnode_t* node);
void iOPrint(bstnode_t* node);
void postPrint(bstnode_t* node);
int bst_sum(bst_t* t);
int bst_find(bst_t* t, int value);
unsigned int bst_size(bst_t* t);
void bst_free(bst_t* t);

// Function to create a new node
bstnode_t* makeNode(int data) {
    bstnode_t* newNode = (bstnode_t*)malloc(sizeof(bstnode_t));
    newNode->data = data;
    newNode->leftChild = NULL;
    newNode->rightChild = NULL;
    return newNode;
}

// Function to create a new BST
bst_t* bst_create() {
    bst_t* newBST = (bst_t*)malloc(sizeof(bst_t));
    newBST->size = 0;
    newBST->root = NULL;
    return newBST;
}

// Function to check if the BST is empty
int bst_empty(bst_t* t) {
    if (t == NULL) {
        return -1;
    }
    return t->size == 0 ? 0 : 1;
}

// Function to add a new item to the BST
int bst_add(bst_t* t, int item) {
    if (t == NULL) {
        return -1;
    }
    bstnode_t* newNode = makeNode(item);

    if (t->root == NULL) {
        t->root = newNode;
        t->size++;
        return 1;
    }

    addHelper(t->root, newNode);
    t->size++;
    return 1;
}

// Helper function to add a new node recursively
int addHelper(bstnode_t* existingNode, bstnode_t* newNode) {
    if (newNode->data < existingNode->data) {
        if (existingNode->leftChild == NULL) {
            existingNode->leftChild = newNode;
        } else {
            addHelper(existingNode->leftChild, newNode);
        }
    } else if (newNode->data > existingNode->data) {
        if (existingNode->rightChild == NULL) {
            existingNode->rightChild = newNode;
        } else {
            addHelper(existingNode->rightChild, newNode);
        }
    }
    return 0;
}

// Function to print the BST in different orders
void bst_print(bst_t* t, int order) {
    if (t == NULL) {
        return;
    }

    if (order != -1 && order != 0 && order != 1) {
        return;
    }

    if (order == -1) {
        prePrint(t->root);
    }

    if (order == 0) {
        iOPrint(t->root);
    }

    if (order == 1) {
        postPrint(t->root);
    }
}

// Helper function to print the BST in pre-order
void prePrint(bstnode_t* node) {
    if (node == NULL) {
        return;
    } else {
        prePrint(node->leftChild);
        printf("%d\n", node->data);
        prePrint(node->rightChild);
    }
}

// Helper function to print the BST in in-order
void iOPrint(bstnode_t* node) {
    if (node == NULL) {
        return;
    } else {
        iOPrint(node->leftChild);
        printf("%d\n", node->data);
        iOPrint(node->rightChild);
    }
}

// Helper function to print the BST in post-order
void postPrint(bstnode_t* node) {
    if (node == NULL) {
        return;
    } else {
        postPrint(node->leftChild);
        postPrint(node->rightChild);
        printf("%d\n", node->data);
    }
}

// Function to calculate the sum of all elements in the BST
int bst_sum(bst_t* t) {
    if (t == NULL || t->root == NULL) {
        return 0;
    }

    // Sum will be calculated recursively
    int sum = 0;
    bstnode_t* root = t->root;

    // Perform in-order traversal and accumulate the sum
    sumHelper(root, &sum);

    return sum;
}

// Helper function to calculate the sum recursively
void sumHelper(bstnode_t* node, int* sum) {
    if (node == NULL) {
        return;
    }

    sumHelper(node->leftChild, sum);
    *sum += node->data;
    sumHelper(node->rightChild, sum);
}

// Function to find a specific value in the BST
int bst_find(bst_t* t, int value) {
    if (t == NULL || t->root == NULL) {
        return 0;
    }

    // Search for the value recursively
    return findHelper(t->root, value);
}

// Helper function to find a specific value recursively
int findHelper(bstnode_t* node, int value) {
    if (node == NULL) {
        return 0;  // Value not found
    }

    if (node->data == value) {
        return 1;  // Value found
    } else if (value < node->data) {
        return findHelper(node->leftChild, value);
    } else {
        return findHelper(node->rightChild, value);
    }
}

// Function to get the size of the BST
unsigned int bst_size(bst_t* t) {
    if (t == NULL) {
        return 0;
    }
    return t->size;
}

// Function to free the memory allocated for the BST
void bst_free(bst_t* t) {
    if (t != NULL) {
        // Free the memory recursively
        freeHelper(t->root);
        // Free the BST structure
        free(t);
    }
}

// Helper function to free the memory recursively
void freeHelper(bstnode_t* node) {
    if (node != NULL) {
        freeHelper(node->leftChild);
        freeHelper(node->rightChild);
       
int main() {
    // Create a new BST
    bst_t* myBST = bst_create();

    // Add elements to the BST
    bst_add(myBST, 50);
    bst_add(myBST, 30);
    bst_add(myBST, 70);
    bst_add(myBST, 20);
    bst_add(myBST, 40);
    bst_add(myBST, 60);
    bst_add(myBST, 80);

    // Check if the BST is empty
    printf("Is the BST empty? %s\n", bst_empty(myBST) ? "Yes" : "No");

    // Print the BST in in-order
    printf("In-order traversal:\n");
    bst_print(myBST, 0);

    // Print the sum of elements in the BST
    printf("Sum of elements: %d\n", bst_sum(myBST));

    // Search for a value in the BST
    int searchValue = 40;
    printf("Is %d present in the BST? %s\n", searchValue, bst_find(myBST, searchValue) ? "Yes" : "No");

    // Get the size of the BST
    printf("Size of the BST: %u\n", bst_size(myBST));

    // Free the memory allocated for the BST
    bst_free(myBST);

    return 0;
}