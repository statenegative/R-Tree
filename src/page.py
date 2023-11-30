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
    # entry: The entry to insert. Either a point or a page, depending on whether this page is a leaf.
    def add(self, entry: typing.Union[Point, "Page"]):
        # Add entry
        self.entries.append(entry)

        # Update bounding box
        if self.leaf:
            self.bounding_box.fit_point(entry)
        else:
            self.bounding_box.fit_box(entry)

    # Gets the number of entries in this page.
    def __len__(self) -> int:
        return len(self.entries)
    
    # Creates a string representation of this page.
    def __str__(self) -> str:
        return f"Page({self.bounding_box}: {self.entries})"
