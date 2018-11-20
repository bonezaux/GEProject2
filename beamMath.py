# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 14:35:43 2018

@author: carl
"""

import numpy as np

def beamDeflection(positions, beamLength, loadPosition, loadForce, beamSupport):
    """
    """
    if(beamSupport == "both"):
        #Calculate x<a & x>=a, and concatenate
        a1 = ((loadForce*(beamLength-loadPosition)*positions)/(6*200E9*0.001*beamLength)*(beamLength**2-positions**2-(beamLength-loadPosition)**2))[positions<loadPosition]
        a2 = ((loadForce*(beamLength-positions)*loadPosition)/(6*200E9*0.001*beamLength)*(beamLength**2-loadPosition**2-(beamLength-positions)**2))[positions>=loadPosition]
        return np.concatenate((a1,a2));
    elif(beamSupport == "cantilever"):
        #Calculate x<a & x>=a, and concatenate
        a1 = ((loadForce*positions**2)/(6*200E9*0.001)*(3*loadPosition-positions))[positions<loadPosition]
        a2 = ((loadForce*loadPosition**2)/(6*200E9*0.001)*(3*positions-loadPosition))[positions>=loadPosition]
        return np.concatenate((a1,a2))        

def beamSuperposition(positions, beamLength, loadPositions, loadForces, beamSupport):
    """
    Returns the deflection superposition of the loads on the given beam.
    """
    deflection = np.zeros(len(positions));
    for force, position in zip(loadForces, loadPositions):
        deflection += beamDeflection(positions, beamLength, position, force, beamSupport);
    return deflection;
