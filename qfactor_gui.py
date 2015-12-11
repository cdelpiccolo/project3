# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 19:47:44 2015

@author: Chiara Del Piccolo
"""

#def qfactor(self):
#    rdczip = zip(exp_rdc, rdc_calc)
#    diff_list = []
#    for t in rdczip:
#        diff = t[0] - t[1]
#        diff_list.append(diff)
#    sqdiff = square(diff_list)
#    numerator = sum(sqdiff)
#    sqobs = square(rdc_obs)
#    denominator = sum(sqobs)
#    Q = sqrt(numerator / denominator)
#    Q = N.around(Q, 6)
#    print 'Q:', Q
#    return Q

import math
import numpy as np
import csv


class Qfactor(object):
    """Calculate the Qfactor for the experimental and back-calculated RDCs."""
    
    def __init__(self):
        pass
    
    def get_rdcs(self):
        """Get experimental and back-calculated RDCs."""
        exp_rdcs = np.genfromtxt('exp_rdcs.csv')
        exp_rdcs = exp_rdcs[:,1]
        #print len(exp_rdcs)
        calc_rdcs = np.genfromtxt('calc_rdcs.csv')
        #print len(calc_rdcs)
        return exp_rdcs, calc_rdcs
    
    def qfactor(self):
        exp_rdcs, calc_rdcs = self.get_rdcs()
        rdczip = zip(exp_rdcs, calc_rdcs)
        diff_list = []
        for t in rdczip:
            diff = t[0] - t[1]
            diff_list.append(diff)
        sqdiff = np.square(diff_list)
        numerator = sum(sqdiff)
        sqobs = np.square(exp_rdcs)
        denominator = sum(sqobs)
        Q = math.sqrt(numerator / denominator)
        Q = np.around(Q, 6)
        print 'Q:', Q
        return Q
        
        
if __name__ == "__main__":
    x = Qfactor()
    x.qfactor()