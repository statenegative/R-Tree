# Main file for testing.
import numpy as np

from page import Page
from r_tree import R_Tree

def main():
    #p = Page(shape=2, leaf=True)
    #p.add(np.array([0, 0]))
    #p.add(np.array([2, 2]))
    #p.add(np.array([1, 1]))
    #p.add(np.array([1, 3]))
    #print(p)

    rt = R_Tree(2, shape=2)
    rt.add(np.array([0, 0]))
    rt.add(np.array([1, 1]))
    rt.add(np.array([2, 2]))
    rt.add(np.array([3, 3]))
    print(rt)
    print(rt.root.entries[0][0])
    print(rt.root.entries[1][0])
    print(rt.root.entries[0][0].entries[0][0])
    print(rt.root.entries[1][0].entries[0][0])
    print(rt.root.entries[1][0].entries[1][0])
    rt.show2D()

if __name__ == "__main__":
    main()
