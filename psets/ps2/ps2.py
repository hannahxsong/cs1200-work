class BinarySearchTree:
    # left: BinarySearchTree
    # right: BinarySearchTree
    # key: int
    # item: int
    # size: int
    def __init__(self, debugger = None):
        self.left = None
        self.right = None
        self.key = None
        self.item = None
        self._size = 1
        self.debugger = debugger

    @property
    def size(self):
         return self._size
       
     # a setter function
    @size.setter
    def size(self, a):
        debugger = self.debugger
        if debugger:
            debugger.inc_size_counter()
        self._size = a

    ####### Part a #######
    '''
    Calculates the size of the tree
    returns the size at a given node
    '''
    def calculate_sizes(self, debugger = None):
        # Debugging code
        # No need to modify
        # Provides counts
        if debugger is None:
            debugger = self.debugger
        if debugger:
            debugger.inc()

        # Implementation
        self.size = 1
        if self.right is not None:
            self.size += self.right.calculate_sizes(debugger)
        if self.left is not None:
            self.size += self.left.calculate_sizes(debugger)
        return self.size

    '''
    Select the ind-th key in the tree
    
    ind: a number between 0 and n-1 (the number of nodes/objects)
    returns BinarySearchTree/Node or None
    '''
    def select(self, ind):
        """
        error and correction explanation: 
        
        the select function returns the zero-based item at this rank in the subtree.

        the old version of code passed the same rank into the right subtree, and that rank still counted 
        the nodes in the left subtree and the current node, even though neither belongs to the 
        right subtree. subtracting both counts converts the requested rank into a rank local to
        the right subtree. subtree sizes let each call choose one child, so the search takes time
        proportional to the tree height rather than visiting every node.
        
        """
        # reject ranks that cannot name an item in this subtree.
        if ind < 0 or ind >= self.size:
            return None

        left_size = 0
        if self.left is not None:
            left_size = self.left.size
        if ind == left_size:
            return self
        if ind < left_size:
            return self.left.select(ind)
        if self.right is not None:
            # right-subtree ranks start after the left subtree and this node.
            return self.right.select(ind - left_size - 1)
        return None


    '''
    Searches for a given key
    returns a pointer to the object with target key or None (Roughgarden)
    '''
    def search(self, key):
        """
        this search method returns the node with the requested key or none if the key is absent.
        when the target is smaller than the current key, it can only be in the left subtree. but when
        the target is larger, it can only be in the right subtree. the method checks at most one child
        at each level and the running time is proportional to the tree's height.

        in this implementation, if the target and the right child is missing, the method may also check the left 
        subtree before returnign none. that subree cannot contain the target so this extra check does not change
        the answer but it's unnecessary work. 

        nontheless, this operation is already correct becuase a node divides the remaining keys
        into smaller keys on the left and larger keys on the right. comparing the target with the current key 
        lets the search continue down one branch, and reaching an empty child means the key is not present. 
        the work is proportional to the tree height and not the number of nodes.

        """
        if self is None:
            return None
        elif self.key == key:
            return self
        elif self.key < key and self.right is not None:
            return self.right.search(key)
        elif self.left is not None:
            return self.left.search(key)
        return None
    

    '''
    Inserts a key into the tree
    key: the key for the new node; 
        ... this is NOT a BinarySearchTree/Node, the function creates one
    
    returns the original (top level) tree - allows for easy chaining in tests
    '''
    def insert(self, key):
        """
        error and correction explanation: 

        the old version recalculated sizes by traversing a whole subtree after
        each recursive insertion. that repeated work could take time linear in
        the number of nodes (or more across the recursive calls). the helper
        now follows only the insertion path and updates sizes on the way back.

        """
        self._insert(key)
        return self

    def _insert(self, key):
        """
        instead of caculate_sizes(), which just rescanned the tree after insertion, i created this 
        function (_insert) to instead report whether it added a new key, so only the nodes along that
        insertion path needs their sizes increased. the outer insert method will still return the root
        tree which preserves the existing API; _insert will just handle all the recursive work and return
        the success flag. 

        how _insert works: a new leaf starts with size one. each ancestor increases its size only when 
        the recursive call actually added a key, so duplicate keys do not change any sizes. only nodes 
        on the search path are visited or updated, making insertion take time proportional to the tree height.

        """
        if self.key is None:
            self.key = key
            return True
        if self.key == key:
            return False

        if key < self.key:
            if self.left is None:
                self.left = BinarySearchTree(self.debugger)
                self.left.key = key
                inserted = True
            else:
                inserted = self.left._insert(key)
        else:
            if self.right is None:
                self.right = BinarySearchTree(self.debugger)
                self.right.key = key
                inserted = True
            else:
                inserted = self.right._insert(key)

        # a successful insertion adds exactly one node to each ancestor subtree.
        if inserted:
            self.size += 1
        return inserted


    """
        Answer to 3b:

        (basic) Pseudocode:
        right rotation at x:

            # move b so it becomes x's left subtree
            x.left = y.right

            #make x the right child of y
            y.right = x

            #recompute the lower node first using its new children
            x.size = 1 + siez(x.left) + size(x.right)
            
            #then recompute y, whose right subtree is now x
            y.size = 1 + size(y.left) + size(y.right)

            return y

        size(node) means the stored subtree size of node or 0 when it's empty. returning y indicates that 
        is's now the root this subtree; a full implemenation also reconnects it to the old parent or makes it
        the tree root if x was the tree root.  

        the rotation directly chances the children of x and y so their old size values may no longer by correct.
        this recomputes x first because it's now below y, then recompute y using x's unpdated size. the other
        subtrees keep the same nodes, so their sizes remain valid and only a constant number of pointers and size
        values are touched -- explaining why the rotation only takes O(1) run time. 

    """