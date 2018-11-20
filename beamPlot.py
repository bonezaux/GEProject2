# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 14:36:52 2018

@author: carl
"""

import numpy as np
import matplotlib.pyplot as plt

from beamMath import beamSuperposition

def beamPlot(beamLength,loadPositions,loadForces,beamSupport):
    """
    Plots a plot for the given beam with the given loads
    """
    res = beamSuperposition(np.arange(0,beamLength*1.01,beamLength/100.0), beamLength, loadPositions, loadForces, beamSupport)
    #TODO: FIX PLOT TITLE
    
    #Get subplots to make two y-axes for one graph
    fig, ax1 = plt.subplots()
    
    #Make position line plot
    ax1.plot(np.arange(0,beamLength*1.01,beamLength/100.0),res)
    ax1.set_xlabel("Position [m]")
    ax1.set_ylabel("Deflection at point [m]")
    ax1.invert_yaxis()
    
    maxdef = max(res)
    print(maxdef)
    exponent = np.floor(np.log10(maxdef))
    plt.text(0,maxdef,"Max deflection: " + str(round(max(res)*10**(-exponent), 2)) + "E" + str(int(exponent)) +" m");
    
    
    #Make load point plot
    ax2 = ax1.twinx()
    ax2.plot(loadPositions, loadForces, 'ro')
    ax2.set_ylabel("Load at point [N]")
    ax2.set_ylim(0, max(loadForces)*1.05)
    
    plt.title("Beam Deflection")
    plt.show()
