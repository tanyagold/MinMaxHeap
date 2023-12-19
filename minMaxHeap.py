# TANYA GOLDSHMID - BIG HOMEWORK
# "I hereby certify that this program is solely the result of my own work 
#    and is in compliance with the Academic Integrity policy of the course 
#    syllabus and the academic integrity policy of the CS department.”

# https://en.wikipedia.org/wiki/Min-max_heap
# https://www.baeldung.com/java-min-max-heap

import pytest
import math

class Node(object):
    def __init__(self, key, data):
        self.key  = key
        self.data = data

    def __str__(self): 
        return "(" + str(self.key) + "," + repr(self.data) + ")"

class MinMaxHeap(object):
    def __init__(self, capacity):
        self.__arr = [None] * capacity
        self.__nElems = 0
 
################################################################################
##############################   HELPER METHODS   ##############################
################################################################################

    # This function returns the index of the left child for a given index in a binary heap.
    def getIndexOfLeftChild(self, idx):
        return 2 * idx + 1

    # This function returns the index of the right child for a given index in a binary heap.
    def getIndexOfRightChild(self, idx):
        return 2 * idx + 2

    # This function returns a list containing the indexes of both the left and right children for a given index in a binary heap.
    def getIndexesOfChildren(self, idx):
        return [self.getIndexOfLeftChild(idx)] + [self.getIndexOfRightChild(idx)]

    # This function returns the indexes of all the grandchildren for a given index in a binary heap by combining the indexes of the children of the left and right child.
    def getIndexesOfGrandchildren(self, idx):
        return self.getIndexesOfChildren(self.getIndexOfLeftChild(idx)) + self.getIndexesOfChildren(self.getIndexOfRightChild(idx))

    # This function returns the indexes of both the children and grandchildren for a given index in a binary heap by combining the indexes obtained from the children and grandchildren functions.
    def getIndexesOfChildrenAndGrandchildren(self, idx):
        return self.getIndexesOfChildren(idx) + self.getIndexesOfGrandchildren(idx)

    # This function returns the index of the parent for a given index in a binary heap by performing a calculation based on the given index.
    def getIndexOfParent(self, idx):
        return int((idx - 1) / 2) 

    # This function returns the index of the grandparent for a given index in a binary heap by performing a calculation based on the given index.
    def getIndexOfGrandparent(self, idx):
        return int((idx - 3) / 4) 

    # This function determines whether a given index in a binary heap has a parent or not by checking if the index is greater than or equal to 1.
    def hasParent(self, idx):
        return idx >= 1    

    # This function determines whether a given index in a binary heap has a grandparent or not by checking if the index is greater than or equal to 3.
    def hasGrandparent(self, idx):
        return idx >= 3

    # This function checks if the binary heap is empty by comparing the number of elements to zero.
    ## EMPTY ## -> if the array is empty
    def isEmpty(self):
        return self.__nElems == 0

    # This function checks if the binary heap is full by comparing the number of elements to the length of the underlying array.
    ## FULL ## -> if every space in the array is occupied (aka full)
    def isFull(self):
        return self.__nElems == len(self.__arr)

    ## EVEN LEVEL ## 
    def isEvenLevel(self, idx): 
        # Calculate the level of the node at the given index
        level = int(math.floor(math.log2(idx + 1)))
        
        # Check if the level is even by checking if it is divisible by 2
        # If the level is even, return True; otherwise, return False
        return level % 2 == 0      

################################################################################
################################################################################

    ## BUILD ## -> creating the heap from the array 
    def create(self):
        # Iterate over the indexes of the heap starting from the last parent node and moving towards the root
        for idx in range(int(self.__nElems/2) -1, -1, -1):
            # Call the pushDown function to restore the heap property starting from the current index
            self.pushDown(idx)

    ## INSERTION ##
    def insert(self, item, data): 
        arr = self.__arr

        # Check if the heap is empty
        if self.isEmpty():
            # Insert the item at the first index
            arr[0] = Node(item, data)
            # Increment the number of elements in the heap
            self.__nElems += 1 

        # Check if the heap is not full
        elif not self.isFull():
            # Insert the item at the index __nElems
            arr[self.__nElems] = Node(item, data)
            # Increment the number of elements in the heap
            self.__nElems += 1
            # Perform a push-up operation to maintain the heap property
            self.pushUp(self.__nElems - 1)

        else:
            # Print an error message if the heap is full
            print("invalid operation: cannot insert because heap is full")    

    ## PUSH DOWN ## 
    def pushDown(self, idx):
        # Assign the heap array to a local variable
        arr = self.__arr

        # Check if the level of the index is even
        if self.isEvenLevel(idx):
            # If the current index is at an even level, perform the "push down min" operation
            self.pushDownMin(idx)
        else:
            # If the current index is at an odd level,  perform the "push down max" operation
            self.pushDownMax(idx) 

    ## PUSH DOWN MIN ## 
    def pushDownMin(self, idx):    
        # Assign the heap array to a local variable
        arr = self.__arr

        # Continue the loop as long as the index has a left child
        while self.getIndexOfLeftChild(idx) < self.__nElems:
            # Get the index of the smallest child or grandchild
            idxSmallest = self.getIndexOfSmallestChildOrGrandChild(idx)

            # Get the index of the parent of the smallest child or grandchild
            idxParent = self.getIndexOfParent(idxSmallest)

            # Get the index of the grandparent of the smallest child or grandchild
            idxGrandparent = self.getIndexOfGrandparent(idxSmallest)

            # Check if the grandparent is the current index
            if idxGrandparent == idx:  
                # Compare the smallest child with the current index
                if arr[idxSmallest].key < arr[idx].key:
                    # Swap them if the smallest child is smaller
                    arr[idxSmallest].key, arr[idx].key = arr[idx].key, arr[idxSmallest].key

                    # Check if the smallest child is larger than the parent
                    if arr[idxSmallest].key > arr[idxParent].key:
                        # Swap them if necessary
                        arr[idxSmallest].key, arr[idxParent].key = arr[idxParent].key, arr[idxSmallest].key

                    # Recursively push down the smallest child
                    self.pushDown(idxSmallest)

            # If the grandparent is not the current index
            # Compare the smallest child with the current index
            elif arr[idxSmallest].key < arr[idx].key:
                # Swap them if the smallest child is smaller
                arr[idxSmallest].key, arr[idx].key = arr[idx].key, arr[idxSmallest].key 

            # Update the index to the smallest child for the next iteration
            idx = idxSmallest

    ## PUSH DOWN MAX ## 
    def pushDownMax(self, idx):  
        # Assign the heap array to a local variable
        arr = self.__arr

        # Continue the loop until the index of the left child is within the bounds of the heap
        while self.getIndexOfLeftChild(idx) < self.__nElems:
            # Get the index of the largest child or grandchild
            idxLargest = self.getIndexOfLargestChildOrGrandChild(idx)

            # Get the index of the parent of the largest child or grandchild
            idxParent = self.getIndexOfParent(idxLargest)

            # Get the index of the grandparent of the largest child or grandchild
            idxGrandparent = self.getIndexOfGrandparent(idxLargest)            
            # Check if the current index is the grandparent of the largest child or grandchild
            if idxGrandparent == idx: 
                # Check if the largest child or grandchild is greater than the current index
                if arr[idxLargest].key > arr[idx].key:
                    # Swap the values of the largest child or grandchild and the current index
                    arr[idxLargest].key, arr[idx].key = arr[idx].key, arr[idxLargest].key

                    # Check if the value of the largest child or grandchild is now smaller than its parent
                    if arr[idxLargest].key < arr[idxParent].key:
                        # Swap the values of the largest child or grandchild and its parent
                        arr[idxLargest].key, arr[idxParent].key = arr[idxParent].key, arr[idxLargest].key

                    # Recursively call the pushDown function on the largest child or grandchild 
                    self.pushDown(idxLargest)

            # If the largest child or grandchild is greater than the current index        
            elif arr[idxLargest].key > arr[idx].key:
                # Swap the values of the largest child or grandchild and the current index
                arr[idxLargest].key, arr[idx].key = arr[idx].key, arr[idxLargest].key  

            # Update the current index to the index of the largest child or grandchild    
            idx = idxLargest

    ## Index of SMALLEST offspring ##   
    def getIndexOfSmallestChildOrGrandChild(self, idx):
        # Assign the heap array to a local variable
        arr = self.__arr
        # Initialize the index of the smallest child or grandchild to -1
        minIndex = -1
        # Initialize the minimum value to a large number
        minValue = 1000000

        # Iterate through the indexes of children and grandchildren 
        for i in self.getIndexesOfChildrenAndGrandchildren(idx):
            # Check if the index is within the range and the value is smaller than the current minimum
            if i < self.__nElems and arr[i].key < minValue:  
                # Update the index of the smallest child or grandchild
                minIndex = i
                # Update the minimum value
                minValue = arr[i].key

        # Return the index of the smallest child or grandchild
        return minIndex

    ## Index of LARGEST offspring ##        
    def getIndexOfLargestChildOrGrandChild(self, idx):
        # Assign the heap array to a local variable
        arr = self.__arr
        # Initialize the index of the largest child or grandchild to -1
        maxIndex = -1
        # Initialize the maximum value to a small number
        maxValue = -1000000

        # Iterate through the indexes of children and grandchildren
        for i in self.getIndexesOfChildrenAndGrandchildren(idx):
             # Check if the index is within the range and the value is greater than the current maximum
            if i < self.__nElems and arr[i].key > maxValue:
                # Update the index of the largest child or grandchild
                maxIndex = i
                # Update the maximum value
                maxValue = arr[i].key

        # Return the index of the largest child or grandchild
        return maxIndex   

    ## PUSH UP ##
    def pushUp(self, idx):
        # Assign the heap array to a local variable
        arr = self.__arr

        # Check if the index is not the root index
        if idx != 0:
            # Get the index of the parent
            idxParent = self.getIndexOfParent(idx)

            # Check if the current level is even
            if self.isEvenLevel(idx):
                # Check if the current value is greater than the parent value
                if arr[idx].key > arr[idxParent].key:
                    # Swap the values between the current and parent indexes
                    arr[idx].key, arr[idxParent].key = arr[idxParent].key, arr[idx].key
                    # Recursively push up the value at the parent index in the max heap
                    self.pushUpMax(idxParent)
                else:
                    # Recursively push up the value at the current index in the min heap
                    self.pushUpMin(idx)
            else:
                # Check if the current value is smaller than the parent value
                if arr[idx].key < arr[idxParent].key:
                    # Swap the values between the current and parent indexes
                    arr[idx].key, arr[idxParent].key = arr[idxParent].key, arr[idx].key
                    # Recursively push up the value at the parent index in the min heap
                    self.pushUpMin(idxParent)
                else:
                    # Recursively push up the value at the current index in the max heap
                    self.pushUpMax(idx)

    ## PUSH UP MIN ## 
    def pushUpMin(self, idx):
        # Assign the heap array to a local variable
        arr = self.__arr
        # Get the index of the grandparent
        idxGrandparent = self.getIndexOfGrandparent(idx)
        # Check if the node has a grandparent and the current value is smaller than the grandparent value
        if self.hasGrandparent(idx) and arr[idx].key < arr[idxGrandparent].key:
            # Swap the values between the current and grandparent indexes
            arr[idx].key, arr[idxGrandparent].key = arr[idxGrandparent].key, arr[idx].key
            # Recursively push up the value at the grandparent index in the min heap
            self.pushUpMin(idxGrandparent)

    ## PUSH UP MAX ##  
    def pushUpMax(self, idx):
        # Assign the heap array to a local variable
        arr = self.__arr
        # Get the index of the grandparent
        idxGrandparent = self.getIndexOfGrandparent(idx)

        # Check if the node has a grandparent and the current value is greater than the grandparent value
        if self.hasGrandparent(idx) and arr[idx].key > arr[idxGrandparent].key:
            # Swap the values between the current and grandparent indexes
            arr[idx].key, arr[idxGrandparent].key = arr[idxGrandparent].key, arr[idx].key
            # Recursively push up the value at the grandparent index in the max heap
            self.pushUpMax(idxGrandparent)    

    ## FIND MINIMUM ## 
    def findMin(self):
        # Assign the heap array to a local variable
        arr = self.__arr

        # Check if the heap is empty
        if self.__nElems == 0:
            # Return None if the heap is empty
            return None
        else:
            # Return the value at the first index of the heap (minimum value)
            return arr[0].key      

    ## FIND MAXIMUM ##
    def findMax(self):
        # Assign the heap array to a local variable
        arr = self.__arr

        # Check if the heap is empty
        if self.__nElems == 0:
            # Return None if the heap is empty
            return None
        # Check if the heap has only one element
        if self.__nElems == 1:
            # Return the value at the first index (maximum value in a max heap)
            return arr[0].key
        # Check if the heap has two elements
        elif self.__nElems == 2:
            # Return the value at the second index (maximum value in a max heap)
            return arr[1].key
        else:
            # Return the maximum value between the second and third index (maximum value in a max heap)
            return max(arr[1].key, arr[2].key)

    ## REMOVE MINIMUM ## 
    def removeMin(self):
        # Assign the heap array to a local variable
        arr = self.__arr

        # Find the minimum value in the heap
        minimum = self.findMin()
        # Check if the heap is not empty
        if minimum is not None:
             # Check if the heap has only one element
            if self.__nElems == 1:
                # Set the value at the first index to None
                arr[0].key = None
                # Decrement the number of elements
                self.__nElems -= 1
            else:
                # Replace the value at the first index with the value at the last index
                arr[0].key = arr[self.__nElems -1].key
                # Set the value at the last index to None
                arr[self.__nElems -1].key = None
                # Decrement the number of elements
                self.__nElems -= 1
                # Push down the value at the first index to maintain heap property
                self.pushDown(0)

        # Return the minimum value
        return minimum    

    ## REMOVE MAXIMUM ##
    def removeMax(self):
        # Assign the heap array to a local variable
        arr = self.__arr

        # Find the maximum value in the heap
        maximum = self.findMax()
        # Check if the heap is not empty
        if maximum is not None:
            # Check if the heap has only one element
            if self.__nElems == 1:
                # Set the value at the first index to None
                arr[0].key = None
                # Decrement the number of elements
                self.__nElems -= 1
            # Check if the heap has two elements
            elif self.__nElems == 2:
                # Set the value at the second index to None
                arr[1].key = None
                # Decrement the number of elements
                self.__nElems -= 1
            else:
                # Determine the index of the maximum value between the second and third index
                maxIndex = 2 if arr[1].key < arr[2].key else 1
                # Replace the value at the maxIndex with the value at the last index
                arr[maxIndex].key = arr[self.__nElems -1].key
                # Set the value at the last index to None
                arr[self.__nElems -1].key = None
                # Decrement the number of elements
                self.__nElems -= 1
                # Push down the value at the maxIndex to maintain heap property
                self.pushDown(maxIndex)
                
        # Return the maximum value
        return maximum 

################################################################################
################################################################################

    ## Checking if its a MinMaxHeap ##
    def isMinMaxHeap(self):
        # Assign the heap array to a local variable
        arr = self.__arr
        # Initialize the flag indicating if the heap is a min-max heap to True
        isMMHeap = True
        # Initialize a list to store the indices of nodes with incorrect parent-child relationship
        badParents = []
        # Check if the number of elements is correct
        ##isNumCorrect = self.__nElems == sum([1 if arr[i].key is not None else 0 for i in range(len(arr))])        

        for idx in range(int(self.__nElems / 2)):
            # Get the index of the left child
            idxLeft = self.getIndexOfLeftChild(idx)
            # Get the index of the right child
            idxRight = self.getIndexOfRightChild(idx)
            
            # Check if it is an even level in the min-max heap
            if self.isEvenLevel(idx):
                # Check if the left child violates the min-max heap property
                if idxLeft < self.__nElems and arr[idxLeft].key < arr[idx].key:
                     # Set the flag to False
                    isMMHeap = False
                    # Append the index of the parent to the list of bad parents
                    badParents.append(idx)
                    # Check if the right child violates the min-max heap property
                if idxRight > self.__nElems and arr[idxRight].key < arr[idx].key:
                    # Set the flag to False
                    isMMHeap = False  
                    # Append the index of the parent to the list of bad parents
                    badParents.append(idx)

            # Odd level in the min-max heap
            else:
                # Check if the left child violates the min-max heap property
                if idxLeft < self.__nElems and arr[idxLeft].key > arr[idx].key:
                    # Set the flag to False
                    isMMHeap = False
                    # Append the index of the parent to the list of bad parents
                    badParents.append(idx)
                    # Check if the right child violates the min-max heap property
                if idxRight > self.__nElems and arr[idxRight].key > arr[idx].key:
                    # Set the flag to False
                    isMMHeap = False 
                    # Append the index of the parent to the list of bad parents
                    badParents.append(idx)

        # Return the results indicating if it is a min-max heap, the list of bad parents, and the correctness of the number of elements
        return isMMHeap, badParents

################################################################################
##############################       VISUAL       ##############################
################################################################################

    ## DISPLAY 1 ##
    def displayHeap(self):
        # Print the label for the heap array
        print("heapArray: ", end="")
        # Iterate through the elements in the heap
        for m in range(self.__nElems):
            # Print each element followed by a space
            print(str(self.__arr[m]) + " ", end="")
            # Print a newline to separate the output
        print()

    ## DISPLAY 2 ##
    def __display(self, cur, indent):
        # Check if the current index is within the range of elements in the heap
        if cur < self.__nElems:
            # Calculate the index of the left child
            leftChild  = 2 * cur + 1  

            # Print the current element indented by the specified amount
            print(("-" * indent) + str(self.__arr[cur]))

            # Check if the left child index is within the range of elements in the heap
            if leftChild < self.__nElems:
                # Recursively call __display for the left child
                self.__display(leftChild,     indent + 2)
                # Recursively call __display for the right child (left child index + 1)
                self.__display(leftChild + 1, indent + 2)

    def display(self): 
        self.__display(0, 0)     

################################################################################
##############################      TESTING       ##############################
################################################################################

#def main():
    #size = 200

    #arr = [i for i in range(1, size - 10)]

    #minMaxHeap = MinMaxHeap(size)

    ###Must support insert
    #minMaxHeap.insert(len(arr), "")
    #minMaxHeap.insert(2, "")
    #minMaxHeap.insert(5, "")
    #minMaxHeap.insert(3, "")
    #minMaxHeap.insert(10, "")
    #minMaxHeap.insert(20, "")
    #minMaxHeap.insert(70, "")
    #print("after insert", minMaxHeap.isMinMaxHeap())

    #minMaxHeap.display()
    #minMaxHeap.displayHeap()    
    #print("after display", minMaxHeap.isMinMaxHeap())

    ### Must support find minimum
    #print("found the MIN", minMaxHeap.findMin())

    ### Must support find maximum
    #print("found the MAX", minMaxHeap.findMax())

    ### Must support remove minimum
    #print("removed the min", minMaxHeap.removeMin())
    #print("after remove min", minMaxHeap.isMinMaxHeap())

    #minMaxHeap.display()
    #minMaxHeap.displayHeap()    
    #print("after display 2", minMaxHeap.isMinMaxHeap())       

    ### Must support remove maximum
    #print("removed the max", minMaxHeap.removeMax())
    #print("after remove max", minMaxHeap.isMinMaxHeap())

    #minMaxHeap.display()
    #minMaxHeap.displayHeap()    
    #print("after last display", minMaxHeap.isMinMaxHeap())    

#main()

################################################################################
##############################      PYTESTS       ##############################
################################################################################

class TestMinMaxHeap(object):

    # 1) Test the isEvenLevel() method
    def test_isEvenLevel(self):
        heap = MinMaxHeap(100)
        assert heap.isEvenLevel(0) == True  # Root node is at even level
        assert heap.isEvenLevel(1) == False  # Left child of the root node is at odd level
        assert heap.isEvenLevel(2) == False  # Right child of the root node is at odd level
        assert heap.isEvenLevel(3) == True  # Left child of left child of the root node is at even level    

    # 2) Test the create() method
    def test_create(self):
        heap = MinMaxHeap(100)
        heap.create()
        assert heap.isEmpty() == True

    # 3) Test the insert() method
    def test_insert(self):
        heap = MinMaxHeap(100)

        # Test inserting into an empty heap
        heap.insert(10, "")
        assert heap.findMin() == 10  # Minimum value should be 10
        assert heap.findMax() == 10  # Maximum value should be 10

        # Test inserting into a non-empty heap
        heap.insert(5, "")
        assert heap.findMin() == 5  # Minimum value should be 5
        assert heap.findMax() == 10  # Maximum value should be 10

        heap.insert(15, "")
        assert heap.findMin() == 5  # Minimum value should still be 5
        assert heap.findMax() == 15  # Maximum value should be 15    

    # 4) Test the pushDown() method
    def test_pushDown(self):
        # Test when the index is at an even level
        heap = MinMaxHeap(100)
        heap.insert(5, "")
        heap.insert(10, "")
        heap.insert(15, "")
        heap.insert(20, "")
        heap.insert(25, "")
        heap.insert(30, "")
        heap.pushDown(0)
        assert heap.findMin() == 5  # Minimum value should still be 5 after pushDown
        assert heap.findMax() == 30  # Maximum value should still be 30 after pushDown

        # Test when the index is at an odd level
        heap = MinMaxHeap(100)
        heap.insert(30, "")
        heap.insert(25, "")
        heap.insert(20, "")
        heap.insert(15, "")
        heap.insert(10, "")
        heap.insert(5, "")
        heap.pushDown(0)
        assert heap.findMin() == 5  # Minimum value should still be 5 after pushDown
        assert heap.findMax() == 30  # Maximum value should still be 30 after pushDown

    # 5) Test the pushDownMin() method
    def test_pushDownMin(self):
        heap = MinMaxHeap(100)
        heap.insert(5, "")
        heap.insert(10, "")
        heap.insert(15, "")
        heap.insert(20, "")
        heap.insert(25, "")
        heap.insert(30, "")
        heap.pushDownMin(0)
        assert heap.findMin() == 5  # Minimum value should still be 5 after pushDownMin

    # 6) Test the pushDownMax() method
    def test_pushDownMax(self):
        heap = MinMaxHeap(100)
        heap.insert(30, "")
        heap.insert(25, "")
        heap.insert(20, "")
        heap.insert(15, "")
        heap.insert(10, "")
        heap.insert(5, "")
        heap.pushDownMax(0)
        assert heap.findMax() == 30  # Maximum value should still be 30 after pushDownMax

    # 7) Test the pushUp() method
    def test_pushUp(self):
        heap = MinMaxHeap(100)
        heap.insert(5, "")
        heap.insert(10, "")
        heap.insert(15, "")
        heap.insert(20, "")
        heap.insert(25, "")
        heap.insert(30, "")

        # Test pushing up on an even level index
        heap.pushUp(3)
        assert heap.findMax() == 30  # Maximum value should still be 30

        # Test pushing up on an odd level index
        heap.pushUp(2)
        assert heap.findMax() == 30  # Maximum value should still be 30

    # 8) Test the pushUpMin() method
    def test_pushUpMin(self):
        heap = MinMaxHeap(100)
        heap.insert(5, "")
        heap.insert(10, "")
        heap.insert(15, "")
        heap.insert(20, "")
        heap.insert(25, "")
        heap.insert(30, "")

        heap.pushUpMin(5)
        assert heap.findMin() == 5  # Minimum value should still be 5

    # 9) Test the pushUpMax() method
    def test_pushUpMax(self):
        heap = MinMaxHeap(100)
        heap.insert(5, "")
        heap.insert(10, "")
        heap.insert(15, "")
        heap.insert(20, "")
        heap.insert(25, "")
        heap.insert(30, "")

        heap.pushUpMax(2)
        assert heap.findMax() == 30  # Maximum value should still be 30

    # 10) Test the findMin() method
    def test_findMin(self):
        # Test finding minimum in an empty heap
        heap = MinMaxHeap(100)
        assert heap.findMin() is None

        # Test finding minimum in a heap with one element
        heap = MinMaxHeap(100)
        heap.insert(10, "")
        assert heap.findMin() == 10

        # Test finding minimum in a heap with multiple elements
        heap = MinMaxHeap(100)
        heap.insert(5, "")
        heap.insert(10, "")
        heap.insert(3, "")
        heap.insert(7, "")
        heap.insert(12, "")
        assert heap.findMin() == 3

    # 11) Test the findMax() method    
    def test_findMax(self):
        # Test finding maximum in an empty heap
        heap = MinMaxHeap(100)
        assert heap.findMax() is None

        # Test finding maximum in a heap with one element
        heap = MinMaxHeap(100)
        heap.insert(10, "")
        assert heap.findMax() == 10

        # Test finding maximum in a heap with two elements
        heap = MinMaxHeap(100)
        heap.insert(5, "")
        heap.insert(10, "")
        assert heap.findMax() == 10

        # Test finding maximum in a heap with three elements
        heap = MinMaxHeap(100)
        heap.insert(5, "")
        heap.insert(10, "")
        heap.insert(8, "")
        assert heap.findMax() == 10

    # 12) Test the removeMin() method    
    def test_removeMin(self):
        # Create a heap and insert elements
        heap = MinMaxHeap(100)
        heap.insert(8, "")
        heap.insert(10, "")
        heap.insert(3, "")
        heap.insert(7, "")

        # Check the removed minimum element and the heap state
        assert heap.removeMin() == 3
        assert heap.findMin() == 7
        assert heap.findMax() == 10

    # 13) Test the removeMax() method    
    def test_removeMax(self):
        # Test removing maximum from an empty heap
        heap = MinMaxHeap(100)
        assert heap.removeMax() is None

        # Test removing maximum from a heap with one element
        heap = MinMaxHeap(100)
        heap.insert(10, "")
        assert heap.removeMax() == 10
        assert heap.findMax() is None
        assert heap.findMin() is None

        # Test removing maximum from a heap with two elements
        heap = MinMaxHeap(100)
        heap.insert(5, "")
        heap.insert(10, "")
        assert heap.removeMax() == 10
        assert heap.findMax() == 5
        assert heap.findMin() == 5

        # Test removing maximum from a heap with three elements
        heap = MinMaxHeap(100)
        heap.insert(5, "")
        heap.insert(10, "")
        heap.insert(8, "")
        assert heap.removeMax() == 10
        assert heap.findMax() == 8
        assert heap.findMin() == 5

        # Test removing maximum from a heap with more than three elements
        heap = MinMaxHeap(100)
        heap.insert(10, "")
        heap.insert(20, "")
        heap.insert(15, "")
        heap.insert(30, "")
        heap.insert(25, "")
        assert heap.removeMax() == 30
        assert heap.findMax() == 25
        assert heap.findMin() == 10

    # 14) Test the entire MinMaxHeap functionality
    def test_minMaxHeap(self):
        heap = MinMaxHeap(100)

        # Test insertion
        heap.insert(10, "")
        heap.insert(20, "")
        heap.insert(15, "")
        heap.insert(5, "")
        heap.insert(25, "")
        heap.insert(30, "")
        assert heap.findMin() == 5  # Minimum value should be 5
        assert heap.findMax() == 30  # Maximum value should be 30

        # Test pushing up
        heap.pushUp(5)
        assert heap.findMax() == 30  # Maximum value should still be 30

        # Test pushing up min
        heap.pushUpMin(1)
        assert heap.findMin() == 5  # Minimum value should still be 5

        # Test pushing up max
        heap.pushUpMax(2)
        assert heap.findMax() == 30  # Maximum value should still be 30   

pytest.main(["-v", "-s", "minMaxHeap.py"])  