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
    
    fig, ax1 = plt.subplots()
    
    ax1.plot(np.arange(0,beamLength*1.01,beamLength/100.0),res)
    ax1.set_xlabel("Position [m]")
    ax1.set_ylabel("Deflection at point [m]")
    
    ax2 = ax1.twinx()
    ax2.plot(loadPositions, loadForces, 'ro')
    ax2.set_ylabel("Load at point [N]")
    ax2.set_ylim(0, max(loadForces)*1.05)
    
    plt.show()
