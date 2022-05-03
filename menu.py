from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLabel, QMessageBox, QVBoxLayout, QWidget, QHBoxLayout, QGroupBox
import sys
import subprocess
from functools import partial

from ui import res
from lib import vulkan, wine

class Menu(QMainWindow):
    
    def __init__(self, dir):
        super(Menu, self).__init__()
        uic.loadUi('ui/menu.ui', self)
        self.MyWine = wine.Wine(dir=dir)
        self.pushButton_14.clicked.connect(self.install_vulkan)
        self.pushButton_2.clicked.connect(self.open_winecfg)
        self.pushButton_3.clicked.connect(self.restart)
        self.pushButton_4.clicked.connect(self.kill)
        self.pushButton_5.clicked.connect(self.cmd)
        self.pushButton_6.clicked.connect(self.task_manager)
        self.pushButton_7.clicked.connect(self.control_panel)
        self.pushButton_8.clicked.connect(self.uninstaller)
        self.pushButton_9.clicked.connect(self.regedit)
        self.pushButton_12.clicked.connect(self.explorer)
        self.pushButton_13.clicked.connect(self.iexplore)
        self.pushButton_10.clicked.connect(self.run_file)
        self.widget = QWidget()
        self.update_dep()
        self.show()
    
    def update_dep(self):
        self.install_but = []
        urls = []
        self.vb = QVBoxLayout()
        with open('lib/link/link.txt', 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                name = line.split(',,')[0]
                urls.append(line.replace('\n', "").split(',,')[1])
                self.hv = QHBoxLayout()
                self.qv = QGroupBox()
                but = QPushButton("Install")
                but.setStyleSheet("""
                                    QPushButton {
                                        background-color: rgb(38, 162, 105);;
                                        color: rgb(255, 255, 255);
                                    }
                                    QPushButton:hover {
                                        background-color: rgb(255, 255, 255);
                                        color: rgb(0, 0, 0);
                                    }
                                """)
                self.install_but.append(but)
                self.hv.addWidget(QLabel(name), stretch=1)
                self.hv.addWidget(self.install_but[i])
                self.qv.setLayout(self.hv)
                self.vb.addWidget(self.qv)
        for i in range(len(self.install_but)):
            self.install_but[i].clicked.connect(partial(self.install_dep, urls[i]))
        self.widget.setLayout(self.vb)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.widget)
        
    def install_dep(self, url):
        msg = QMessageBox()
        msg.setWindowTitle("Download and Install")
        msg.setText("Please wait...")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec_()
        subprocess.call(['bash/download.sh', url])
        name = url.split("/")[-1]
        self.MyWine.run_file("download/" + name)
        msg = QMessageBox()
        msg.setWindowTitle("Completed")
        msg.setText("Installation completed successfully.")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec_()
        
    def install_vulkan(self):
        msg = QMessageBox()
        msg.setWindowTitle("Download and Install")
        msg.setText("Please wait...")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec_()
        links = vulkan.Vulkan().get_list()
        for link in links:
            subprocess.call(['bash/vulkan.sh', "/home/qasem/wine", link, link.split("/")[-1]])
        msg = QMessageBox()
        msg.setWindowTitle("Completed")
        msg.setText("Installation completed successfully.")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec_()
    
    def run_file(self):
        file = str(QFileDialog.getOpenFileName(self, "Select Target Directory")[0])
        result = self.MyWine.run_file(file)
        if result == 0:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Please enter a valid windows executable file.")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec_()
    
    def open_winecfg(self):
        self.MyWine.winecfg()
        
    def restart(self):
        self.MyWine.restart()
        
    def kill(self):
        self.MyWine.kill()
        
    def cmd(self):
        self.MyWine.cmd()
    
    def task_manager(self):
        self.MyWine.task_manager()
        
    def control_panel(self):
        self.MyWine.control_panel()
        
    def uninstaller(self):
        self.MyWine.uninstaller()
        
    def regedit(self):
        self.MyWine.regedit()
        
    def explorer(self):
        self.MyWine.explorer()
        
    def iexplore(self):
        self.MyWine.iexplore()
       
app = QApplication(sys.argv)
dir = sys.argv[1]
window = Menu(dir=dir)
app.exec_()