# R-tree data structure.
import matplotlib.pyplot as plt
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
            shape = (shape,)
        
        self.M = M
        self.shape = shape
        self.root = Page(shape, True)
        self.size = 0
    
    # Adds an entry into the R-tree.
    #
    # key: The key to insert.
    # val: The value to insert.
    def add(self, key: Point, val: typing.Any=None):
        self.size += 1
        split = self.__add(self.root, key, val)

        # Handle creating new root
        if split:
            old_root = self.root
            new_child = old_root.split()
            self.root = Page(self.shape, False)
            self.root.add(old_root)
            self.root.add(new_child)

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
        child = page.least_enlargement(key)
        # Since this page isn't a leaf, least_enlargement is guaranteed to return a value
        split = self.__add(child, key, val)
        
        # Handle splitting
        if split:
            new_child = child.split()
            page.add(new_child)
            return len(page) > self.M
    
    # Displays a 2D visualization of the R-tree.
    def plot2D(self, draw_boxes: bool=True):
        if self.shape == (2,):
            self.__plot2D(self.root, draw_boxes)
    
    # Recursive backend of show2D
    def __plot2D(self, page: Page, draw_boxes: bool, color: str='k'):
        # Display bounding box
        if draw_boxes:
            self.plot_box(page.bounding_box)

        # Base case
        if page.leaf:
            for point, _ in page.entries:
                plt.plot(point[0], point[1], f"{color}o")
        else:
            for child, _ in page.entries:
                self.__plot2D(child, draw_boxes)
    
    def plot_box(self, box: BoundingBox, color: str='k'):
        plt.plot((box.lower[0], box.upper[0]), (box.lower[1], box.lower[1]), f"{color}-")
        plt.plot((box.lower[0], box.lower[0]), (box.lower[1], box.upper[1]), f"{color}-")
        plt.plot((box.upper[0], box.upper[0]), (box.lower[1], box.upper[1]), f"{color}-")
        plt.plot((box.lower[0], box.upper[0]), (box.upper[1], box.upper[1]), f"{color}-")
    
    def __setitem__(self, key: Point, val: typing.Any=None):
        self.add(key, val)
    
    # Gets the total number of entries in the R-tree.
    def __len__(self) -> int:
        return self.size
    
    def __str__(self) -> str:
        return f"R_Tree({self.size}, {self.root})"
    
    def search(self, radius: float, origin: Point):
        #this doesnt make help me
        upper = origin + radius
        lower = origin - radius
        box = BoundingBox(lower, upper)
        return self.__search(self.root,box,origin,radius)

    # Private workhorse function
    def __search(self, page: Page, box: BoundingBox, origin: Point, radius: float):
        # Base case
        if page.leaf:
            ret = []
            for point,_ in page.entries:
                if R_Tree.__dist(origin, point) <= radius:
                    ret.append(point)
            return ret, [page.bounding_box]

        # If it intersects run through all its children
        ret1 = []
        ret2 = [page.bounding_box]
        if page.bounding_box.intersects(box):
            for x, _ in page.entries:
                if x.bounding_box.intersects(box):
                    points, boxes = self.__search(x, box, origin, radius)
                    ret1 += points
                    ret2 += boxes
        return ret1, ret2

    # N-dimensional distance function
    def __dist(a, b):
        return np.linalg.norm(b-a)
