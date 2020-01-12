import os
import PySide2
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from PySide2 import QtCore
from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon
from pylab import *


dirname = os.getcwd()
#plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(dirname, 'plugins', 'platforms')

class Window(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Box Office Trend')
        self.setGeometry(650, 550, 650, 550)
        #self.setMaximumHeight(650)
        #self.setMaximumHeight(650)
        #self.setMinimumWidth(650)
        #self.setMaximumWidth(650)
        
        

        self.setIcon()
        self.center()
        self.createGridLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(self.groupBox)
        self.setLayout(vbox)
        self.create
        
        self.show()
        #print(os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'])
   

    def setIcon(self):

        """ 
        Setting icon to the main window.
        """
        appIcon = QIcon("icon.png")
        self.setWindowIcon(appIcon)

    def center(self):

        """
        Setting main window to center.
        """
        qRect = self.frameGeometry()
        centerpoint = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerpoint)
        self.move(qRect.topLeft())

    def createGraph(self):

        """
        This method is invoked on the click of Generate Trend Button and creates the graph.
        """

        try:
            self.selectedMovie = str(self.ddl.currentText())
            if self.selectedMovie == "-- Please select the movie --":
                QMessageBox.about(self, 'Message', 'Please select a movie from the dropdown list')
            elif self.selectedMovie == "Data File Not Found":
                QMessageBox.about(self, 'Message', 'Data File Not Found!')
            else:
                self.progressbar.setVisible(True)
                self.progressbar.setValue(20)
                bocollection = self.GlobalMovieSet[self.GlobalMovieSet.Movie == self.selectedMovie].iloc[0,1:]
                day = range(1,16)
                time.sleep(1)
                self.progressbar.setValue(60)
                plot(day,bocollection, markerfacecolor= 'w', marker = 'o')
                plt.gcf().canvas.set_window_title('Box Office Trend')
                xlabel('Day')
                ylabel('Box Office Collection in Crores')
                title('Day wise Box Office Collection of '+ self.selectedMovie)
                grid(True)
                time.sleep(1)
                self.progressbar.setValue(100)
                time.sleep(1)
                show()
                self.progressbar.reset()
                self.progressbar.setVisible(False)
                print(bocollection)
        except:
            QMessageBox.about(self, 'Error', 'Something went wrong!')
            self.progressbar.reset()
            self.progressbar.setVisible(False)
        

    
    def createGridLayout(self):

        """ 
        Creating a grid layout and adding widgets (comboxBox, button and progressbAR) to the layout.
        """

        self.groupBox = QGroupBox()
        gridLayout = QGridLayout()

        self.ddl = QComboBox(self)
        try:
            movieDataSet = pd.read_excel('MovieDataset15days.xlsx')
            movieList = movieDataSet["Movie"].tolist()
            print(movieList)
            self.ddl.addItem('-- Please select the movie --')

            for movie in movieList:
                self.ddl.addItem(movie)
            self.GlobalMovieSet = movieDataSet
        except :
            self.ddl.addItem('Data File Not Found')
       
        self.ddl.setStyleSheet("border-radius:5px; border: 2px solid grey; color:black; font-weight: 500; background-color:none; height:25px; padding-left:2px;")
        gridLayout.addWidget(self.ddl, 0, 0)

        searchButton = QPushButton("Generate Trend", self)
        searchButton.clicked.connect(self.createGraph)
        searchButton.setIcon(QIcon("search.png"))
        searchButton.setStyleSheet("background-color: #4287f5; color: white; font-weight: bold; border:2px solid grey; height: 25px; border-radius:5px; margin-left:120px; margin-right:120px;")
        gridLayout.addWidget(searchButton, 1, 0)

        #self.statusLabel = QLabel("Creating graph")
        self.progressbar = QProgressBar()
        self.progressbar.setMinimum(0)
        self.progressbar.setMaximum(100)
        self.progressbar.setVisible(False)
        self.progressbar.setStyleSheet("border:2px solid grey; border-radius: 5px; color:black; font-weight: bold; text-align:center; width: 20px;height: 25px; margin-left:120px; margin-right:120px;")
        
        gridLayout.addWidget(self.progressbar, 2, 0)


        self.groupBox.setLayout(gridLayout)

        
myApp = QApplication(sys.argv)
window = Window()
window.show()

myApp.exec_()
sys.exit(0)






