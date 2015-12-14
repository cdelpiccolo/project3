# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 09:37:57 2015

@author: Chiara Del Piccolo
"""

"""
Read in experimental Residual Dipolar Couplings
(RDCs), and read in alpha-carbon (Ca) and alpha-hydrogen (Ha) coordinates to calculate the
expected RDCs from a text file. Here, the example used is the substrate-free form
of arginine kinase, in phage alignment media. 
Adapated from Class 4 assignment. 12.13.15 committed
This version for Calpha-Halpha couplings, saupe matrix input. 
"""

import numpy as np
from scipy import linalg
from math import *
import csv 
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

class ResidualDipolarCouplings(object):
    """Read in experimental RDCs and calculate expected RDCs from coordinates."""
    def __init__(self, saupe_matrix, exp_rdc_file, cafile, hafile, dmax):
        self.saupe_matrix = saupe_matrix
        self.dmax = dmax
        self.exp_rdc_file = exp_rdc_file
        self.cafile = cafile
        self.hafile = hafile        
        
    def get_exp_rdcs(self):
        """Read in experimentally observed RDCs from a text file."""
        exp_rdc = np.genfromtxt(self.exp_rdc_file)
        return exp_rdc

    def get_coords(self):
        """Read in the coordinates of the alpha-carbon (Calpha) and alpha-hydrogen (Halpha) residues
           from a text file."""
        CAcoords = np.genfromtxt(self.cafile) 
        HAcoords = np.genfromtxt(self.hafile) 
       
        #slicing
        CA_residues = CAcoords[:,0] 
        CA_xcoords = CAcoords[:,1]
        CA_ycoords = CAcoords[:,2]
        CA_zcoords = CAcoords[:,3]
        
        HA_residues = HAcoords[:,0]
        HA_xcoords = HAcoords[:,1]
        HA_ycoords = HAcoords[:,2]
        HA_zcoords = HAcoords[:,3]
        
        #element-wise subtraction
        dx = CA_xcoords - HA_xcoords
        dy = CA_ycoords - HA_ycoords
        dz = CA_zcoords - HA_zcoords
        return dx, dy, dz
        
    def make_saupe_matrix(self):
        saupe = self.saupe_matrix
        sxx = saupe[0]
        syy = saupe[1]
        sxy = saupe[2]
        sxz = saupe[3]
        syz = saupe[4]
        return sxx, syy, sxy, sxz, syz

    def back_calculate_rdcs(self):
        """Back-calculate the expected RDCs."""
        dx, dy, dz = self.get_coords()
        sxx, syy, sxy, sxz, syz = self.make_saupe_matrix()
        dmax = self.dmax
        
        rdc_list = []
        for i in range(len(dx)):
            r = sqrt(dx[i] * dx[i] + dy[i] * dy[i] + dz[i] * dz[i])    
            sc1 = np.array((dx[i] * dx[i] - dz[i] * dz[i]) * dmax / r**5)
            sc2 = np.array((dy[i] * dy[i] - dz[i] * dz[i]) * dmax / r**5)
            sc3 = np.array((2 * dx[i] * dy[i]) * dmax / r**5)
            sc4 = np.array((2 * dx[i] * dz[i]) * dmax / r**5)
            sc5 = np.array((2 * dy[i] * dz[i]) * dmax / r**5)
            
            rdc = (sxx*sc1) + (syy*sc2) + (sxy*sc3) + (sxz*sc4) + (syz*sc5)
            rdc_list.append(rdc)
        rdcs = np.array(rdc_list)
        np.savetxt("calc_rdcs.csv", rdcs)
        return rdcs
 
if __name__ == "__main__":        
    x = ResidualDipolarCouplings([-2.95379276065e-06, -0.000216342464017, 0.000151739172395, -0.000386038080569, -0.000355440050948], u'apo_phage.txt', u'h.txt', u'n.txt', -60400)
    x.get_exp_rdcs()
    x.get_coords()
    x.make_saupe_matrix()
    x.back_calculate_rdcs()

