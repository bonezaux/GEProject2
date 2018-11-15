# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 14:33:04 2018

@author: carl
"""
import numpy as np
import pandas as pd
from beamPlot import beamPlot

#Apparently how you check whether something is a float in python.
def isFloat(string):
    try:
        float(string)
    except ValueError:
        return False;
    return True;

def printLoads(loads):
    """
    Prints given loads, and returns whether any actually exist.
    """
    if(len(loads) == 0):
        print("No current loads")
        return False
    else:
        for i, load in enumerate(loads):
            print(str(i+1) + ". " + str(load[1]) + "N at " + str(load[0]) + "m")
        return True


def getBeam():
    """
    Asks the user for input, and then returns a new beam according to given input.
    """
    supportTypes = {"1": "both", "2": "cantilever"}
    
    #Get input for length&support, and check whether both are valid
    length = input("Input beam length [m]: ")
    if not isFloat(length):
        print("You must input a scalar!")
        return None
    print("Support types:")
    print("1. both")
    print("2. cantilever")
    support = input("Choose support type: ")
    if support != "1" and support != "2":
        print("You must choose either 1 or 2!")
        return None
    return (float(length), supportTypes[support])

def checkLoads():
    """
    Checks whether all loads are valid for current beam.
    """
    pass

def saveFile(beam, loads):
    """
    Saves the beam and loads to a file with filename given by the user.
    Uses panda for saving to csv.
    """
    filename = input("Write file name to save file as, without extension:")
    if not filename.isalnum():
        print ("Illegal filename! Please only enter alphanumerical characters.") 
        return
    
    result = np.array([beam[0], beam[1]])
    for load in loads:
        result = np.vstack((result, np.array([load[0], load[1]])))
    print(str(pd.DataFrame(result)))
    print(pd.DataFrame(result).to_csv(index=False))
    
    with open(filename+".csv", "w") as file:
        pd.DataFrame(result).to_csv(file, index=False)

def loadFile():
    filename = input("Write file name to load from, without extension:")
    
    data = None
    with open(filename+".csv") as file:
        data = pd.read_csv(file)
    
    print(data)
    
def mainScript():
    #Beam tuple, [0] = length, [1] = supportType (string)
    beam = None
    #Contains load tuples, for which [0] = position & [1] = force
    loads = []
    
    while True:
        print(""" Menu 
1. Configure beam
2. Configure loads
3. Save beam and loads
4. Load beam and loads
5. Generate plot
6. Quit""")
        if beam != None:
            print("Current beam: " + str(beam[0]) + "m, " + beam[1] + " supported.");
            
        entry = input("Choose a menu entry: ")
        
        #Configure beam
        if entry == "1":
            tmp = getBeam()
            if(tmp != None):
                beam = tmp
        
        #Configure loads
        elif entry == "2":
            print("Beam menu")
            print("1. See current loads")
            print("2. Add a load")
            print("3. Remove a load")
            
            entry = input("Choose menu point: ")
            
            if entry == "1":
                printLoads(loads)
            elif entry == "2":
                #Make temporary values if user inputs nonsense
                position = input("Input position [m]: ")
                if not isFloat(position):
                    print("You must input a scalar!")
                    continue
                force = input("Input force [N]: ")
                if not isFloat(force):
                    print("You must input a scalar!")
                    continue
                #Add load tuple if both are acceptable
                loads.append((float(position), float(force)))
                print("Added " + force + "N load at position " + position + "m")
            elif entry == "3":
                if(printLoads(loads)):
                    toRemove = input("Load index to remove: ")
                    if not toRemove.isdecimal() or int(toRemove) < 1 or int(toRemove) > len(loads):
                        print("You have to choose a valid load!")
                        continue
                    load = loads.pop(int(toRemove)-1);
                    print("Removed " + str(load[1]) + "N at " + str(load[0]) + "m")
        
        #Save beam and loads
        elif entry == "3":
            saveFile(beam, loads)
        
        #Load beam and loads
        elif entry == "4":
            loadFile()
        
        #Plot
        elif entry == "5":
            if len(loads) == 0:
                print("No loads set!")
                continue
            if beam == None:
                print("Beam not configured!")
                continue
            loadPositions, loadForces = zip(*loads)
            beamPlot(beam[0], loadPositions, loadForces, beam[1])
        elif entry == "6":
            print("Quitting")
            break

mainScript()