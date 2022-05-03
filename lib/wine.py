import subprocess
import os
import re

class Wine:
    
    def __init__(self, dir):
        self.PATH = 'WINEPREFIX="' + dir + '" '
    
    def get_format(self, file):
        return os.path.splitext(file)[-1].lower()
    
    def run_file(self, file):
        format = self.get_format(file)
        file = re.escape(file)
        if format not in ['.exe', '.msi', '.bat']:
            return 0
        else:
            if format == '.exe':
                subprocess.call(self.PATH + 'wine ' + file, shell=True)
            elif format == '.msi':
                subprocess.call(self.PATH + 'wine msiexec /i ' + file, shell=True)
            elif format == '.bat':
                subprocess.call(self.PATH + 'wine start ' + file, shell=True)
    
    def run_game(self, file):
        format = self.get_format(file)
        file = re.escape(file)
        if format not in ['.exe', '.msi']:
            return 0
        else:
            if format == '.exe':
                subprocess.call(self.PATH + 'wine DXVK_HUD=1 ' + file, shell=True)
            elif format == '.msi':
                subprocess.call(self.PATH + 'wine msiexec /i DXVK_HUD=1 ' + file, shell=True)
            
    def winecfg(self):
        subprocess.call(self.PATH + 'winecfg', shell=True)
        
    def restart(self):
        subprocess.call(self.PATH + 'wineboot -r', shell=True)
        
    def kill(self):
        subprocess.call(self.PATH + 'wineboot -k', shell=True)
    
    def cmd(self):
        subprocess.call(self.PATH + 'wine cmd', shell=True)
        
    def task_manager(self):
        subprocess.call(self.PATH + 'wine taskmgr', shell=True)
        
    def control_panel(self):
        subprocess.call(self.PATH + 'wine control', shell=True)
        
    def uninstaller(self):
        subprocess.call(self.PATH + 'wine uninstaller', shell=True)
        
    def regedit(self):
        subprocess.call(self.PATH + 'wine regedit', shell=True)
        
    def explorer(self):
        subprocess.call(self.PATH + 'wine explorer', shell=True)
        
    def iexplore(self):
        subprocess.call(self.PATH + 'wine iexplore', shell=True)