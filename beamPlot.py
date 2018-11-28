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
    
    #Print the maximum deflection in scientific notation, at a non-obtrusive location
    maxDeflection = max(res)
    textX = 0 if beamSupport == "cantilever" else beamLength/4
    textY = maxDeflection if beamSupport=="cantilever" else maxDeflection/4
    exponent = np.floor(np.log10(maxDeflection))
    plt.text(textX,textY,"Max deflection: " + str(round(maxDeflection*10**(-exponent), 2)) + "* 10^" + str(int(exponent)) +" m");
    
    
    #Make load point plot
    ax2 = ax1.twinx()
    ax2.plot(loadPositions, loadForces, 'ro')
    ax2.set_ylabel("Load at point [N]")
    ax2.set_ylim(0, max(loadForces)*1.05)
    
    plt.title("Beam Deflection")
    plt.show()
