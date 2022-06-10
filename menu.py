from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLabel, QMessageBox, QVBoxLayout, QWidget, QHBoxLayout, QGroupBox
import sys
import subprocess
from functools import partial
import os
import sys

from ui import res
from lib import vulkan, wine

class Menu(QMainWindow):
    
    def __init__(self, dir):
        super(Menu, self).__init__()
        uic.loadUi('ui/menu.ui', self)
        self.MyWine = wine.Wine(dir=dir)
        if not os.path.isdir('lib/list'):
            os.mkdir('libb/list')
        if not os.path.isfile("lib/list/list-{name}.txt".format(name=dir.split("/")[-1])):
            open("lib/list/list-{name}.txt".format(name=dir.split("/")[-1]), 'w').close()
        self.list_file = "lib/list/list-{name}.txt".format(name=dir.split("/")[-1])
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
        self.pushButton_15.clicked.connect(self.notepad)
        self.pushButton_16.clicked.connect(self.wordpad)
        self.pushButton_10.clicked.connect(self.run_file)
        self.pushButton.clicked.connect(self.add_new)
        self.pushButton_11.clicked.connect(self.back)
        self.widget = QWidget()
        self.widget_app = QWidget()
        self.update_dep()
        self.update_app()
        self.show()
    
    def back(self):
        self.close()
        os.chdir(sys.path[0])
        subprocess.call('python3 main.py ' + dir, shell=True)
    
    def add_new(self):
        os.chdir(sys.path[0])
        subprocess.call('python3 add.py ' + '"' + self.list_file + '"', shell=True)
        self.update_app()
    
    def update_app(self):
        self.run_but = []
        self.edit_but = []
        self.del_but = []
        names = []
        imgs = []
        pathes = []
        self.widget_app = QWidget()
        self.vb = QVBoxLayout()
        with open(self.list_file, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if line != '\n':
                    name, img, path = line.replace('\n', "").split(",,,")
                    names.append(name)
                    imgs.append(img)
                    pathes.append(path)
                    self.hv = QHBoxLayout()
                    self.qb = QGroupBox()
                    self.qb.setStyleSheet("""
                                        QGroupBox{
                                            background-color: rgb(157, 163, 158);
                                            border: 2px solid gray; 
                                            border-radius: 10px; 
                                        }
                                        """)
                    self.qb.setMaximumHeight(200)
                    label = QLabel(self)
                    pic = QtGui.QPixmap(img)
                    pic = pic.scaledToHeight(200)
                    label.setPixmap(pic)
                    self.vh_but = QVBoxLayout()
                    self.vh_but.addWidget(QLabel(name))
                    ## Buttons
                    run = QPushButton("Run")
                    run.setStyleSheet("""
                                        QPushButton {
                                            background-color: rgb(38, 162, 105);
                                            color: rgb(255, 255, 255);
                                        }
                                        QPushButton:hover {
                                            background-color: rgb(255, 255, 255);
                                            color: rgb(0, 0, 0);
                                        }
                                    """)
                    self.run_but.append(run)
                    self.vh_but.addWidget(run)
                    edit = QPushButton("Edit")
                    edit.setStyleSheet("""
                                        QPushButton {
                                            background-color: rgb(26, 95, 180);
                                            color: rgb(255, 255, 255);
                                        }
                                        QPushButton:hover {
                                            background-color: rgb(255, 255, 255);
                                            color: rgb(0, 0, 0);
                                        }
                                    """)
                    self.edit_but.append(edit)
                    self.vh_but.addWidget(edit)
                    del_ = QPushButton("Delete")
                    del_.setStyleSheet("""
                                        QPushButton {
                                            background-color: rgb(192, 28, 40);
                                            color: rgb(255, 255, 255);
                                        }
                                        QPushButton:hover {
                                            background-color: rgb(255, 255, 255);
                                            color: rgb(0, 0, 0);
                                        }
                                    """)
                    self.del_but.append(del_)
                    self.vh_but.addWidget(del_)
                    ## END Buttons
                    self.hv.addWidget(label, stretch=1)
                    self.hv.addLayout(self.vh_but)
                    self.qb.setLayout(self.hv)
                    self.vb.addWidget(self.qb)
        for i in range(len(self.run_but)):
            self.run_but[i].clicked.connect(partial(self.run_but_func, pathes[i]))
            self.edit_but[i].clicked.connect(partial(self.edit_but_func, [names[i], imgs[i], pathes[i]]))
            self.del_but[i].clicked.connect(partial(self.del_but_func, pathes[i]))
        self.widget_app.setLayout(self.vb)
        self.scrollArea_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setWidget(self.widget_app)
    
    def run_but_func(self, file):
        self.MyWine.run_game(file)
    
    def edit_but_func(self, file):
        os.chdir(sys.path[0])
        subprocess.call('python3 add.py ' + '"' + self.list_file + '" ' + '"' + file[0] + '" ' + '"' + file[1] + '" ' + '"' + file[2] + '"', shell=True)
        self.update_app()
    
    def del_but_func(self, file):
        msg = QMessageBox()
        msg.setWindowTitle("Delete App or Game")
        msg.setText("Are you sure you want to do this?")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        msg.setIcon(QMessageBox.Icon.Warning)
        result = msg.exec_()
        if result ==  QMessageBox.StandardButton.Ok:
            os.chdir(sys.path[0])
            with open(self.list_file, 'r') as f:
                lines = f.readlines()
            with open(self.list_file, 'w') as f:
                for line in lines:
                    if line.replace('\n', "").split(",,,")[-1] != file:
                        f.write('\n' + line.replace('\n', ""))
            self.update_app()
    
    def open_dialog(self, name=None, img=None, path=None):
        if name == None:
            os.chdir(sys.path[0])
            subprocess.call('python3 add.py', shell=True)
        else:
            pass
    
    def update_dep(self):
        self.install_but = []
        urls = []
        self.vb = QVBoxLayout()
        os.chdir(sys.path[0])
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
                                        background-color: rgb(38, 162, 105);
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
        os.chdir(sys.path[0])
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
            os.chdir(sys.path[0])
            subprocess.call(['bash/vulkan.sh', "/home/qasem/wine", link, link.split("/")[-1]])
        msg = QMessageBox()
        msg.setWindowTitle("Completed")
        msg.setText("Installation completed successfully.")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec_()
    
    def run_file(self):
        file = str(QFileDialog.getOpenFileName(self, "Select Target Directory")[0])
        if file != '':
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
    
    def notepad(self):
        self.MyWine.notepad()
        
    def wordpad(self):
        self.MyWine.wordpad()
       
app = QApplication(sys.argv)
dir = sys.argv[1]
window = Menu(dir=dir)
app.exec_()