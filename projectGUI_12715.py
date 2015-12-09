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
    
    def create_dmax1_saupe_win2(self):
        self.dmax1saupe = Dmax1_Saupe_Window()
        
    def create_dmax1_saupe_win3(self):
        self.dmax1saupe = Dmax1_Saupe_Window()
    
    def create_dmax1_saupe_win4(self):
        self.dmax1saupe = Dmax1_Saupe_Window()
    
    def create_dmax1_saupe_win5(self):
        self.dmax1saupe = Dmax1_Saupe_Window()
    
    def create_dmax1_diag_win1(self):
        self.dmax1diag = Dmax1_Diag_Window()
        
    def create_dmax1_diag_win2(self):
        self.dmax1diag = Dmax1_Diag_Window()
    
    def create_dmax1_diag_win3(self):
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
    
    def create_dmax2_saupe_win2(self):
        self.dmax2saupe = Dmax2_Saupe_Window()
        
    def create_dmax2_saupe_win3(self):
        self.dmax2saupe = Dmax2_Saupe_Window()
    
    def create_dmax2_saupe_win4(self):
        self.dmax2saupe = Dmax2_Saupe_Window()
    
    def create_dmax2_saupe_win5(self):
        self.dmax2saupe = Dmax2_Saupe_Window()
        
    def matrix_buttons(self):
        "Prompt the user to choose whether to input the saupe matrix or the \
        diagonalized matrix and Euler angles."""    
        saupe_btn = QtGui.QPushButton("Input saupe matrix", self)
        saupe_btn.clicked.connect(self.create_dmax2_saupe_win1)
        saupe_btn.resize(200, 20)
        saupe_btn.move(150, 50)
        
        diag_btn = QtGui.QPushButton("Input diagonalized matrix and Euler angles", self)
        #diag_btn.clicked.connect() #next window class
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
        self.make_diagwin1()
        self.make_diagwin2()
        self.make_diagwin3()
#   
    global saupe_list 
    saupe_list = []   #you will need to redefine this for each version?  
    global diag_list
    diag_list = []    
    
    def make_saupewin1(self):
        sxx, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 1', 
                                           'Enter sxx:', decimals = 5)        
        if ok:
            saupe_list.append(sxx)
            
    def make_saupewin2(self):
        syy, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 2', 
                                           'Enter syy:', decimals = 5)
        if ok:
            saupe_list.append(syy)
            
    def make_saupewin3(self):
        sxy, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 3', 
                                           'Enter sxy:', decimals = 5)        
        if ok:
            saupe_list.append(sxy)
    
    def make_saupewin4(self):
        sxz, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 4', 
                                           'Enter sxz:', decimals = 5)
        if ok:
            saupe_list.append(sxz)
            
    def make_saupewin5(self):
        syz, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 5', 
                                           'Enter syz:', decimals = 5)
        if ok:
            saupe_list.append(syz)
        print saupe_list
        
class Dmax1_Diag_Window(QtGui.QWidget):
    """Prompt the user to input the values of the Saupe matrix."""
    def __init__(self):
        super(Dmax1_Diag_Window, self).__init__()
        self.make_diagwin1()
        self.make_diagwin2()
        self.make_diagwin3()
        
    global diag_list
    diag_list = []
    
    def make_diagwin1(self):
        Sxx, ok = QtGui.QInputDialog.getDouble(self, 'Diagonalized Matrix Input 1',
                                               'Enter Sxx:', decimals = 5)
        if ok:
            diag_list.append(Sxx)
            
    def make_diagwin2(self):
        Syy, ok = QtGui.QInputDialog.getDouble(self, 'Diagonalized Matrix Input 2',
                                               'Enter Syy:', decimals = 5)
        if ok:
            diag_list.append(Syy)
            
    def make_diagwin3(self):
        Szz, ok = QtGui.QInputDialog.getDouble(self, 'Diagonalized Matrix Input 3',
                                               'Enter Szz:', decimals = 5)
        if ok:
            diag_list.append(Szz)
        print diag_list
                                      
        
class Dmax2_Saupe_Window(QtGui.QWidget):
    """Prompt the user to input the values of the Saupe matrix."""
    def __init__(self):
        super(Dmax2_Saupe_Window, self).__init__()
        self.make_saupewin1()
        self.make_saupewin2()
        self.make_saupewin3()
        self.make_saupewin4()
        self.make_saupewin5()
#   
    global saupe_list 
    saupe_list = []   #you will need to redefine this for each version?  
    
    def make_saupewin1(self):
        sxx, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 1', 
                                           'Enter sxx:', decimals = 5)        
        if ok:
            saupe_list.append(sxx)
    
    def make_saupewin2(self):
        syy, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 2', 
                                           'Enter syy:', decimals = 5)
        if ok:
            saupe_list.append(syy)
            
    def make_saupewin3(self):
        sxy, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 3', 
                                           'Enter sxy:', decimals = 5)        
        if ok:
            saupe_list.append(sxy)
    
    def make_saupewin4(self):
        sxz, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 4', 
                                           'Enter sxz:', decimals = 5)
        if ok:
            saupe_list.append(sxz)
            
    def make_saupewin5(self):
        syz, ok = QtGui.QInputDialog.getDouble(self, 'Saupe Matrix Input 5', 
                                           'Enter syz:', decimals = 5)
        if ok:
            saupe_list.append(syz)
        print saupe_list

def main():
    app = QtGui.QApplication(sys.argv)
    RDC_GUI = IntroWindow()
    sys.exit(app.exec_())
    
main()

#random change for git   

    

        
            