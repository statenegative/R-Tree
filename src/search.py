# Searches an r-tree.
import numpy as np
import numpy.typing as npt
import random
import matplotlib.pyplot as plt

from page import Page
from r_tree import R_Tree

Point = npt.NDArray

def show_search(rt: R_Tree, radius: float, origin: Point, draw_all_boxes: bool=True, draw_searched_boxes=True):
    # Perform search
    points, boxes = rt.search(radius, origin)

    # Plot search
    rt.plot2D(draw_boxes=draw_all_boxes)
    for point in points:
        plt.plot(point[0], point[1], 'go')
    if draw_searched_boxes:
        for box in boxes:
            rt.plot_box(box, color='r')
    plt.gca().add_patch(plt.Circle(origin, radius, color='b', fill=False))
    plt.show()
