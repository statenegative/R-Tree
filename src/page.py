# R-tree page data structure
import numpy as np
import numpy.typing as npt
import typing

from bounding_box import BoundingBox

class Page:
    # Page constructor.
    #
    # shape: The shape of the keys stored in this page.
    # rtol: The relative tolerance (See numpy.isclose).
    # atol: The absolute tolerance (See numpy.isclose).
    def __init__(self, shape: tuple[int,...]=(2,), rtol=1e-05, atol=1e-08):
        # Convert shape to tuple
        if isinstance(shape, int):
            self.shape = (shape,)
        else:
            self.shape = shape
        self.rtol = rtol
        self.atol = atol
        self.entries = []
        self.min = np.ndarray(shape)
        self.max = np.ndarray(shape)
        self.__recompute_bounds()
    
    # Inserts an entry into this page.
    #
    # key: The bounding box or position of the entry.
    # val: The page or data associated with the entry.
    def insert(self, key: BoundingBox | npt.NDArray, val: typing.Union["Page", typing.Any]):
        # Check key shape
        if key.shape != self.shape:
            raise ValueError(f"Shape mismatch: key has shape {key.shape}, but page holds keys of shape {self.shape}.")
        
        # Add to entries list
        entry = Entry(key, val)
        self.entries.append(Entry(key, val))

        # Update bounding box
        if entry.is_point:
            self.min = np.minimum(self.min, key)
            self.max = np.maximum(self.max, key)
        else:
            self.min = np.minimum(self.min, key.lower)
            self.max = np.maximum(self.max, key.upper)
    
    # Inserts an entry into this page.
    #
    # key: The position or bounding box of the entry.
    # val: The page or data associated with the entry.
    def __setitem__(self, key: BoundingBox | npt.NDArray, val: typing.Union["Page", typing.Any]):
        self.insert(key, val)

    # Deletes an entry from this page.
    #
    # key: The entry to delete.
    def delete(self, key: BoundingBox | npt.NDArray):
        is_point = isinstance(key, npt.NDArray)

        # Find key in entries list
        found = False
        for i in range(len(self.entries)):
            entry = self.entries[i]
            # Compare key with entry
            if (((is_point and entry.is_point) and entry.isclose_box(key, self.rtol, self.atol))
                or ((not is_point and not entry.is_point) and entry.isclose_point(key, self.rtol, self.atol))):
                found = True
                break
        
        # Handle if entry wasn't found
        if not found:
            raise KeyError(f"Key not found in page.")
        
        # Remove entry
        del a[i]
        # Update bounding box
        self.__recompute_bounds()

    # Deletes an entry from this page.
    #
    # key: The entry to delete.
    def __delitem__(self, key: npt.NDArray):
        self.delete(key)
    
    # Gets the length of this page.
    def __len__(self) -> int:
        return len(self.entries)
    
    # Creates a string representation of this page.
    def __str__(self) -> str:
        return str([entry.key for entry in self.entries])

    # Recomputes this page's bounding box.
    def __recompute_bounds(self):
        self.__recompute_min()
        self.__recompute_max()
    
    # Recomputes this page's minimum bounds.
    def __recompute_min(self):
        self.min.fill(np.inf)
        for entry in self.entries:
            if entry.is_point:
                self.min = np.minimum(self.min, entry.key)
            else:
                self.min = np.minimum(self.min, entry.key.lower)

    # Recomputes this page's maximum bounds.
    def __recompute_max(self):
        self.max.fill(-np.inf)
        for entry in self.entries:
            if entry.is_point:
                self.max = np.maximum(self.max, entry.key)
            else:
                self.max = np.maximum(self.max, entry.key.upper)

# Page entry.
class Entry:
    # Entry constructor.
    #
    # key: The bounding box or position of this entry.
    # val: The page or data held by this entry.
    def __init__(self, key: BoundingBox | npt.NDArray, val: Page | typing.Any):
        self.is_point = not isinstance(key, BoundingBox)
        self.is_leaf = not isinstance(val, Page)
        self.key = key
        self.val = val

    # Checks whether a point is equal to this entry within a tolerance.
    #
    # other: The point to check against.
    # rtol: The relative tolerance (See numpy.isclose).
    # atol: The absolute tolerance (See numpy.isclose).
    def isclose_point(self, other: npt.NDArray, rtol: float=1e-05, atol: float=1e-08) -> bool:
        return np.isclose(self.key, other, rtol, atol)

    # Checks whether a bounding box is equal to this entry within a tolerance.
    #
    # other: The bounding box to check against.
    # rtol: The relative tolerance (See numpy.isclose).
    # atol: The absolute tolerance (See numpy.isclose).
    def isclose_box(self, other: BoundingBox, rtol: float=1e-05, atol: float=1e-08) -> bool:
        return (np.isclose(self.key.lower, other.lower, rtol, atol)
            and np.isclose(self.key.upper, other.upper, rtol, atol))
    