# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 14:33:04 2018

@author: carl
"""
import numpy as np
import pandas as pd
import os.path
from beamPlot import beamPlot

def isFloat(string):
    """
    Checks whether a string can be converted to a float.
    """
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
        print(" Loads")
        for i, load in enumerate(loads):
            print(str(i+1) + ". " + str(load[1]) + "N at " + str(load[0]) + "m")
        return True


def getBeam():
    """
    Asks the user for input, and then returns a new beam according to given input.
    """
    supportTypes = {"1": "both", "2": "cantilever"}
    
    #Get input for length & support, and check whether both are valid
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

def validLoads(beam, loads):
    """
    Returns all the loads that are valid for the given beam.
    """
    for load in loads:
        if load[0] >= 0 and load[0] <= beam[0]:
            yield load

def checkLoads(beam, loads):
    """
    Checks whether all loads are valid for current beam.
    """
    for load in loads:
        if load[0] < 0 or load[0] > beam[0]:
            return False
    
    return True

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
    
    result = np.array([beam[0], beam[1]])
    for load in loads:
        result = np.vstack((result, np.array([load[0], load[1]])))
        
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
                if not checkLoads(tmp, loads):
                    print("Your loads are not all valid for the new beam.")
                    print("All invalid loads will be removed.")
                    if beam != None:
                        yn = input("Do you want to save first? [y/n] ").lower()
                        if(yn == "y"):
                            saveFile(beam, loads)
                    loads = validLoads(beam, loads)
                    
                    input("Press enter to continue ");
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
                input("Press enter to continue ")
                
            elif entry == "2":
                #Make temporary values for if user inputs nonsense
                position = input("Input position [m]: ")
                if not isFloat(position) or float(position) <= 0:
                    print("You must input a positive scalar!")
                    continue
                if beam != None and float(position) >= beam[0]:
                    print("That load position is not on the beam, or on top of support!");
                    continue;
                
                force = input("Input force [N]: ")
                if not isFloat(force) or float(force) <= 0:
                    print("You must input a positive scalar!")
                    continue
                #Add load tuple if both are acceptable
                
                loads.append((float(position), float(force)))
                print("Added " + force + "N load at position " + position + "m")
                if beam == None:
                    print("Note that no beam exists; load will be removed if outside beam.")
                
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
            if beam == None:
                print("Cannot save without a valid beam.")
                continue
            saveFile(beam, loads)
        
        #Load beam and loads
        elif entry == "4":
            if beam != None:
                yn = input("Do you want to save first? [y/n] ").lower()
                if(yn == "y"):
                    saveFile(beam,loads)
            
            value = loadFile()
            if value != None:
                beam, loads = value
                print(" - Loaded data - ")
                print("Beam: " + str(beam[0]) + "m, " + beam[1] + " supported.\n");
                printLoads(loads);
                input("Press enter to continue ")
        
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
            if beam != None:
                yn = input("Do you want to save first? [y/n] ").lower()
                if(yn == "y"):
                    saveFile(beam,loads)
            
            print("Quitting")
            break

mainScript()