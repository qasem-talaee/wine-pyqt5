import subprocess
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLabel, QMessageBox, QVBoxLayout, QWidget, QHBoxLayout, QGroupBox
import sys
import os
import shutil
from functools import partial

from ui import res
from lib import wine

class WineMain(QMainWindow):
    
    def __init__(self):
        if not os.path.isfile('wine.txt'):
            open('wine.txt', 'w').close()
        if not os.path.isfile('lib/link/link.txt'):
            open('lib/link/link.txt', 'w').close()
        super(WineMain, self).__init__()
        uic.loadUi('ui/main.ui', self)
        self.pushButton_2.clicked.connect(self.add_new)
        self.pushButton.clicked.connect(self.add_exiting)
        self.actionAbout_Me.triggered.connect(self.about_me)
        self.pushButton_3.clicked.connect(self.install_wine)
        self.widget = QWidget()
        self.vb = QVBoxLayout()
        self.update_list()
        self.show()
    
    def update_list(self):
        name = []
        dire = []
        self.widget = QWidget()
        self.vb = QVBoxLayout()
        self.hv = QHBoxLayout()
        self.qb = QGroupBox()
        self.widget.destroyed
        os.chdir(sys.path[0])
        with open('wine.txt', 'r') as f:
            for line in f:
                if line != '\n':
                    detail = line.replace("\n", "").split(",,")
                    name.append(detail[0])
                    dire.append(detail[1])
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
            self.del_list = []
            for i, n in enumerate(name):
                self.hv = QHBoxLayout()
                self.qb = QGroupBox()
                but = QPushButton(n)
                self.button_list.append(but)
                del_but = QPushButton("Delete")
                del_but.setStyleSheet("""
                                        QPushButton {
                                            background-color: rgb(255, 0, 0);
                                            color: rgb(255, 255, 255);
                                        }
                                        QPushButton:hover {
                                            background-color: rgb(255, 255, 255);
                                            color: rgb(0, 0, 0);
                                        }
                                    """)
                self.del_list.append(del_but)
                self.hv.addWidget(self.button_list[i], stretch=1)
                self.hv.addWidget(self.del_list[i])
                self.qb.setLayout(self.hv)
                self.vb.addWidget(self.qb)
            for i in range(len(dire)):
                self.button_list[i].clicked.connect(partial(self.open_wine, dire[i]))
                self.del_list[i].clicked.connect(partial(self.del_wine, dire[i]))
            self.widget.setLayout(self.vb)
            self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.scrollArea.setWidgetResizable(True)
            self.scrollArea.setWidget(self.widget)
    
    def open_wine(self, dir):
        self.close()
        os.chdir(sys.path[0])
        subprocess.call('python3 menu.py ' + dir, shell=True)
    
    def del_wine(self, dir):
        msg = QMessageBox()
        msg.setWindowTitle("Delete wine prefix")
        msg.setText("Are you sure you want to do this?")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        msg.setIcon(QMessageBox.Icon.Warning)
        result = msg.exec_()
        if result ==  QMessageBox.StandardButton.Ok:
            os.chdir(sys.path[0])
            if os.path.isdir(dir):
                shutil.rmtree(dir)
            with open("wine.txt", 'r') as f:
                lines = f.readlines()
            with open("wine.txt", 'w') as f:
                for line in lines:
                    if line != '\n':
                        detail = line.replace("\n", "").split(",,")[1]
                        if detail != dir:
                            f.write(line)
            self.update_list()
    
    def add_new(self):
        dir = str(QFileDialog.getExistingDirectory(self, "Select Target Directory"))
        if dir != '':
            my_wine = wine.Wine(dir=dir)
            try:
                my_wine.winecfg()
            except:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Please sure that you installed wine on your machine.")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.exec_()
            else:
                os.chdir(sys.path[0])
                with open('wine.txt', 'a') as f:
                    f.write('\n' + dir.split("/")[-1] + ",," + dir)
                self.update_list()
    
    def add_exiting(self):
        dir = str(QFileDialog.getExistingDirectory(self, "Select Target Directory"))
        if dir != '':
            my_wine = wine.Wine(dir=dir)
            try:
                my_wine.winecfg()
            except:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Please enter a valid wine prefix folder.")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.exec_()
            else:
                with open('wine.txt', 'a') as f:
                    f.write('\n' + dir.split("/")[-1] + ",," + dir)
                self.update_list()
            
    def about_me(self):
        msg = QMessageBox()
        msg.setWindowTitle("About Me")
        msg.setTextFormat(QtCore.Qt.TextFormat.RichText)
        msg.setText("Hi. I am Qasem Talaee.<br>"
                    "I am a computer programmer.<br>"
                    "I wrote this software for free, hoping that you will enjoy from gaming on linux.<br>"
                    "<b><i>Enjoy It My Friend !</i></b><br><br>"
                    "My Github : <a href='https://github.com/qasem-talaee'>https://github.com/qasem-talaee</a><br>"
                    "My Website : <a href='http://qtle.ir'>http://qtle.ir</a><br>"
                    "My Email : <a href='mailto:qasem.talaee1375@gmail.com'>qasem.talaee1375@gmail.com</a><br>")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec_()
        
    def install_wine(self):
        os.chdir(sys.path[0])
        subprocess.call(['sh', './bash/wine.sh'])
        msg = QMessageBox()
        msg.setWindowTitle("Completed")
        msg.setText("Installation completed successfully.")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec_()
        
app = QApplication(sys.argv)
window = WineMain()
app.exec_()