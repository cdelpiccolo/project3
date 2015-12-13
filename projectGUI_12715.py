# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 21:59:53 2015

@author: Chiara Del Piccolo
"""

import numpy as np
import scipy as sp
from math import *
import time, sys, os, math, copy, re
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPushButton
import calc_rdc_dmax1_diag
import calc_rdc_dmax1_saupe
import calc_rdc_dmax2_diag
import calc_rdc_dmax2_saupe
import calc_rdc_cn_diag
import calc_rdc_cn_saupe
import qfactor_gui
import pandas as pd
import seaborn as sns

class IntroWindow(QtGui.QMainWindow):
    """Greet the user, ask the user to enter the application."""
    def __init__(self):
        super(IntroWindow, self).__init__()
        self.setWindowTitle("Welcome")
        self.setGeometry(50, 50, 400, 150)
        self.entry_button()
        
    def create_win(self):
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
        self.setGeometry(50, 50, 500, 200) #width, height
        self.coupling_buttons()
        
    def create_nh_win(self):
        self.nhwin = NH_Dmax_Window()
    
    def create_cn_win(self):
        self.cnwin = CN_Matrix_Window()  
        
    def create_caha_win(self):
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
        self.dmax1win = Dmax1_Window() #not yet written
        
    def create_dmax2_win(self):
        self.dmax2win = Dmax2_Window() #not yet written
        
    def dmax_buttons(self):
        "Prompt the user to choose the scaling factor (Dmax) for the calculations."""    
        dmax1_btn = QtGui.QPushButton("Dmax = 21700", self)
        dmax1_btn.clicked.connect(self.create_dmax1_win) 
        dmax1_btn.resize(200, 20)
        dmax1_btn.move(150, 50)
        
        dmax2_btn = QtGui.QPushButton("Dmax = 24850", self)
        dmax2_btn.clicked.connect(self.create_dmax2_win) #next window class to write
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
        self.cnsaupe = CN_Saupe_Window()
       
    def create_cn_diag_win1(self):
        self.cndiag = CN_Diag_Window()
        
    def matrix_buttons(self):
        "Prompt the user to choose whether to input the saupe matrix or the \
        diagonalized matrix and Euler angles."""    
        saupe_btn = QtGui.QPushButton("Input saupe matrix", self)
        saupe_btn.clicked.connect(CN_Saupe_Window)
        saupe_btn.resize(200, 20)
        saupe_btn.move(150, 50)
        
        diag_btn = QtGui.QPushButton("Input diagonalized matrix and Euler angles", self)
        diag_btn.clicked.connect(CN_Diag_Window) #next window class
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
        
    def matrix_buttons(self):
        "Prompt the user to choose whether to input the saupe matrix or the \
        diagonalized matrix and Euler angles."""    
        saupe_btn = QtGui.QPushButton("Input saupe matrix", self)
        #saupe_btn.clicked.connect(self.create
        saupe_btn.resize(200, 20)
        saupe_btn.move(150, 50)
        
        diag_btn = QtGui.QPushButton("Input diagonalized matrix and Euler angles", self)
        #diag_btn.clicked.connect(CaHa_Diag_Window) #next window class
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
        self.dmax1saupe = Dmax1_Saupe_Window()
       
    def create_dmax1_diag_win1(self):
        self.dmax1diag = Dmax1_Diag_Window()
                
    def matrix_buttons(self):
        "Prompt the user to choose whether to input the saupe matrix or the \
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
        self.dmax2saupe = Dmax2_Saupe_Window()
    
    def create_dmax2_diag_win1(self):
        self.dmax2diag = Dmax2_Diag_Window()
        
    def matrix_buttons(self):
        "Prompt the user to choose whether to input the saupe matrix or the \
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
#   
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
        print saupe_list
        
        
    def make_expRDC_file_win(self):
        expRDCfile, ok = QtGui.QInputDialog.getText(self, 'Experimental RDC file',
                                                    'Enter the name of the experimental RDC file.')
        if ok:
            print expRDCfile #to be changed later
            params_list.append(expRDCfile)
    
    def make_hcoords_file_win(self):
        hcoords_file, ok = QtGui.QInputDialog.getText(self, 'H coordinates file', 
                                                      'Enter the name of the file containing the H coordinates.')
        if ok:
            print hcoords_file #to be changed later
            params_list.append(hcoords_file)
    
    def make_ncoords_file_win(self):
        ncoords_file, ok = QtGui.QInputDialog.getText(self, 'N coordinates file', 
                                                      'Enter the name of the file containing the N coordinates.')
        if ok:
            print ncoords_file #to be changed later
            params_list.append(ncoords_file)
            params_list.append(21700)
    
    def run_rdc_calc(self):
        rdcrun = calc_rdc_dmax1_saupe.ResidualDipolarCouplings(params_list[0], params_list[1], params_list[2], params_list[3], params_list[4])
        rdcrun.get_exp_rdcs()
        rdcrun.get_coords()
        rdcrun.back_calculate_rdcs()
        qcalc = qfactor_gui.Qfactor()
        qcalc.qfactor()
            
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
        print diag_list
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
        print euler_list
        params_list.append(euler_list)
    
    def make_expRDC_file_win(self):
        expRDCfile, ok = QtGui.QInputDialog.getText(self, 'Experimental RDC file',
                                                    'Enter the name of the experimental RDC file.')
        if ok:
            print expRDCfile #to be changed later
            params_list.append(expRDCfile)
#            exp_rdcs = np.genfromtxt(expRDCfile)
#            np.savetxt("exp_rdcs.csv", exp_rdcs)
    
    def make_hcoords_file_win(self):
        hcoords_file, ok = QtGui.QInputDialog.getText(self, 'H coordinates file', 
                                                      'Enter the name of the file containing the H coordinates.')
        if ok:
            print hcoords_file #to be changed later
            params_list.append(hcoords_file)
    
    def make_ncoords_file_win(self):
        ncoords_file, ok = QtGui.QInputDialog.getText(self, 'N coordinates file', 
                                                      'Enter the name of the file containing the N coordinates.')
        if ok:
            print ncoords_file #to be changed later
            params_list.append(ncoords_file)
            
            params_list.append(21700) #make new function for this?

    def run_rdc_calc(self):
        rdcrun = calc_rdc_dmax1_diag.ResidualDipolarCouplings(params_list[0], params_list[1], params_list[2], params_list[3], params_list[4], params_list[5])
        rdcrun.get_exp_rdcs()
        rdcrun.get_coords()
        rdcrun.do_matrix_operations()
        rdcrun.back_calculate_rdcs()
        qcalc = qfactor_gui.Qfactor()
        qcalc.qfactor()
     
       
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
   
    global saupe_list 
    saupe_list = []   #you will need to redefine this for each version?  
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
        print saupe_list  #to be removed later
        
    def make_expRDC_file_win(self):
        expRDCfile, ok = QtGui.QInputDialog.getText(self, 'Experimental RDC file',
                                                    'Enter the name of the experimental RDC file.')
        if ok:
            print expRDCfile #to be changed later
            params_list.append(expRDCfile)
    
    def make_hcoords_file_win(self):
        hcoords_file, ok = QtGui.QInputDialog.getText(self, 'H coordinates file', 
                                                      'Enter the name of the file containing the H coordinates.')
        if ok:
            print hcoords_file #to be changed later
            params_list.append(hcoords_file)
    
    def make_ncoords_file_win(self):
        ncoords_file, ok = QtGui.QInputDialog.getText(self, 'N coordinates file', 
                                                      'Enter the name of the file containing the N coordinates.')
        if ok:
            print ncoords_file #to be changed later
            params_list.append(ncoords_file)
            params_list.append(24850)
    
    def run_rdc_calc(self):
        rdcrun = calc_rdc_dmax2_saupe.ResidualDipolarCouplings(params_list[0], params_list[1], params_list[2], params_list[3], params_list[4])
        rdcrun.get_exp_rdcs()
        rdcrun.get_coords()
        rdcrun.back_calculate_rdcs()
        qcalc = qfactor_gui.Qfactor()
        qcalc.qfactor()
        
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
        print diag_list
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
        print euler_list
        params_list.append(euler_list)
    
    def make_expRDC_file_win(self):
        expRDCfile, ok = QtGui.QInputDialog.getText(self, 'Experimental RDC file',
                                                    'Enter the name of the experimental RDC file.')
        if ok:
            print expRDCfile #to be changed later
            params_list.append(expRDCfile)
    
    def make_hcoords_file_win(self):
        hcoords_file, ok = QtGui.QInputDialog.getText(self, 'H coordinates file', 
                                                      'Enter the name of the file containing the H coordinates.')
        if ok:
            print hcoords_file #to be changed later
            params_list.append(hcoords_file)
    
    def make_ncoords_file_win(self):
        ncoords_file, ok = QtGui.QInputDialog.getText(self, 'N coordinates file', 
                                                      'Enter the name of the file containing the N coordinates.')
        if ok:
            print ncoords_file #to be changed later
            params_list.append(ncoords_file)
            
            params_list.append(24850) 

    def run_rdc_calc(self):
        rdcrun = calc_rdc_dmax2_diag.ResidualDipolarCouplings(params_list[0], params_list[1], params_list[2], params_list[3], params_list[4], params_list[5])
        rdcrun.get_exp_rdcs()
        rdcrun.get_coords()
        rdcrun.do_matrix_operations()
        rdcrun.back_calculate_rdcs()
        qcalc = qfactor_gui.Qfactor()
        qcalc.qfactor()
        
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
#   
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
        print saupe_list
        
        
    def make_expRDC_file_win(self):
        expRDCfile, ok = QtGui.QInputDialog.getText(self, 'Experimental RDC file',
                                                    'Enter the name of the experimental RDC file.')
        if ok:
            print expRDCfile #to be changed later
            params_list.append(expRDCfile)
    
    def make_ccoords_file_win(self):
        ccoords_file, ok = QtGui.QInputDialog.getText(self, 'C coordinates file', 
                                                      'Enter the name of the file containing the C coordinates.')
        if ok:
            print ccoords_file #to be changed later
            params_list.append(ccoords_file)
    
    def make_ncoords_file_win(self):
        ncoords_file, ok = QtGui.QInputDialog.getText(self, 'N coordinates file', 
                                                      'Enter the name of the file containing the N coordinates.')
        if ok:
            print ncoords_file #to be changed later
            params_list.append(ncoords_file)
            params_list.append(6125)
    
    def run_rdc_calc(self):
        rdcrun = calc_rdc_cn_saupe.ResidualDipolarCouplings(params_list[0], params_list[1], params_list[2], params_list[3], params_list[4])
        rdcrun.get_exp_rdcs()
        rdcrun.get_coords()
        rdcrun.back_calculate_rdcs()
        qcalc = qfactor_gui.Qfactor()
        qcalc.qfactor()
            
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
        print diag_list
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
        print euler_list
        params_list.append(euler_list)
    
    def make_expRDC_file_win(self):
        expRDCfile, ok = QtGui.QInputDialog.getText(self, 'Experimental RDC file',
                                                    'Enter the name of the experimental RDC file.')
        if ok:
            print expRDCfile #to be changed later
            params_list.append(expRDCfile)
    
    def make_ccoords_file_win(self):
        ccoords_file, ok = QtGui.QInputDialog.getText(self, 'C coordinates file', 
                                                      'Enter the name of the file containing the C coordinates.')
        if ok:
            print ccoords_file #to be changed later
            params_list.append(ccoords_file)
    
    def make_ncoords_file_win(self):
        ncoords_file, ok = QtGui.QInputDialog.getText(self, 'N coordinates file', 
                                                      'Enter the name of the file containing the N coordinates.')
        if ok:
            print ncoords_file #to be changed later
            params_list.append(ncoords_file)
            
            params_list.append(6125) 

    def run_rdc_calc(self):
        rdcrun = calc_rdc_cn_diag.ResidualDipolarCouplings(params_list[0], params_list[1], params_list[2], params_list[3], params_list[4], params_list[5])
        rdcrun.get_exp_rdcs()
        rdcrun.get_coords()
        rdcrun.do_matrix_operations()
        rdcrun.back_calculate_rdcs()
        qcalc = qfactor_gui.Qfactor()
        qcalc.qfactor()
    

def main():
    app = QtGui.QApplication(sys.argv)
    RDC_GUI = IntroWindow()
    sys.exit(app.exec_())
    
main()

#random change for git   

    

        
            