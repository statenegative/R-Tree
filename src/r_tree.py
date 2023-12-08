# R-tree data structure.
import numpy as np
import numpy.typing as npt
import typing
from bounding_box import BoundingBox
from page import Page

Point = npt.NDArray

class R_Tree:
    # R-tree constructor.
    #
    # M: The number of entries a page can hold.
    # shape: The shape of the keys in this R-tree.
    def __init__(self, M: int, shape: int | tuple[int,...]=(2,)):
        if isinstance(shape, int):
            self.shape = (shape,)
        
        self.M = M
        self.shape = shape
        self.root = Page(shape, True)
        self.size = 0
    
    # Adds an entry into the R-tree.
    #
    # key: The key to insert.
    # val: The value to insert.
    def add(self, key: Point, val: typing.Any=None):
        split = self.__add(self.root, key, val)

        # Handle creating new root
        if split:
            old_root = self.root
            new_child = old_root.split()
            self.root = Page(self.shape, False)
            self.root.add(old_root)
            self.root.add(new_child)

    
    def __setitem__(self, key: Point, val: typing.Any=None):
        self.add(key, val)
    
    # Gets the total number of entries in the R-tree.
    def __len__(self) -> int:
        return self.size
    
    # Internal recursive add function to handle splitting.
    #
    # page: The page being recursively processed.
    # key: The key to insert.
    # val: The value to insert.
    # Returns whether a split needs to occur.
    def __add(self, page: Page, key: Point, val: typing.Any) -> bool:
        # Leaf case
        if page.leaf:
            page.add(key, val)
            return len(page) > self.M

        # Determine child page to traverse
        child = page.least_enlargement(point)
        # Since this page isn't a leaf, least_enlargement is guaranteed to return a value
        split = self.__add(child, key, val)
        
        # Handle splitting
        if split:
            new_child = child.split()
            page.add(new_child)
            return len(page) > self.M
        
    def search(self, radius, origin):

        #this doesnt make help me
        upper = origin + radius
        lower = origin - radius
        box = BoundingBox(lower, upper)
        return self.__search(self.root,box,origin,radius)


        #private workhorse function
    def __search(self, page: Page, box, origin, radius):
        if page.leaf:
            ret = []
            for point,_ in page.entries:
                if R_Tree.__dist(origin, point) <= radius:
                    ret.append(point)
            return ret
                   
        #if it intersects run through all its children
        ret = []
        if page.bounding_box.intersects(box):
            for x,_ in page.entries:
                if x.bounding_box.intersects(box):
                    ret += self.__search(x, box,origin,radius)
        return ret
        
        
   
    def __dist(a,b):
        return np.linalg.norm(b-a)

def main():
    t = R_Tree(2)
    p1 = Page()
    p2 = Page(leaf = True)
    p3 = Page(leaf = True)
    p2.add(np.array([1,1]))
    p2.add(np.array([2,2]))
    p3.add(np.array([3,4]))
    p3.add(np.array([4,3]))

    p1.add(p3)
    p1.add(p2)
    t.root = p1
    print(t.search(3, np.array([1.5,1.5])))
    
    
if __name__ == "__main__":
    main()