# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 09:37:57 2015

@author: Chiara Del Piccolo
"""

"""
Read in experimental Residual Dipolar Couplings
(RDCs), and read in carbon (C) and nitrogen (N) coordinates to calculate the
expected RDCs from a text file.
This version for CN couplings, saupe matrix input. 
"""

import numpy as np
from math import *

class ResidualDipolarCouplings(object):
    """Read in experimental RDCs and calculate expected RDCs from coordinates."""
    def __init__(self, saupe_matrix, exp_rdc_file, cfile, nfile, dmax):
        self.saupe_matrix = saupe_matrix
        self.dmax = dmax
        self.exp_rdc_file = exp_rdc_file
        self.cfile = cfile
        self.nfile = nfile        
        
    def get_exp_rdcs(self):
        """Read in experimentally observed RDCs from a text file."""
        exp_rdc = np.genfromtxt(self.exp_rdc_file)
        return exp_rdc

    def get_coords(self):
        """Read in the coordinates of the carbon (C) and nitrogen (N) residues
           from a text file."""
        Ccoords = np.genfromtxt(self.cfile) 
        Ncoords = np.genfromtxt(self.nfile) 
       
        #slicing
        C_residues = Ccoords[:,0] 
        C_xcoords = Ccoords[:,1]
        C_ycoords = Ccoords[:,2]
        C_zcoords = Ccoords[:,3]
        
        N_residues = Ncoords[:,0]
        N_xcoords = Ncoords[:,1]
        N_ycoords = Ncoords[:,2]
        N_zcoords = Ncoords[:,3]
        
        #element-wise subtraction
        dx = C_xcoords - N_xcoords
        dy = C_ycoords - N_ycoords
        dz = C_zcoords - N_zcoords
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
    x = ResidualDipolarCouplings([-2.95379276065e-06, -0.000216342464017, 0.000151739172395, -0.000386038080569, -0.000355440050948], u'apo_phage.txt', u'h.txt', u'n.txt', 6125)
    x.get_exp_rdcs()
    x.get_coords()
    x.make_saupe_matrix()
    x.back_calculate_rdcs()

