from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLabel, QMessageBox, QVBoxLayout, QWidget, QHBoxLayout, QGroupBox, QDialog, QLineEdit
import sys
import subprocess
from functools import partial

class Add(QMainWindow):
    
    def __init__(self):
        super(Add, self).__init__()
        uic.loadUi('ui/add.ui', self)
        if len(sys.argv) == 1:
            self.name = ''
            self.img = ''
            self.path = ''
            self.status = 'add'
        else:
            self.name = sys.argv[1]
            self.img = sys.argv[2]
            self.path = sys.argv[3]
            self.status = 'edit'
            self.lineEdit.setText(self.name)
            self.lineEdit_2.setText(self.img)
            self.lineEdit_3.setText(self.path)
        self.pushButton.clicked.connect(self.add_img)
        self.pushButton_2.clicked.connect(self.add_path)
        self.pushButton_3.clicked.connect(self.add)
        self.pushButton_4.clicked.connect(self.cancel)
        self.show()
    
    def cancel(self):
        self.close()
        
    def add_img(self):
        file = str(QFileDialog.getOpenFileName(self, "Select Target Directory")[0])
        if file != '':
            self.img = file
            self.lineEdit_2.setText(file)
        
    def add_path(self):
        file = str(QFileDialog.getOpenFileName(self, "Select Target Directory")[0])
        if file != '':
            self.path = file
            self.lineEdit_3.setText(file)
            
    def add(self):
        if self.status == 'add':
            self.name = self.lineEdit.text()
            if self.img == '':
                self.img = self.lineEdit_2.text()
            if self.path == '':
                self.path = self.lineEdit_3.text()
            if self.name == '' or self.img == '' or self.path == '':
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Please enter informtion.")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.exec_()
            else:
                with open('lib/list/list.txt', 'a') as f:
                    f.write("\n" + self.name + ",,," + self.img + ",,," + self.path)
                self.close()
        if self.status == 'edit':
            self.name = self.lineEdit.text()
            self.img = self.lineEdit_2.text()
            self.path = self.lineEdit_3.text()
            if self.name == '' or self.img == '' or self.path == '':
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Please enter informtion.")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.exec_()
            else:
                with open('lib/list/list.txt', 'r') as f:
                    lines = f.readlines()
                with open('lib/list/list.txt', 'w') as f:
                    for line in lines:
                        old_path = line.replace("\n", "").split(",,,")[2]
                        if old_path == self.path and line != '\n':
                            f.write(self.name + ",,," + self.img + ",,," + self.path)
                        else:
                            f.write(line)
                self.close()
                
        
app = QApplication(sys.argv)
window = Add()
app.exec_()