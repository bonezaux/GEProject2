# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 14:33:04 2018

@author: carl
"""
from beamPlot import beamPlot
from beamIO import saveFile, loadFile

def isFloat(string):
    """
    Checks whether a string can be converted to a float.
    """
    try:
        float(string)
    except ValueError:
        return False;
    return True;


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
            if len(loads) == 0:
                print("No loads!")
        else:
            print("No beam!")
            
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
            if(beam == None):
                print("You cannot add loads to no beam!")    
                continue;
            
            print("Loads menu")
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