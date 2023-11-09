# R-tree page entry bounding box
import numpy as np
import numpy.typing as npt
import typing

class BoundingBox:
    # Bounding box constructor.
    #
    # lower: The lower bounds of the bounding box.
    # upper: The upper bounds of the bounding box.
    def __init__(self, lower: npt.NDArray, upper: npt.NDArray):
        if lower.shape != upper.shape:
            raise ValueError(f"Shape mismatch: lower bound has shape {lower.shape}, but upper bound has shape {upper.shape}.")
        self.lower = lower
        self.upper = upper
        self.shape = lower.shape
    
    # Determines whether another bounding box intersects with this one.
    #
    # other: The other bounding box to check.
    def intersects(self, other: "BoundingBox") -> bool:
        intersects_lower = (self.lower <= box.lower) & (box.lower <= self.upper)
        intersects_upper = (self.lower <= box.upper) & (box.upper <= self.upper)
        return all(intersects_lower | intersects_upper)

    # Checks if a point is contained within this bounding box.
    #
    # point: The point to check.
    def contains_point(self, point: npt.NDArray) -> bool:
        return all((self.lower <= point) & (point <= self.upper))
    
    # Creates a string representation of this bounding box.
    def __str__(self) -> str:
        return f"BoundingBox({self.lower}, {self.upper})"
    
