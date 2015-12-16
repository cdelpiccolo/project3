# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 20:30:00 2015

@author: Chiara Del Piccolo
"""
"""
Construct plots that compare the experimental and back-calculated RDCs so that
possible points of dynamics can be identified.
Also, print basic statistics and possible outliers.
"""

import math
import numpy as np
import pandas as pd
import seaborn as sns
import logging

class Pandas(object):
    """Calculate the Qfactor for the experimental and back-calculated RDCs."""   
    
    def __init__(self):
        pass
    
    def edit_csv(self):
        """Edit csv files so that they are compatible with pandas."""
        with open('exp_rdcs.csv') as infile:
          with open('exp_rdcs2.csv', 'w') as outfile:
            for line in infile:
              fields = line.split(' ')
              outfile.write(', '.join(fields))
        
        df = pd.read_csv('exp_rdcs2.csv')
        df.columns = 'Residue Number', 'Experimental RDC'
        df.to_csv('exp_rdcs3.csv')
        
        df2 = pd.read_csv('calc_rdcs.csv')
        df2.columns = ['Back-Calculated RDC']
        df2.to_csv('calc_rdcs2.csv')
     
    def get_exp_rdcs(self):
        """Read in experimentally observed RDCs and the associated residue numbers
           from a csv file and construct a pandas DataFrame."""
        exp_df = pd.read_csv('exp_rdcs3.csv')
        logging.info('%s %s' % ('Number of experimental RDCs:', len(exp_df)))
        return exp_df
        
    def get_calc_rdcs(self):
        """Read in back-calculated RDCs from a csv file
           and construct a pandas dataframe."""
        calc_df = pd.read_csv('calc_rdcs2.csv')
        logging.info('%s %s' % ('Number of calculated RDCs:', len(calc_df)))
        return calc_df
        
    def make_rdc_df(self):
        """Concatenate the experimental and back-calculated RDCs into a single DataFrame."""
        exp_df = self.get_exp_rdcs()
        calc_df = self.get_calc_rdcs()
        exp_df = pd.DataFrame(exp_df, columns=['Residue Number', 'Experimental RDC'])
        calc_df = pd.DataFrame(calc_df, columns=['Back-Calculated RDC'])
        rdc_df = pd.concat([exp_df, calc_df], axis=1)
        return rdc_df
        
    def manip_rdc_df(self):
        """Manipulate the rdc dataframe using methods in pandas."""
        rdc_df = self.make_rdc_df()
        basic_stats = rdc_df.describe()
        print basic_stats
        filter_outliers = rdc_df[abs(rdc_df['Experimental RDC']) > 20]  #possible outliers     
        filter_outliers = pd.DataFrame.dropna(filter_outliers, subset=['Experimental RDC', 'Back-Calculated RDC'])
        print "Possible outliers: ", filter_outliers
        
        exp_rdc_plot = sns.jointplot(x="Residue Number", y="Experimental RDC", data=rdc_df)
        print exp_rdc_plot
        pairplot = sns.pairplot(rdc_df, vars=['Experimental RDC', 'Back-Calculated RDC'])
        print pairplot
   
if __name__ == "__main__":
    x = Pandas()
    x.edit_csv()
    x.manip_rdc_df()