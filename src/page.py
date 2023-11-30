# R-tree page data structure.
import numpy as np
import numpy.typing as npt
import typing

from bounding_box import BoundingBox

Point = npt.NDArray

# R-tree page data structure.
#
# Individual pages do not handle splitting, since it is done in-place.
class Page:
    # Page constructor.
    #
    # shape: The shape of the keys in this page.
    # leaf: Whether this page is a leaf node. This is used to avoid checking types.
    def __init__(self, shape: int | tuple[int,...]=(2,), leaf: bool=False):
        # Convert shape to tuple
        if isinstance(shape, int):
            self.shape = (shape,)
        
        # Create bounding box and entries list
        self.shape = shape
        self.leaf = leaf
        self.entries = []
        self.bounding_box = BoundingBox(np.full(shape, np.inf), np.full(shape, -np.inf))
    
    # Inserts an entry into the page.
    #
    # key: The key to insert. Either a point or a page, depending on whether this page is a leaf.
    # val: The value to insert. If this page isn't a leaf, val should be None.
    def add(self, key: typing.Union[Point, "Page"], val: typing.Any=None):
        # Add entry
        self.entries.append((key, val))

        # Update bounding box
        if self.leaf:
            self.bounding_box.fit_point(key)
        else:
            self.bounding_box.fit_box(key.bounding_box)
    
    # Gets the child page that would require the least enlargement if point were inserted.
    #
    # point: The point to test for insertion.
    # Returns the page, or None if there are no child pages.
    def least_enlargement(self, point: Point) -> typing.Optional["Page"]:
        if self.leaf or len(self) == 0:
            return []

        # Find all children that this point is contained within
        min_enlargement = np.inf
        min_page = self.entries[0][0]
        for page, _ in self.entries[1:]:
            # If an exact match is found, return immediately
            if point in page.bounding_box:
                return page
            # Calculate increase in area
            area = page.bounding_box.test_enlargement(point)
            if area < min_enlargement:
                min_enlargement = area
                min_page = page
        
        return min_page
    
    # Splits this page, returning the newly split page.
    #
    # Returns a new page containing the entries that have been removed from this page.
    def split(self) -> "Page":
        pass
    
    def __setitem__(self, key: typing.Union[Point, "Page"], val: typing.Any=None):
        self.add(key, val)

    # Gets the number of entries in this page.
    def __len__(self) -> int:
        return len(self.entries)
    
    # Creates a string representation of this page.
    def __str__(self) -> str:
        data = []
        for entry in self.entries:
            if entry[1]:
                data.append(entry)
            else:
                data.append(entry[0])

        return f"Page({self.bounding_box}: {data})"
