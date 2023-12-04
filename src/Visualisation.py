# Import all the necessary libraries in the code
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
# Defining a custom-defined function cubes
def cubesPlot(sides):
    # Creating data points for the sides
    data = np.ones(sides)
    # Creating the figure object
    fig = plt.figure(figsize=(9, 9))
    # Creating axes object to the plot
    ax = fig.add_subplot(111 , projection = '3d')
    # Plotting the figure
    ax.voxels(data, facecolors="yellow")
    # Displaying the figure
    plt.show()
# Creating the main () function
def cube(edges):
    # Defining side for the cube
    # Edges must be a list of arrays with 
    #X, Y,  Z
    sides = np.array([ 1, 2, 1 ])
    # Calling the cubes () function
    cubesPlot(sides)
# Calling the main () function

# "Scans r tree upon being called"

#values key = tuple
#values value = coordinates
    #2d or 3d data will be implied upon len of values
def getData(node):
    #I really gotta understand how to parse this tree
    if node.leaf == True:
        pass
        #return {"XYZ": "bounding box?" }

    #UHHH probably want to do this via recursion 
    #return values

def main():
    root = None #replace with root
    data = getData(root)

if __name__ == "__main__":
    main()
