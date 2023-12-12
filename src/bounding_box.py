# R-tree page entry bounding box
import numpy as np
import numpy.typing as npt
import typing

Point = npt.NDArray

class BoundingBox:
    # Bounding box constructor.
    #
    # lower: The lower bounds of the bounding box.
    # upper: The upper bounds of the bounding box.
    def __init__(self, lower: Point, upper: Point):
        if lower.shape != upper.shape:
            raise ValueError(f"Shape mismatch: lower bound has shape {lower.shape}, but upper bound has shape {upper.shape}.")
        self.lower = np.array(lower)
        self.upper = np.array(upper)
    
    # Expands the bounding box to contain the given point.
    #
    # point: The point to contain.
    def fit_point(self, point: Point):
        self.lower = np.minimum(self.lower, point)
        self.upper = np.maximum(self.upper, point)

    # Expands the bounding box to fully contain the given bounding box.
    #
    # box: The box to contain.
    def fit_box(self, box: "BoundingBox"):
        self.lower = np.minimum(self.lower, box.lower)
        self.upper = np.maximum(self.upper, box.upper)
    
    # Determines whether another bounding box intersects with this one.
    #
    # other: The other bounding box to check.
    def intersects(self, other: "BoundingBox") -> bool:
        intersects_lower = (self.lower >= other.lower) & (self.lower <= other.upper)
        intersects_upper = (self.upper >= other.upper) & (self.upper <= other.upper)
        return all(intersects_lower | intersects_upper)

    # Calculates the area of this bounding box.
    def area(self) -> float:
        return np.prod(self.upper - self.lower)
    
    # Calculates the amount the area of this bounding box would increase to if point
    # were added to it.
    #
    # point: The point to test.
    # Returns the new theoretical area.
    def test_point_enlargement(self, point: Point) -> float:
        # Calculate new lower and upper bounds
        lower = np.minimum(self.lower, point)
        upper = np.maximum(self.upper, point)
        return np.prod(upper - lower)
    
    # Calculates the amount the area of this bounding box would increase to if point
    # were added to it.
    #
    # box: The box to test.
    # Returns the new theoretical area.
    def test_box_enlargement(self, box: BoundingBox) -> float:
        lower = np.minimum(self.lower, box.lower)
        upper = np.maximum(self.upper, box.upper)
        return np.prod(upper - lower)

    # Checks if a point is contained within this bounding box.
    #
    # point: The point to check.
    def __contains__(self, point: Point) -> bool:
        return all((self.lower <= point) & (point <= self.upper))
    
    # Creates a string representation of this bounding box.
    def __str__(self) -> str:
        return f"BoundingBox({self.lower}, {self.upper})"
    
