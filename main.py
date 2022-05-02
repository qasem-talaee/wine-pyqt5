from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLabel, QMessageBox, QGroupBox, QVBoxLayout, QWidget
import sys
from libwine.wine import Wine
import os

class WineMain(QMainWindow):
    
    def __init__(self):
        self.WINEPATH = "/"
        if not os.path.isfile('wine.txt'):
            open('wine.txt', 'w').close()
        super(WineMain, self).__init__()
        uic.loadUi('ui/main.ui', self)
        self.pushButton_2.clicked.connect(self.add_new)
        self.pushButton.clicked.connect(self.add_exiting)
        self.widget = QWidget()
        self.vb = QVBoxLayout()
        self.update_list()
        self.show()
    
    def update_list(self):
        name = []
        dir = []
        self.widget = QWidget()
        self.vb = QVBoxLayout()
        self.widget.destroyed
        with open('wine.txt', 'r') as f:
            for line in f:
                detail = line.replace("\n", "").split(",,")
                name.append(detail[0])
                dir.append(detail[1])
        if len(name) == 0:
            obj = QLabel("No Wine Prefix Found.Please create new.")
            self.vb.addWidget(obj)
            self.widget.setLayout(self.vb)
            self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.scrollArea.setWidgetResizable(True)
            self.scrollArea.setWidget(self.widget)
        else:
            self.button_list = []
            for i, n in enumerate(name):
                self.button_list.append(QPushButton(n))
                self.vb.addWidget(self.button_list[i])
            for i in range(len(dir)):
                self.button_list[i].clicked.connect(lambda *args : self.open_wine(dir[i]))
            self.widget.setLayout(self.vb)
            self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.scrollArea.setWidgetResizable(True)
            self.scrollArea.setWidget(self.widget)
    
    def open_wine(self, dir):
        print(dir)
    
    def add_new(self):
        dir = str(QFileDialog.getExistingDirectory(self, "Select Target Directory"))
        if dir != '':
            try:
                wineprefix = Wine(winepath=self.WINEPATH, wineprefix=dir, verbose=3)
            except:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Please sure that you installed wine on your machine.")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.exec_()
            else:
                wineprefix.winecfg()
                with open('wine.txt', 'a') as f:
                    f.write('\n' + dir.split("/")[-1] + ",," + dir)
                self.update_list()
    
    def add_exiting(self):
        dir = str(QFileDialog.getExistingDirectory(self, "Select Target Directory"))
        if dir != '':
                #wineprefix = Wine(winepath=self.WINEPATH, wineprefix=dir, verbose=3)
                #wineprefix.winecfg()
                with open('wine.txt', 'a') as f:
                    f.write('\n' + dir.split("/")[-1] + ",," + dir)
                self.update_list()
        
app = QApplication(sys.argv)
window = WineMain()
app.exec_()