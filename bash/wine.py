import subprocess

class InstallWine:
    
    def __init__(self):
        subprocess.call(['sh', './bash/wine.sh'])