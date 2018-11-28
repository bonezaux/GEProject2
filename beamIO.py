# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 22:03:29 2018

@author: Carl
"""
import numpy as np
import pandas as pd
import os.path

def saveFile(beam, loads):
    """
    Saves the beam and loads to a file with filename given by the user.
    Uses pandas for saving to csv.
    """
    if beam==None:
        print("Cannot save data without beam!")
        return
    
    #Get a valid filename
    while(True):
        filename = input("Write file name to save as:")
        if not filename.isalnum():
            print ("Illegal filename! Please only enter alphanumerical characters.") 
            return
        else:
            break
    
    #Create a matrix, 0th row is the beam, other rows are the loads.
    result = np.array([beam[0], beam[1]])
    for load in loads:
        result = np.vstack((result, np.array([load[0], load[1]])))
    
    #Save matrix as <filename>.csv
    with open(filename+".csv", "w") as file:
        pd.DataFrame(result).to_csv(file, index=False)
        print("Wrote data to file " + filename + ".csv")
        
def loadFile():
    """
    Loads beam and loads from a csv file, as saved by the program previously.
    Uses pandas for loading from csv.
    """
    #Get a valid filename
    while(True):
        filename = input("Write file name to load from:")
        if not filename.isalnum():
            print ("Illegal filename! Please only enter alphanumerical characters.") 
            return None
        else:
            break
    
    #Check whether it is a file
    if not os.path.isfile(filename+".csv"):
        print ("File does not exist. Notice that the program loads .csv files if you supplied your own data file.")
        return None
    
    #Load data from file
    data = None
    with open(filename+".csv") as file:
        data = pd.read_csv(file)
        data = data.values.reshape(-1, 2)
        beam = (float(data[0,0]), data[0,1])
        loads = []
        for r in data[1:,:]:
            loads.append(r.astype(float))
        print("Loaded " + filename + ".csv!");
        return (beam, loads)
    
    return None
