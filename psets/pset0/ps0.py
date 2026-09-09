#################
#               #
# Problem Set 0 #
#               #
#################


#
# Setup
#
class BinaryTree:
    def __init__(self, root):
        """
        :param root: the root of the binary tree
        """
        self.root: BTvertex = root
 
class BTvertex:
    def __init__(self, key):
        """
        :param: the key associated with the vertex of the binary tree
        """
        self.parent: BTvertex = None
        self.left: BTvertex = None
        self.right: BTvertex = None
        self.key: int = key
        self.size: int = None
#
# Problem 1a
#

# Input: BTvertex v, the root of a BinaryTree of size n
# Output: Up to you
# Side effect: sets the size of each vertex n in the
# ... tree rooted at vertex v to the size of that subtree
# Runtime: O(n)
def calculate_sizes(v):
    # base case: when the subtree is empty/none
    #recursive case: calculate the size of both left and right subtrees then add 
    # together to determine size of node.

    # if the current node is none, return size 1
    if v == None:
        return 0
    # calculate the size of current node's v.left and v.right
    l = calculate_sizes(v.left)
    r = calculate_sizes(v.right)
    # add together v.left + v.right
    v.size = 1 + l + r
    # return v.size
    return v.size
#
# Problem 1c
#

# Input: a positive integer t, 
# ...BTvertex v, the root of a BinaryTree of size n >= 2t+1
# Output: BTvertex, descendent of v such that its size is between 
# ... t and 2t-1 (inclusive)
# Runtime: O(h) 

def FindDescendantOfSize(t, v):
    if v.left:
        left_size = v.left.size
    else:
        left_size = 0
    
    if v.right:
        right_size = v.right.size
    else:
        right_size = 0

    #figure out which child is bigger
    if left_size >= right_size:
        bigger = v.left
        bigger_size = left_size
    else: 
        bigger = v.right
        bigger_size = right_size

    #case 1: bigger child already in range
    if bigger_size >= t and bigger_size <= 2 * t - 1:
        return bigger
    #case 2: bigger child too big, then recurse
    else:
        return FindDescendantOfSize(t, bigger)
