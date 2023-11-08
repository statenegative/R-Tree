# R tree page data structure
import numpy as np
import numpy.typing as npt
import typing

class page:
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
    # key: The position of the entry.
    # data: The data associated with the entry.
    def insert(self, key: npt.ArrayLike, data: typing.Any):
        # Convert key into np.ndarray
        if not isinstance(key, np.ndarray):
            key = np.array(key)

        # Check key shape
        if key.shape != self.shape:
            raise ValueError(f"Shape mismatch: key {key} has shape {key.shape}, but page holds keys of shape {self.shape}.")
        
        # Add to entries list
        self.entries.append((key, data))

        # Update bounding box
        self.min = np.minimum(self.min, key)
        self.max = np.maximum(self.max, key)
    
    # Inserts an entry into this page.
    #
    # key: The position of the entry.
    # data: The data associated with the entry.
    def __setitem__(self, key: npt.ArrayLike, data: typing.Any):
        self.insert(key, data)

    # Checks whether this page contains a key.
    #
    # key: The key to check.
    def __contains__(self, key: npt.ArrayLike) -> bool:
        # Convert key into np.ndarray
        if not isinstance(key, np.ndarray):
            key = np.array(key)

        # Search list for key
        for entry in self.entries:
            if np.isclose(entry[0], key):
                return True
        return False

    # Deletes an entry from this page.
    #
    # key: The entry to delete.
    def delete(self, key: npt.ArrayLike):
        # Convert key into  np.ndarray
        if not isinstance(key, np.ndarray):
            key = np.array(key)

        # Find key in entries list
        found = False
        for i in range(len(self.entries)):
            entry = self.entries[i][0]
            if np.isclose(entry, key):
                found = True
                break
        
        # Handle if entry wasn't found
        if not found:
            raise KeyError(f"Key {key} not found in page.")
        
        # Remove entry
        del a[i]
        # Update bounding box
        self.__recompute_bounds()

    def __delitem__(self, key: npt.ArrayLike):
        self.delete(key)
    
    # Creates a string representation of this page.
    def __str__(self) -> str:
        return str(self.entries)

    # Recomputes this page's bounding box.
    def __recompute_bounds(self):
        self.__recompute_min()
        self.__recompute_max()
    
    # Recomputes this page's minimum bounds.
    def __recompute_min(self):
        self.min.fill(np.inf)
        for entry in self.entries:
            self.min = np.minimum(self.min, entry)

    # Recomputes this page's maximum bounds.
    def __recompute_max(self):
        self.max.fill(-np.inf)
        for entry in self.entries:
            self.max = np.maximum(self.max, entry)
