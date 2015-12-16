# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 21:59:53 2015

@author: Chiara Del Piccolo
"""
"""
CS 506 Final Project.
This program implements a simple GUI interface that accepts user inputs and 
uses them to calculate the expected RDCs and the Qfactor. 
The user inputs and the results of the calculations will be output to a 
log file called "final_log_TIME_DATE". 
The program will then construct plots to compare individual experimental 
and calculated RDCS  in order to identify possible points of protein dynamics.

EXAMPLE RUN:
Runs the program for NH Coupling data collected for the apo form of arginine
kinase in phage media.

Choose NH Coupling.
Choose Dmax = 21700
Choose diagonalized matrix / Euler angle input.
Diagonalized_matrix values: -0.000240977,-0.000429318,0.000670295 
Euler_angle values: 36.93, 139.18,-118.93
Experimental RDC File: apo_phage.csv
H coordinates file: h.txt
N coordinates file: n.txt 
"""

import numpy as np
import scipy as sp
from math import *
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPushButton
import calc_rdc_dmax1_diag
import calc_rdc_dmax1_saupe
import calc_rdc_dmax2_diag
import calc_rdc_dmax2_saupe
import calc_rdc_cn_diag
import calc_rdc_cn_saupe
import calc_rdc_caha_saupe
import calc_rdc_caha_diag
import qfactor_gui
import pandas_gui
import logging
import datetime as dt

log_filename = dt.datetime.now().strftime('log_%H_%M_%d_%m_%Y.txt')
log_filename_final = dt.datetime.now().strftime('final_log_%H_%M_%d_%m_%Y.txt')
logging.basicConfig(filename=log_filename, level=logging.INFO)

class IntroWindow(QtGui.QMainWindow):
    """Greet the user, ask the user to enter the application."""
    def __init__(self):
        super(IntroWindow, self).__init__()
        self.setWindowTitle("Welcome")
        self.setGeometry(50, 50, 400, 150)
        self.entry_button()
        
    def create_win(self):
        """Create window to ask the user which type of coupling to input."""
        self.win = CouplingWindow()
     
    def entry_button(self):
        """Make a button for the user to click to enter the application."""
        entry_btn = QtGui.QPushButton("Welcome to the RDC Analysis Tool. \n Click here to enter the application.", self)
        entry_btn.resize(300, 40)
        entry_btn.move(50, 50)
        entry_btn.clicked.connect(self.create_win)
        self.show() 
        
class CouplingWindow(QtGui.QMainWindow):
    """Ask the user to input the coupling type."""
    def __init__(self):
        super(CouplingWindow, self).__init__()
        self.setWindowTitle("Choose coupling type:")
        self.setGeometry(50, 50, 500, 200) 
        self.coupling_buttons()
        
    def create_nh_win(self):
        """Create a window for NH couplings."""
        self.nhwin = NH_Dmax_Window()
    
    def create_cn_win(self):
        """Create a window for CN couplings."""
        self.cnwin = CN_Matrix_Window()  
        
    def create_caha_win(self):
        """Create a window for Calpha-Halpha couplings."""
        self.cahawin = CaHa_Matrix_Window() 
        
    def coupling_buttons(self):
        """Prompt the user to select the coupling type for the experiment."""   
        nh_btn = QtGui.QPushButton("Nitrogen-Hydrogen (NH) Coupling", self)
        nh_btn.clicked.connect(self.create_nh_win) 
        nh_btn.resize(200, 20)
        nh_btn.move(150, 50)
        
        cn_btn = QtGui.QPushButton("Carbon-Nitrogen (CN) Coupling", self)
        cn_btn.clicked.connect(self.create_cn_win) #next window class
        cn_btn.resize(200, 20)
        cn_btn.move(150, 100)
        
        caha_btn = QtGui.QPushButton("Calpha-Halpha (CaHa) Coupling", self)
        caha_btn.clicked.connect(self.create_caha_win)  #next window class
        caha_btn.resize(200, 20)
        caha_btn.move(150, 150)
        
        self.show()
        
class NH_Dmax_Window(QtGui.QMainWindow):
    """Choose the scaling factor (Dmax) for NH Couplings."""
    def __init__(self):
        super(NH_Dmax_Window, self).__init__()
        self.setWindowTitle("Choose scaling factor:")
        self.setGeometry(50, 50, 500, 200)
        self.dmax_buttons()
        
    def create_dmax1_win(self):
        """Create a window for Dmax = 21700."""
        self.dmax1win = Dmax1_Window() 
        
    def create_dmax2_win(self):
        """Create a window for Dmax = 24850."""
        self.dmax2win = Dmax2_Window()
        
    def dmax_buttons(self):
        "Prompt the user to choose the scaling factor (Dmax) for the calculations."""    
        dmax1_btn = QtGui.QPushButton("Dmax = 21700", self)
        dmax1_btn.clicked.connect(self.create_dmax1_win) 
        dmax1_btn.resize(200, 20)
        dmax1_btn.move(150, 50)
        
        dmax2_btn = QtGui.QPushButton("Dmax = 24850", self)
        dmax2_btn.clicked.connect(self.create_dmax2_win) #next window class 
        dmax2_btn.resize(200, 20)
        dmax2_btn.move(150, 100)
        
        self.show()

class CN_Matrix_Window(QtGui.QMainWindow):
    """Choose which matrix to use for CN Couplings."""
    def __init__(self):
        super(CN_Matrix_Window, self).__init__()
        self.setWindowTitle("Choose matrix to input:")
        self.setGeometry(50, 50, 500, 200)
        self.matrix_buttons()
    
    def create_cn_saupe_win1(self):
        """Create a window for saupe matrix input for CN couplings."""
        self.cnsaupe = CN_Saupe_Window()
       
    def create_cn_diag_win1(self):
        """Create a window for diagonalized matrix and Euler angles inputs for\
        CN couplings."""
        self.cndiag = CN_Diag_Window()
        
    def matrix_buttons(self):
        """Prompt the user to choose whether to input the saupe matrix or the \
        diagonalized matrix and Euler angles."""    
        saupe_btn = QtGui.QPushButton("Input saupe matrix", self)
        saupe_btn.clicked.connect(self.create_cn_saupe_win1)
        saupe_btn.resize(200, 20)
        saupe_btn.move(150, 50)
        
        diag_btn = QtGui.QPushButton("Input diagonalized matrix and Euler angles", self)
        diag_btn.clicked.connect(self.create_cn_diag_win1) #next window class
        diag_btn.resize(300, 20)
        diag_btn.move(100, 100)
        
        self.show()
        
class CaHa_Matrix_Window(QtGui.QMainWindow):
    """Choose which matrix to use for Calpha-Halpha Couplings."""
    
    def __init__(self):
        super(CaHa_Matrix_Window, self).__init__()
        self.setWindowTitle("Choose matrix to input:")
        self.setGeometry(50, 50, 500, 200)
        self.matrix_buttons()
        
    def create_caha_saupe_win1(self):
        """Create a window for saupe matrix input for Calpha-Halpha couplings."""
        self.cahasaupe = CaHa_Saupe_Window()
       
    def create_caha_diag_win1(self):
        """Create a window for diagonalized matrix and Euler angles input for\
        Calpha-Halpha couplings."""
        self.cahadiag = CaHa_Diag_Window()
        
    def matrix_buttons(self):
        """Prompt the user to choose whether to input the saupe matrix or the \
        diagonalized matrix and Euler angles."""    
        saupe_btn = QtGui.QPushButton("Input saupe matrix", self)
        saupe_btn.clicked.connect(self.create_caha_saupe_win1)
        saupe_btn.resize(200, 20)
        saupe_btn.move(150, 50)
        
        diag_btn = QtGui.QPushButton("Input diagonalized matrix and Euler angles", self)
        diag_btn.clicked.connect(self.create_caha_diag_win1) 
        diag_btn.resize(300, 20)
        diag_btn.move(100, 100)
        
        self.show()
        
class Dmax1_Window(QtGui.QMainWindow):
    """After the user chooses Dmax=21700 for the scaling factor, \
    prompt the user to choose whether to input the saupe matrix \
    or the diagonalized matrix and Euler angles."""
    
    def __init__(self):
        super(Dmax1_Window, self).__init__()
        self.setWindowTitle("Choose matrix to input:")
        self.setGeometry(50, 50, 500, 200)
        self.matrix_buttons()
        
    def create_dmax1_saupe_win1(self):
        """Create a window for saupe matrix input for NH couplings, where\
        Dmax = 21700."""
        self.dmax1saupe = Dmax1_Saupe_Window()
       
    def create_dmax1_diag_win1(self):
        """Create a window for diagonalized matrix and Euler angles input for\
        NH couplings, where Dmax = 21700."""
        self.dmax1diag = Dmax1_Diag_Window()
                
    def matrix_buttons(self):
        """Prompt the user to choose whether to input the saupe matrix or the \
        diagonalized matrix and Euler angles."""    
        saupe_btn = QtGui.QPushButton("Input saupe matrix", self)
        saupe_btn.clicked.connect(self.create_dmax1_saupe_win1)
        saupe_btn.resize(200, 20)
        saupe_btn.move(150, 50)
        
        diag_btn = QtGui.QPushButton("Input diagonalized matrix and Euler angles", self)
        diag_btn.clicked.connect(self.create_dmax1_diag_win1)
        diag_btn.resize(300, 20)
        diag_btn.move(100, 100)
        
        self.show()
        
class Dmax2_Window(QtGui.QMainWindow):
    """After the user chooses Dmax=21700 for the scaling factor, \
    prompt the user to choose whether to input the saupe matrix \
    or the diagonalized matrix and Euler angles."""
    
    def __init__(self):
        super(Dmax2_Window, self).__init__()
        self.setWindowTitle("Choose matrix to input:")
        self.setGeometry(50, 50, 500, 200)
        self.matrix_buttons()
    
    def create_dmax2_saupe_win1(self):
        """Create a window for saupe matrix input for NH couplings, where Dmax = 21700."""
        self.dmax2saupe = Dmax2_Saupe_Window()
    
    def create_dmax2_diag_win1(self):
        """Create a window for diagonalized matrix and Euler angles input for\
        NH couplings, where Dmax = 21700."""
        self.dmax2diag = Dmax2_Diag_Window()
        
    def matrix_buttons(self):
        """Prompt the user to choose whether to input the saupe matrix or the \
        diagonalized matrix and Euler angles."""    
        saupe_btn = QtGui.QPushButton("Input saupe matrix", self)
        saupe_btn.clicked.connect(self.create_dmax2_saupe_win1)
        saupe_btn.resize(200, 20)
        saupe_btn.move(150, 50)
        
        diag_btn = QtGui.QPushButton("Input diagonalized matrix and Euler angles", self)
        diag_btn.clicked.connect(self.create_dmax2_diag_win1)
        diag_btn.resize(300, 20)
        diag_btn.move(100, 100)
        
        self.show()
        
class Dmax1_Saupe_Window(QtGui.QWidget):
    """Prompt the user to input the values of the Saupe matrix."""    
    
    def __init__(self):
        super(Dmax1_Saupe_Window, self).__init__()
        self.make_saupewin1()
        self.make_saupewin2()
        self.make_saupewin3()
        self.make_saupewin4()
        self.make_saupewin5()
        self.make_expRDC_file_win()
        self.make_hcoords_file_win()
        self.make_ncoords_file_win()
        self.run_rdc_calc()
        self.run_pandas()
  
    global saupe_list 
    saupe_list = []    
    global diag_list
    diag_list = [] 
    global params_list 
    params_list = []
    
    def make_saupewin1(self):
        sxx, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 1', 
                                           'Enter sxx:', decimals = 10)        
        if ok:
            saupe_list.append(sxx)
            
    def make_saupewin2(self):
        syy, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 2', 
                                           'Enter syy:', decimals = 10)
        if ok:
            saupe_list.append(syy)
            
    def make_saupewin3(self):
        sxy, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 3', 
                                           'Enter sxy:', decimals = 10)        
        if ok:
            saupe_list.append(sxy)
    
    def make_saupewin4(self):
        sxz, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 4', 
                                           'Enter sxz:', decimals = 10)
        if ok:
            saupe_list.append(sxz)
            
    def make_saupewin5(self):
        syz, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 5', 
                                           'Enter syz:', decimals = 10)
        if ok:
            saupe_list.append(syz)
            params_list.append(saupe_list)
        logging.info('%s %s' % ('Saupe Matrix:', saupe_list))
        
    def make_expRDC_file_win(self):
        expRDCfile, ok = QtGui.QInputDialog.getText(self, 'Experimental RDC file',
                                                    'Enter the name of the experimental RDC file.')
        if ok:
            logging.info('%s %s' % ('Experimental RDC file:', expRDCfile))
            params_list.append(expRDCfile)
            exp_rdcs = np.genfromtxt(expRDCfile)
            np.savetxt("exp_rdcs.csv", exp_rdcs)
    
    def make_hcoords_file_win(self):
        hcoords_file, ok = QtGui.QInputDialog.getText(self, 'H coordinates file', 
                                                      'Enter the name of the file containing the H coordinates.')
        if ok:
            logging.info('%s %s' % ('Hydrogen coordinates file:', hcoords_file))
            params_list.append(hcoords_file)
    
    def make_ncoords_file_win(self):
        ncoords_file, ok = QtGui.QInputDialog.getText(self, 'N coordinates file', 
                                                      'Enter the name of the file containing the N coordinates.')
        if ok:
            logging.info('%s %s' % ('Nitrogen coordinates file:', ncoords_file))
            params_list.append(ncoords_file)
            params_list.append(21700)
            logging.info('Dmax = 21700')
    
    def run_rdc_calc(self):
        """Back-calculate the RDCs and calculate the Qfactor."""
        rdcrun = calc_rdc_dmax1_saupe.ResidualDipolarCouplings(params_list[0], params_list[1], params_list[2], params_list[3], params_list[4])
        rdcrun.get_exp_rdcs()
        rdcrun.get_coords()
        rdcrun.back_calculate_rdcs()
        qcalc = qfactor_gui.Qfactor()
        qcalc.qfactor()
    
    def run_pandas(self):
        """Show the plots that compare the experimental and back-calculated\
        RDCs, and identify possible points of dynamics."""
        pandasrun = pandas_gui.Pandas()
        pandasrun.edit_csv()
        pandasrun.manip_rdc_df()
        pandasrun.edit_logfile()
            
class Dmax1_Diag_Window(QtGui.QWidget):
    """Prompt the user to input the values of the Saupe matrix."""
    def __init__(self):
        super(Dmax1_Diag_Window, self).__init__()
        self.make_diagwin1()
        self.make_diagwin2()
        self.make_diagwin3()
        self.make_eulerwin1()
        self.make_eulerwin2()
        self.make_eulerwin3()
        self.make_expRDC_file_win()
        self.make_hcoords_file_win()
        self.make_ncoords_file_win()
        self.run_rdc_calc()
        self.run_pandas()
        
    global diag_list
    diag_list = []
    global euler_list
    euler_list = []
    global params_list
    params_list = []
    
    def make_diagwin1(self):
        Sxx, ok = QtGui.QInputDialog.getDouble(self, 'Diagonalized Matrix Input 1',
                                               'Enter Sxx:', decimals = 10)
        if ok:
            diag_list.append(Sxx)
            
    def make_diagwin2(self):
        Syy, ok = QtGui.QInputDialog.getDouble(self, 'Diagonalized Matrix Input 2',
                                               'Enter Syy:', decimals = 10)
        if ok:
            diag_list.append(Syy)
            
    def make_diagwin3(self):
        Szz, ok = QtGui.QInputDialog.getDouble(self, 'Diagonalized Matrix Input 3',
                                               'Enter Szz:', decimals = 10)
        if ok:
            diag_list.append(Szz)
        logging.info('%s %s' % ('Diagonalized matrix:', diag_list))
        params_list.append(diag_list)        
        
    def make_eulerwin1(self):
        alpha, ok = QtGui.QInputDialog.getDouble(self, 'Euler Angle alpha', 
                                                 'Enter alpha (in degrees)', decimals = 2)
        if ok:
            euler_list.append(alpha)
        
    def make_eulerwin2(self):
        beta, ok = QtGui.QInputDialog.getDouble(self, 'Euler Angle beta', 
                                                 'Enter beta (in degrees)', decimals = 2)                                  
        if ok:
            euler_list.append(beta)
                                        
    def make_eulerwin3(self):
        gamma, ok = QtGui.QInputDialog.getDouble(self, 'Euler Angle gamma', 
                                                 'Enter gamma (in degrees)', decimals = 2)
        if ok:
            euler_list.append(gamma)
        logging.info('%s %s' % ('Euler angles:', euler_list))
        params_list.append(euler_list)
    
    def make_expRDC_file_win(self):
        expRDCfile, ok = QtGui.QInputDialog.getText(self, 'Experimental RDC file',
                                                    'Enter the name of the experimental RDC file.')
        if ok:
            logging.info('%s %s' % ('Experimental RDC file:', expRDCfile))
            params_list.append(expRDCfile)
            exp_rdcs = np.genfromtxt(expRDCfile)
            np.savetxt("exp_rdcs.csv", exp_rdcs)
    
    def make_hcoords_file_win(self):
        hcoords_file, ok = QtGui.QInputDialog.getText(self, 'H coordinates file', 
                                                      'Enter the name of the file containing the H coordinates.')
        if ok:
            logging.info('%s %s' % ('Hydrogen coordinates file:', hcoords_file))
            params_list.append(hcoords_file)
    
    def make_ncoords_file_win(self):
        ncoords_file, ok = QtGui.QInputDialog.getText(self, 'N coordinates file', 
                                                      'Enter the name of the file containing the N coordinates.')
        if ok:
            logging.info('%s %s' % ('Nitrogen coordinates file:', ncoords_file)) 
            params_list.append(ncoords_file)
            params_list.append(21700) 
            logging.info('Dmax = 21700')

    def run_rdc_calc(self):
        """Back-calculate the RDCs and calculate the Qfactor."""
        rdcrun = calc_rdc_dmax1_diag.ResidualDipolarCouplings(params_list[0], params_list[1], params_list[2], params_list[3], params_list[4], params_list[5])
        rdcrun.get_exp_rdcs()
        rdcrun.get_coords()
        rdcrun.do_matrix_operations()
        rdcrun.back_calculate_rdcs()
        qcalc = qfactor_gui.Qfactor()
        qcalc.qfactor()
    
    def run_pandas(self):
        pandasrun = pandas_gui.Pandas()
        pandasrun.edit_csv()
        pandasrun.manip_rdc_df()
        pandasrun.edit_logfile()
            
class Dmax2_Saupe_Window(QtGui.QWidget):
    """Prompt the user to input the values of the Saupe matrix."""
    def __init__(self):
        super(Dmax2_Saupe_Window, self).__init__()
        self.make_saupewin1()
        self.make_saupewin2()
        self.make_saupewin3()
        self.make_saupewin4()
        self.make_saupewin5()
        self.make_expRDC_file_win()
        self.make_hcoords_file_win()
        self.make_ncoords_file_win()
        self.run_rdc_calc()
        self.run_pandas()
   
    global saupe_list 
    saupe_list = []    
    global params_list
    params_list = []    
    
    def make_saupewin1(self):
        sxx, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 1', 
                                           'Enter sxx:', decimals = 10)                                          
        if ok:
            saupe_list.append(sxx)
    
    def make_saupewin2(self):
        syy, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 2', 
                                           'Enter syy:', decimals = 10)
        if ok:
            saupe_list.append(syy)
            
    def make_saupewin3(self):
        sxy, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 3', 
                                           'Enter sxy:', decimals = 10)        
        if ok:
            saupe_list.append(sxy)
    
    def make_saupewin4(self):
        sxz, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 4', 
                                           'Enter sxz:', decimals = 10)
        if ok:
            saupe_list.append(sxz)
            
    def make_saupewin5(self):
        syz, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 5', 
                                           'Enter syz:', decimals = 10)
        if ok:
            saupe_list.append(syz)
            params_list.append(saupe_list)
        logging.info('%s %s' % ('Saupe matrix:', saupe_list))  
        
    def make_expRDC_file_win(self):
        expRDCfile, ok = QtGui.QInputDialog.getText(self, 'Experimental RDC file',
                                                    'Enter the name of the experimental RDC file.')
        if ok:
            logging.info('%s %s' % ('Experimental RDC file:', expRDCfile))
            params_list.append(expRDCfile)
            exp_rdcs = np.genfromtxt(expRDCfile)
            np.savetxt("exp_rdcs.csv", exp_rdcs)
    
    def make_hcoords_file_win(self):
        hcoords_file, ok = QtGui.QInputDialog.getText(self, 'H coordinates file', 
                                                      'Enter the name of the file containing the H coordinates.')
        if ok:
            logging.info('%s %s' % ('Hydrogen coordinates file:', hcoords_file))
            params_list.append(hcoords_file)
    
    def make_ncoords_file_win(self):
        ncoords_file, ok = QtGui.QInputDialog.getText(self, 'N coordinates file', 
                                                      'Enter the name of the file containing the N coordinates.')
        if ok:
            logging.info('%s %s' % ('Nitrogen coordinates file:', ncoords_file)) 
            params_list.append(ncoords_file)
            params_list.append(24850)
    
    def run_rdc_calc(self):
        rdcrun = calc_rdc_dmax2_saupe.ResidualDipolarCouplings(params_list[0], params_list[1], params_list[2], params_list[3], params_list[4])
        rdcrun.get_exp_rdcs()
        rdcrun.get_coords()
        rdcrun.back_calculate_rdcs()
        qcalc = qfactor_gui.Qfactor()
        qcalc.qfactor()
        
    def run_pandas(self):
        pandasrun = pandas_gui.Pandas()
        pandasrun.edit_csv()
        pandasrun.manip_rdc_df()
        pandasrun.edit_logfile()
        
class Dmax2_Diag_Window(QtGui.QWidget):
    """Prompt the user to input the values of the Saupe matrix."""
    def __init__(self):
        super(Dmax2_Diag_Window, self).__init__()
        self.make_diagwin1()
        self.make_diagwin2()
        self.make_diagwin3()
        self.make_eulerwin1()
        self.make_eulerwin2()
        self.make_eulerwin3()
        self.make_expRDC_file_win()
        self.make_hcoords_file_win()
        self.make_ncoords_file_win()
        self.run_rdc_calc()
        self.run_pandas()
        
    global diag_list
    diag_list = []
    global euler_list
    euler_list = []
    global params_list
    params_list = []
    
    def make_diagwin1(self):
        Sxx, ok = QtGui.QInputDialog.getDouble(self, 'Diagonalized Matrix Input 1',
                                               'Enter Sxx:', decimals = 10)
        if ok:
            diag_list.append(Sxx)
            
    def make_diagwin2(self):
        Syy, ok = QtGui.QInputDialog.getDouble(self, 'Diagonalized Matrix Input 2',
                                               'Enter Syy:', decimals = 10)
        if ok:
            diag_list.append(Syy)
            
    def make_diagwin3(self):
        Szz, ok = QtGui.QInputDialog.getDouble(self, 'Diagonalized Matrix Input 3',
                                               'Enter Szz:', decimals = 10)
        if ok:
            diag_list.append(Szz)
        logging.info('%s %s' % ('Diagonalized matrix:', diag_list))
        params_list.append(diag_list)        
        
    def make_eulerwin1(self):
        alpha, ok = QtGui.QInputDialog.getDouble(self, 'Euler Angle alpha', 
                                                 'Enter alpha (in degrees)', decimals = 2)
        if ok:
            euler_list.append(alpha)
        
    def make_eulerwin2(self):
        beta, ok = QtGui.QInputDialog.getDouble(self, 'Euler Angle beta', 
                                                 'Enter beta (in degrees)', decimals = 2)                                  
        if ok:
            euler_list.append(beta)
                                        
    def make_eulerwin3(self):
        gamma, ok = QtGui.QInputDialog.getDouble(self, 'Euler Angle gamma', 
                                                 'Enter gamma (in degrees)', decimals = 2)
        if ok:
            euler_list.append(gamma)
        logging.info('%s %s' % ('Euler angles', euler_list))
        params_list.append(euler_list)
    
    def make_expRDC_file_win(self):
        expRDCfile, ok = QtGui.QInputDialog.getText(self, 'Experimental RDC file',
                                                    'Enter the name of the experimental RDC file.')
        if ok:
            logging.info('%s %s' % ('Experimental RDC file:', expRDCfile)) 
            params_list.append(expRDCfile)
            exp_rdcs = np.genfromtxt(expRDCfile)
            np.savetxt("exp_rdcs.csv", exp_rdcs)
    
    def make_hcoords_file_win(self):
        hcoords_file, ok = QtGui.QInputDialog.getText(self, 'H coordinates file', 
                                                      'Enter the name of the file containing the H coordinates.')
        if ok:
            logging.info('%s %s' % ('Hydrogen coordinates:', hcoords_file))
            params_list.append(hcoords_file)
    
    def make_ncoords_file_win(self):
        ncoords_file, ok = QtGui.QInputDialog.getText(self, 'N coordinates file', 
                                                      'Enter the name of the file containing the N coordinates.')
        if ok:
            logging.info('%s %s' % ('Nitrogen coordinates:', ncoords_file)) 
            params_list.append(ncoords_file)
            
            params_list.append(24850) 
            logging.info('Dmax = 24850')

    def run_rdc_calc(self):
        rdcrun = calc_rdc_dmax2_diag.ResidualDipolarCouplings(params_list[0], params_list[1], params_list[2], params_list[3], params_list[4], params_list[5])
        rdcrun.get_exp_rdcs()
        rdcrun.get_coords()
        rdcrun.do_matrix_operations()
        rdcrun.back_calculate_rdcs()
        qcalc = qfactor_gui.Qfactor()
        qcalc.qfactor()
        
    def run_pandas(self):
        pandasrun = pandas_gui.Pandas()
        pandasrun.edit_csv()
        pandasrun.manip_rdc_df()
        pandasrun.edit_logfile()
        
class CN_Saupe_Window(QtGui.QWidget):
    """Prompt the user to input the values of the Saupe matrix."""
    def __init__(self):
        super(CN_Saupe_Window, self).__init__()
        self.make_saupewin1()
        self.make_saupewin2()
        self.make_saupewin3()
        self.make_saupewin4()
        self.make_saupewin5()
        self.make_expRDC_file_win()
        self.make_ccoords_file_win()
        self.make_ncoords_file_win()
        self.run_rdc_calc()
        self.run_pandas()
   
    global saupe_list 
    saupe_list = []    
    global diag_list
    diag_list = [] 
    global params_list 
    params_list = []
    
    def make_saupewin1(self):
        sxx, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 1', 
                                           'Enter sxx:', decimals = 10)        
        if ok:
            saupe_list.append(sxx)
            
    def make_saupewin2(self):
        syy, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 2', 
                                           'Enter syy:', decimals = 10)
        if ok:
            saupe_list.append(syy)
            
    def make_saupewin3(self):
        sxy, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 3', 
                                           'Enter sxy:', decimals = 10)        
        if ok:
            saupe_list.append(sxy)
    
    def make_saupewin4(self):
        sxz, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 4', 
                                           'Enter sxz:', decimals = 10)
        if ok:
            saupe_list.append(sxz)
            
    def make_saupewin5(self):
        syz, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 5', 
                                           'Enter syz:', decimals = 10)
        if ok:
            saupe_list.append(syz)
            params_list.append(saupe_list)
        logging.info(saupe_list)
        
        
    def make_expRDC_file_win(self):
        expRDCfile, ok = QtGui.QInputDialog.getText(self, 'Experimental RDC file',
                                                    'Enter the name of the experimental RDC file.')
        if ok:
            logging.info('%s %s' % ('Experimental RDC file:', expRDCfile))
            params_list.append(expRDCfile)
            exp_rdcs = np.genfromtxt(expRDCfile)
            np.savetxt("exp_rdcs.csv", exp_rdcs)
    
    def make_ccoords_file_win(self):
        ccoords_file, ok = QtGui.QInputDialog.getText(self, 'C coordinates file', 
                                                      'Enter the name of the file containing the C coordinates.')
        if ok:
            logging.info('%s %s' % ('Carbon coordinates file:', ccoords_file)) 
            params_list.append(ccoords_file)
    
    def make_ncoords_file_win(self):
        ncoords_file, ok = QtGui.QInputDialog.getText(self, 'N coordinates file', 
                                                      'Enter the name of the file containing the N coordinates.')
        if ok:
            logging.info('%s %s' % ('Nitrogen coordinates file:', ncoords_file)) 
            params_list.append(ncoords_file)
            params_list.append(6125)
            logging.info('Dmax = 6125')
    
    def run_rdc_calc(self):
        rdcrun = calc_rdc_cn_saupe.ResidualDipolarCouplings(params_list[0], params_list[1], params_list[2], params_list[3], params_list[4])
        rdcrun.get_exp_rdcs()
        rdcrun.get_coords()
        rdcrun.back_calculate_rdcs()
        qcalc = qfactor_gui.Qfactor()
        qcalc.qfactor()
    
    def run_pandas(self):
        pandasrun = pandas_gui.Pandas()
        pandasrun.edit_csv()
        pandasrun.manip_rdc_df()
        pandasrun.edit_logfile()
            
class CN_Diag_Window(QtGui.QWidget):
    """Prompt the user to input the values of the Saupe matrix."""
    def __init__(self):
        super(CN_Diag_Window, self).__init__()
        self.make_diagwin1()
        self.make_diagwin2()
        self.make_diagwin3()
        self.make_eulerwin1()
        self.make_eulerwin2()
        self.make_eulerwin3()
        self.make_expRDC_file_win()
        self.make_ccoords_file_win()
        self.make_ncoords_file_win()
        self.run_rdc_calc()
        self.run_pandas()
        
    global diag_list
    diag_list = []
    global euler_list
    euler_list = []
    global params_list
    params_list = []
    
    def make_diagwin1(self):
        Sxx, ok = QtGui.QInputDialog.getDouble(self, 'Diagonalized Matrix Input 1',
                                               'Enter Sxx:', decimals = 10)
        if ok:
            diag_list.append(Sxx)
            
    def make_diagwin2(self):
        Syy, ok = QtGui.QInputDialog.getDouble(self, 'Diagonalized Matrix Input 2',
                                               'Enter Syy:', decimals = 10)
        if ok:
            diag_list.append(Syy)
            
    def make_diagwin3(self):
        Szz, ok = QtGui.QInputDialog.getDouble(self, 'Diagonalized Matrix Input 3',
                                               'Enter Szz:', decimals = 10)
        if ok:
            diag_list.append(Szz)
        logging.info('%s %s' % ('Diagonalized matrix:', diag_list))
        params_list.append(diag_list)        
        
    def make_eulerwin1(self):
        alpha, ok = QtGui.QInputDialog.getDouble(self, 'Euler Angle alpha', 
                                                 'Enter alpha (in degrees)', decimals = 2)
        if ok:
            euler_list.append(alpha)
        
    def make_eulerwin2(self):
        beta, ok = QtGui.QInputDialog.getDouble(self, 'Euler Angle beta', 
                                                 'Enter beta (in degrees)', decimals = 2)                                  
        if ok:
            euler_list.append(beta)
                                        
    def make_eulerwin3(self):
        gamma, ok = QtGui.QInputDialog.getDouble(self, 'Euler Angle gamma', 
                                                 'Enter gamma (in degrees)', decimals = 2)
        if ok:
            euler_list.append(gamma)
        logging.info('%s %s' % ('Euler angles', euler_list))
        params_list.append(euler_list)
    
    def make_expRDC_file_win(self):
        expRDCfile, ok = QtGui.QInputDialog.getText(self, 'Experimental RDC file',
                                                    'Enter the name of the experimental RDC file.')
        if ok:
            logging.info('%s %s' % ('Experimental RDC file:', expRDCfile))
            params_list.append(expRDCfile)
            exp_rdcs = np.genfromtxt(expRDCfile)
            np.savetxt("exp_rdcs.csv", exp_rdcs)
    
    def make_ccoords_file_win(self):
        ccoords_file, ok = QtGui.QInputDialog.getText(self, 'C coordinates file', 
                                                      'Enter the name of the file containing the C coordinates.')
        if ok:
            logging.info('%s %s' % ('Carbon coordinates file:', ccoords_file))
            params_list.append(ccoords_file)
    
    def make_ncoords_file_win(self):
        ncoords_file, ok = QtGui.QInputDialog.getText(self, 'N coordinates file', 
                                                      'Enter the name of the file containing the N coordinates.')
        if ok:
            logging.info('%s %s' % ('Nitrogen coordinates file:', ncoords_file)) 
            params_list.append(ncoords_file)
            params_list.append(6125) 
            logging.info('Dmax = 6125')

    def run_rdc_calc(self):
        rdcrun = calc_rdc_cn_diag.ResidualDipolarCouplings(params_list[0], params_list[1], params_list[2], params_list[3], params_list[4], params_list[5])
        rdcrun.get_exp_rdcs()
        rdcrun.get_coords()
        rdcrun.do_matrix_operations()
        rdcrun.back_calculate_rdcs()
        qcalc = qfactor_gui.Qfactor()
        qcalc.qfactor()
        
    def run_pandas(self):
        pandasrun = pandas_gui.Pandas()
        pandasrun.edit_csv()
        pandasrun.manip_rdc_df()
        pandasrun.edit_logfile()
    
class CaHa_Saupe_Window(QtGui.QWidget):
    """Prompt the user to input the values of the Saupe matrix."""
    def __init__(self):
        super(CaHa_Saupe_Window, self).__init__()
        self.make_saupewin1()
        self.make_saupewin2()
        self.make_saupewin3()
        self.make_saupewin4()
        self.make_saupewin5()
        self.make_expRDC_file_win()
        self.make_cacoords_file_win()
        self.make_hacoords_file_win()
        self.run_rdc_calc()
        self.run_pandas()
   
    global saupe_list 
    saupe_list = []    
    global diag_list
    diag_list = [] 
    global params_list 
    params_list = []
    
    def make_saupewin1(self):
        sxx, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 1', 
                                           'Enter sxx:', decimals = 10)        
        if ok:
            saupe_list.append(sxx)
            
    def make_saupewin2(self):
        syy, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 2', 
                                           'Enter syy:', decimals = 10)
        if ok:
            saupe_list.append(syy)
            
    def make_saupewin3(self):
        sxy, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 3', 
                                           'Enter sxy:', decimals = 10)        
        if ok:
            saupe_list.append(sxy)
    
    def make_saupewin4(self):
        sxz, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 4', 
                                           'Enter sxz:', decimals = 10)
        if ok:
            saupe_list.append(sxz)
            
    def make_saupewin5(self):
        syz, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 5', 
                                           'Enter syz:', decimals = 10)
        if ok:
            saupe_list.append(syz)
            params_list.append(saupe_list)
        logging.info('%s %s' % ('Saupe matrix:', saupe_list))        
        
    def make_expRDC_file_win(self):
        expRDCfile, ok = QtGui.QInputDialog.getText(self, 'Experimental RDC file',
                                                    'Enter the name of the experimental RDC file.')
        if ok:
            logging.info('%s %s' % ('Experimental RDC file:', expRDCfile)) 
            params_list.append(expRDCfile)
            exp_rdcs = np.genfromtxt(expRDCfile)
            np.savetxt("exp_rdcs.csv", exp_rdcs)
    
    def make_cacoords_file_win(self):
        cacoords_file, ok = QtGui.QInputDialog.getText(self, 'Calpha coordinates file', 
                                                      'Enter the name of the file containing the Calpha coordinates.')
        if ok:
            logging.info('%s %s' % ('Alpha carbon coordinates file:', cacoords_file)) 
            params_list.append(cacoords_file)
    
    def make_hacoords_file_win(self):
        hacoords_file, ok = QtGui.QInputDialog.getText(self, 'Halpha coordinates file', 
                                                      'Enter the name of the file containing the Halpha coordinates.')
        if ok:
            logging.info('%s %s' % ('Alpha hydrogen coordinates file:', hacoords_file)) 
            params_list.append(hacoords_file)
            params_list.append(-60400)
            logging.info('Dmax = -60400')
    
    def run_rdc_calc(self):
        rdcrun = calc_rdc_caha_saupe.ResidualDipolarCouplings(params_list[0], params_list[1], params_list[2], params_list[3], params_list[4])
        rdcrun.get_exp_rdcs()
        rdcrun.get_coords()
        rdcrun.back_calculate_rdcs()
        qcalc = qfactor_gui.Qfactor()
        qcalc.qfactor()
        
    def run_pandas(self):
        pandasrun = pandas_gui.Pandas()
        pandasrun.edit_csv()
        pandasrun.manip_rdc_df()
        pandasrun.edit_logfile()
            
class CaHa_Diag_Window(QtGui.QWidget):
    """Prompt the user to input the values of the Saupe matrix."""
    def __init__(self):
        super(CaHa_Diag_Window, self).__init__()
        self.make_diagwin1()
        self.make_diagwin2()
        self.make_diagwin3()
        self.make_eulerwin1()
        self.make_eulerwin2()
        self.make_eulerwin3()
        self.make_expRDC_file_win()
        self.make_cacoords_file_win()
        self.make_hacoords_file_win()
        self.run_rdc_calc()
        self.run_pandas()
        
    global diag_list
    diag_list = []
    global euler_list
    euler_list = []
    global params_list
    params_list = []
    
    def make_diagwin1(self):
        Sxx, ok = QtGui.QInputDialog.getDouble(self, 'Diagonalized Matrix Input 1',
                                               'Enter Sxx:', decimals = 10)
        if ok:
            diag_list.append(Sxx)
            
    def make_diagwin2(self):
        Syy, ok = QtGui.QInputDialog.getDouble(self, 'Diagonalized Matrix Input 2',
                                               'Enter Syy:', decimals = 10)
        if ok:
            diag_list.append(Syy)
            
    def make_diagwin3(self):
        Szz, ok = QtGui.QInputDialog.getDouble(self, 'Diagonalized Matrix Input 3',
                                               'Enter Szz:', decimals = 10)
        if ok:
            diag_list.append(Szz)
        logging.info('%s %s' % ('Diagonalized matrix:', diag_list))
        params_list.append(diag_list)        
        
    def make_eulerwin1(self):
        alpha, ok = QtGui.QInputDialog.getDouble(self, 'Euler Angle alpha', 
                                                 'Enter alpha (in degrees)', decimals = 2)
        if ok:
            euler_list.append(alpha)
        
    def make_eulerwin2(self):
        beta, ok = QtGui.QInputDialog.getDouble(self, 'Euler Angle beta', 
                                                 'Enter beta (in degrees)', decimals = 2)                                  
        if ok:
            euler_list.append(beta)
                                        
    def make_eulerwin3(self):
        gamma, ok = QtGui.QInputDialog.getDouble(self, 'Euler Angle gamma', 
                                                 'Enter gamma (in degrees)', decimals = 2)
        if ok:
            euler_list.append(gamma)
        logging.info('%s %s' % ('Euler angles', euler_list))
        params_list.append(euler_list)
    
    def make_expRDC_file_win(self):
        expRDCfile, ok = QtGui.QInputDialog.getText(self, 'Experimental RDC file',
                                                    'Enter the name of the experimental RDC file.')
        if ok:
            logging.info('%s %s' % ('Experimental RDC file:', expRDCfile)) 
            params_list.append(expRDCfile)
            exp_rdcs = np.genfromtxt(expRDCfile)
            np.savetxt("exp_rdcs.csv", exp_rdcs)
    
    def make_cacoords_file_win(self):
        cacoords_file, ok = QtGui.QInputDialog.getText(self, 'Calpha coordinates file', 
                                                      'Enter the name of the file containing the Calpha coordinates.')
        if ok:
            logging.info('%s %s' % ('Alpha carbon coordinates file:', cacoords_file)) 
            params_list.append(cacoords_file)
    
    def make_hacoords_file_win(self):
        hacoords_file, ok = QtGui.QInputDialog.getText(self, 'Halpha coordinates file', 
                                                     'Enter the name of the file containing the Halpha coordinates.')
        
        if ok:
            logging.info('%s %s' % ('Alpha hydrogen coordinates file:', hacoords_file))
            params_list.append(hacoords_file)
            params_list.append(6125)
            logging.info('Dmax = 6125')

    def run_rdc_calc(self):
        rdcrun = calc_rdc_caha_diag.ResidualDipolarCouplings(params_list[0], params_list[1], params_list[2], params_list[3], params_list[4], params_list[5])
        rdcrun.get_exp_rdcs()
        rdcrun.get_coords()
        rdcrun.do_matrix_operations()
        rdcrun.back_calculate_rdcs()
        qcalc = qfactor_gui.Qfactor()
        qcalc.qfactor()
        
    def run_pandas(self):
        pandasrun = pandas_gui.Pandas()
        pandasrun.edit_csv()
        pandasrun.manip_rdc_df()
        pandasrun.edit_logfile()
 
def main():
    app = QtGui.QApplication(sys.argv)
    RDC_GUI = IntroWindow()
    sys.exit(app.exec_()) 
    
main()
   

    

        
            