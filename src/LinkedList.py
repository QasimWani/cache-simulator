#Define node
class Node:
    def __init__(self, dirty_bit, tag_bits):
        """ 
        Define doubly linked list structure
        """
        self.dirty = dirty_bit
        self.tag = tag_bits
        self.prev = None
        self.next = None

### Construct a doubly linked list
class DoublyLinkedList:
    """ Define LinkedList for fast read-ins in cache.py """
    def __init__(self):
        self.head = None
        self.tail = None

    #Time: O(1) ; Space: O(1)
    def setHead(self, node):
        if(self.head is None):
            self.head = node
            self.tail = node
        else:
            self.insertBefore(self.head, node)

    #Time: O(1) ; Space: O(1)
    def setTail(self, node):
        if(self.tail is None):
            self.tail = node
            self.head = node
        else:
            self.insertAfter(self.tail, node)

    #Time: O(1) ; Space: O(1)
    def insertBefore(self, node, nodeToInsert):
        if(node is None): #set head & tail
            self.setHead(nodeToInsert)
            return
        self.remove(nodeToInsert)

        if(node.prev == None): #inserting at head
            nodeToInsert.next = node
            node.prev = nodeToInsert
            node = node.prev
            self.head = node
            curr = self.head
            return

        nodeToInsert.prev = node.prev
        nodeToInsert.next = node
        node.prev.next = nodeToInsert
        node.prev = nodeToInsert
        
    #Time: O(1) ; Space: O(1)
    def insertAfter(self, node, nodeToInsert):
        if(node is None):#set head & tail
            self.setHead(nodeToInsert)
            return
        self.remove(nodeToInsert)

        if(node.next == None):#inserting at tail
            node.next = nodeToInsert
            nodeToInsert.prev = node
            self.tail = nodeToInsert
            return

        nodeToInsert.next = node.next
        nodeToInsert.prev = node
        node.next.prev = nodeToInsert
        node.next = nodeToInsert
        
    #Time: O(1) ; Space: O(1)
    def remove(self, node):
        if(node == self.head): #dealing with head
            self.head = self.head.next #reassign head to new head
        if(node == self.tail): #dealing with tail
            self.tail = self.tail.prev
        self.removeHelper(node)

    #Time: O(1) ; Space: O(1)
    def removeHelper(self, node):	
        if(node.next is not None):
            node.next.prev = node.prev
        if(node.prev is not None):
            node.prev.next = node.next
        node.next = None
        node.prev = None

    #Time: O(n) ; Space: O(1)
    def containsNodeWithValue(self, value):
        curr = self.head
        while(curr is not None):
            if(curr.tag == value):
                return curr 
            curr = curr.next
        return None
    
    #Time: O(n) ; Space: O(1)
    def LRU(self, node, isExist=False):
        #insert before headl (if exists in linkedlist) -> remove node.
        self.insertBefore(self.head, node)
        if(isExist):
            self.remove(node)
      
      
    #Time: O(n) ; Space: O(1)
    def getSize(self):
        """
        Get number of nodes in a Doubly Linked List
        """
        size = 0
        curr = self.head
        while(curr is not None):
            curr = curr.next
            size += 1
        return size
