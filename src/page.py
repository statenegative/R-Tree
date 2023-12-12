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
        min_area = np.inf
        min_page = self.entries[0][0]
        for page, _ in self.entries[1:]:
            # If an exact match is found, return immediately
            if point in page.bounding_box:
                return page
            # Calculate increase in area
            area = page.bounding_box.test_point_enlargement(point)
            if area < min_area:
                min_area = area
                min_page = page
        
        return min_page
    
    # Splits this page, returning the newly split page.
    # This uses quadratic split, finding the two worst rectangles to put in a node
    # together, using them for the two children.
    #
    # Returns a new page containing the entries that have been removed from this page.
    def split(self) -> "Page":
        max_area = -np.inf
        max_pair = (0, 1)
        for i in range(len(self.entries)):
            for j in range(len(self.entries)):
                # Get entries
                a = self.entries[i][0]
                b = self.entries[j][0]

                if a is not b:
                    # Handle point and bounding box calculations separately
                    if self.leaf:
                        # Calculate new area
                        lower = np.minimum(a, b)
                        upper = np.maximum(a, b)
                    else:
                        # Calculate new area
                        lower = np.minimum(a.lower, b.lower)
                        upper = np.maximum(a.upper, b.upper)
                    # Calculate area and save if it's a new maximum
                    area = np.prod(upper - lower)
                    if area > max_area:
                        max_area = area
                        max_pair = (i, j)
        
        # Perform split
        a = self.entries[max_pair[0]][0]
        b = self.entries[max_pair[1]][0]
        page_a = Page(self.shape, self.leaf)
        page_b = Page(self.shape, self.leaf)
        page_a.add(a)
        page_b.add(b)

        # Examine all entries
        for entry, _ in self.entries:
            if entry is not a and entry is not b:
                area_a = page_a.bounding_box.area()
                area_b = page_b.bounding_box.area()
                if self.leaf:
                    enlargement_a = page_a.bounding_box.test_point_enlargement(entry) - area_a
                    enlargement_b = page_a.bounding_box.test_point_enlargement(entry) - area_b
                else:
                    enlargement_a = page_a.bounding_box.test_box_enlargement(entry) - area_a
                    enlargement_b = page_a.bounding_box.test_box_enlargement(entry) - area_b
                
                # Add entry to the better page
                if enlargement_a < enlargement_b:
                    page_a.add(entry)
                else:
                    page_b.add(entry)
        
        # Update pages
        self.entries = page_a.entries
        return page_b
    
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
