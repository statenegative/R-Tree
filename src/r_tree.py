# R-tree data structure.
import numpy as np
import numpy.typing as npt
import typing

from page import Page

Point = npt.NDArray

class R_Tree:
    # R-tree constructor.
    #
    # M: The number of entries a page can hold.
    # shape: The shape of the keys in this R-tree.
    def __init__(M: int, shape: int | tuple[int,...]=(2,)):
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
        # Since this page isn't a leaf, least_enlargement is guaranteed to return a value
        child = page.least_enlargement(point)
        split = self.__add(child, key, val)
        
        # Handle splitting
        if split:
            new_child = child.split()
            page.add(new_child)
            return len(page) > self.M
