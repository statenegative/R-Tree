# Main file for testing.
import numpy as np
import random
from page import Page
from r_tree import R_Tree
import search
import matplotlib.pyplot as plt
import os

def main():
    
    path = os.getcwd() + "\data_sets\\"
    Hospital = False
    while True:
        user = input("Select a dataset(select 1-3): 1. Charging Stations 2. Charging Stations Random 3. Hospitals: ")
        if user == '1':
            file = open(path + "Charging_Station",  errors="ignore")
            break
        if user == '2':
            file = open(path + "Charging_StationR",  errors="ignore")
            break
        if user == '3':
            file = open(path + "Hospitals",  errors="ignore")
            Hospital = True
            break
    
    
    en = {attr: i for i, attr in enumerate((file.readline().strip().split(",")))}
    x = en["X"]
    y = en["Y"]
    
    name = en.get("NAME")

   
    
    read = file.readlines()
    
    #creates an R tree of size 
    if Hospital:
        bb = input("Select how many nodes can be in a bounding box(Recommended 5-15): ")
    else:
        bb = input("Select how many nodes can be in a bounding box(Recommended 25-100): ")
    rt = R_Tree(int(bb), shape=2)
    counter = 0
    for r in read:
        print("Adding node " + str(counter) + " out of " + str(len(read)-1))
        attr = r.split(",")
        try:
            rt.add(np.array([attr[x], attr[y]],dtype = np.float64), attr[name])
        except:
            pass
        counter+=1

    
    
    
    while True:
        user = input("Select how to display the data(1-3) or q to exit:\n 1. Visualize the R-tree\n 2. Visualize the R-tree and search within a radius, showing only bounding boxes used to locate nodes within radius\n 3. Visualize the R-tree and show all bounding boxes:" )
        if user == "1":

            rt.plot2D()
            plt.show()

        if user == "2":
            if Hospital:
                search.show_search(rt,100000, np.array([-13448630.8033,5751579.6696 ]), False, True)
        
            else:
                search.show_search(rt,1, np.array([-122.47792210417252, 47.26152376395718]), False, True)
    
        if user == "3":
            if Hospital:
                search.show_search(rt,100000, np.array([-13448630.8033,5751579.6696 ]), True, True)
        
            else:
                search.show_search(rt,1, np.array([-122.47792210417252, 47.26152376395718]), True, True)
        if user == "q":
            exit(1)
    
if __name__ == "__main__":

    main()

