import os
import subprocess

subprocess.call('python3 -m venv ./venv && source ./venv/bin/activate && pip install -r req.txt', shell=True)
path = os.path.dirname(os.path.realpath(__file__))
home_dir = os.path.expanduser('~')
desktop_source = """#!/bin/bash
[Desktop Entry]
Encoding=UTF-8
Version=1.0
Type=Application
Terminal=false
Exec=bash -c 'source {path}/venv/bin/activate && cd {path} && python3 main.py'
Name=Wine Gui
Icon={path}/ui/icons/icons8-gamer-64.png""".format(path=path)
desktop_file = open('{home_dir}/.local/share/applications/Wine-Gui.desktop'.format(home_dir=home_dir), 'w')
desktop_file.write(desktop_source)
desktop_file.close()
subprocess.call('chmod +x {home_dir}/.local/share/applications/Wine-Gui.desktop'.format(home_dir=home_dir), shell=True)
print('Done!')