import subprocess

class InstallWine:
    
    def __init__(self):
        subprocess.Popen('sudo apt update -y', shell=True)