from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
import sys

class Add(QMainWindow):
    
    def __init__(self):
        super(Add, self).__init__()
        uic.loadUi('ui/add.ui', self)
        self.link_file = sys.argv[1]
        if len(sys.argv) == 2:
            self.name = ''
            self.img = ''
            self.path = ''
            self.status = 'add'
        else:
            self.name = sys.argv[2]
            self.img = sys.argv[3]
            self.path = sys.argv[4]
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
            self.new_path = file
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
                with open(self.link_file, 'a') as f:
                    f.write("\n" + self.name + ",,," + self.img + ",,," + self.path)
                self.close()
        if self.status == 'edit':
            self.name = self.lineEdit.text()
            self.img = self.lineEdit_2.text()
            self.new_path = self.lineEdit_3.text()
            if self.name == '' or self.img == '' or self.new_path == '':
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Please enter informtion.")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.exec_()
            else:
                with open(self.link_file, 'r') as f:
                    lines = f.readlines()
                with open(self.link_file, 'w') as f:
                    for line in lines:
                        if line != '\n':
                            old_path = line.replace("\n", "").split(",,,")[2]
                            if self.path == old_path:
                                f.write(self.name + ",,," + self.img + ",,," + self.new_path)
                            else:
                                f.write(line)
                self.close()
                
        
app = QApplication(sys.argv)
window = Add()
app.exec_()