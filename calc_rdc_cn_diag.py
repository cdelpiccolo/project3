# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 09:37:57 2015

@author: Chiara Del Piccolo
"""

"""
Read in experimental Residual Dipolar Couplings
(RDCs), and read in carbon (C) and nitrogen (N) coordinates to calculate the
expected RDCs from a text file.
This version for CN couplings, diagonalized matrix / euler angles input.
"""

import numpy as np
from math import *

class ResidualDipolarCouplings(object):
    """Read in experimental RDCs and calculate expected RDCs from coordinates."""
    def __init__(self, Smatrix, euler_angles, exp_rdc_file, cfile, nfile, dmax):
        self.Smatrix = Smatrix
        self.euler_angles = euler_angles
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

    def do_matrix_operations(self):
        """Construct and rotate the matrices that are needed to calculate
           the expected RDCs."""
           
        S_matrix = self.Smatrix
        euler_angles = self.euler_angles
        diag_Smatrix = np.diag(S_matrix)

        alpha_deg = euler_angles[0]
        beta_deg = euler_angles[1]
        gamma_deg = euler_angles[2]
        
        #convert to radians
        alpha = alpha_deg*(pi/180)
        beta = beta_deg*(pi/180)
        gamma = gamma_deg*(pi/180)
        
        #construct rotation matrix            
        a = cos (gamma) * cos (beta) * cos (alpha) - sin (gamma) * sin (alpha)
        b = cos (gamma) * cos (beta) * sin (alpha) + sin (gamma) * cos (alpha)
        c = -cos (gamma) * sin (beta)
        d = -sin (gamma) * cos (beta) * cos (alpha) - cos (gamma) * sin (alpha)
        e = -sin (gamma) * cos (beta) * sin (alpha) + cos (gamma) * cos (alpha)
        f = sin (gamma) * sin (beta)
        g = cos (alpha) * sin (beta)
        h = sin (alpha) * sin (beta)
        k = cos (beta)
        
        rmatrix = np.array([a,b,c,d,e,f,g,h,k], float)
        rmatrix = rmatrix.reshape((3, 3))
        
        #construct saupe matrix
        r_transpose = np.transpose(rmatrix)
        saupe_temp = np.dot(r_transpose, diag_Smatrix)
        saupe_matrix = np.dot(saupe_temp, rmatrix)             
        sxx = saupe_matrix[0,0]
        syy = saupe_matrix[1,1]
        sxy = saupe_matrix[0,1]
        sxz = saupe_matrix[0,2]
        syz = saupe_matrix[1,2]
        
        return sxx, syy, sxy, sxz, syz

    def back_calculate_rdcs(self):
        """Back-calculate the expected RDCs."""
        dx, dy, dz = self.get_coords()
        sxx, syy, sxy, sxz, syz = self.do_matrix_operations()
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
    x = ResidualDipolarCouplings([-0.000240977,-0.000429318,0.000670295], [36.9364,139.182,-118.931], u'apo_phage.csv', u'h.txt', u'n.txt', 6125)
    x.get_exp_rdcs()
    x.get_coords()
    x.do_matrix_operations()
    x.back_calculate_rdcs()
