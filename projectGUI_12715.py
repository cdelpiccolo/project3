# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 21:59:53 2015

@author: Chiara Del Piccolo
"""

import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPushButton

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
        self.cnwin = CN_Matrix_Window()  #not yet written
        
    def create_caha_win(self):
        self.cahawin = CaHa_Matrix_Window() #not yet written
        
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
        
    def dmax_buttons(self):
        "Prompt the user to choose the scaling factor (Dmax) for the calculations."""    
        dmax1_btn = QtGui.QPushButton("Dmax = 21700", self)
        #dmax_btn.clicked.connect(NH_Dmax1_Matrix_Window()) #correct way to call the next window?
        dmax1_btn.resize(200, 20)
        dmax1_btn.move(150, 50)
        
        dmax2_btn = QtGui.QPushButton("Dmax = 24850", self)
        #dmax2_btn.clicked.connect(NH_Dmax2_Matrix_Window()) #next window class
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
        
    def matrix_buttons(self):
        "Prompt the user to choose whether to input the saupe matrix or the \
        diagonalized matrix and Euler angles."""    
        saupe_btn = QtGui.QPushButton("Input saupe matrix", self)
        #saupe_btn.clicked.connect(CN_Saupe_Window) #next window class
        saupe_btn.resize(200, 20)
        saupe_btn.move(150, 50)
        
        diag_btn = QtGui.QPushButton("Input diagonalized matrix and Euler angles", self)
        #diag_btn.clicked.connect(CN_Diag_Window) #next window class
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

def main():
    app = QtGui.QApplication(sys.argv)
    RDC_GUI = IntroWindow()
    sys.exit(app.exec_())
    
main()
        

    

        
            