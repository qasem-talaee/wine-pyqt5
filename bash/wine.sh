#!/bin/bash
# Script for downloading & installing wine on Debian based systems
# Originaly author: #ToDo: please write your information
# Modified by: Mobin Aydinfar <mobin@mobintestserver.ir>
# Project: https://github.com/qasem-talaee/wine-pyqt5

# Updating repos info using apt
sudo apt update
if [ $? -ne 0 ]  ; then
  #echo "[INFO] apt update is Done!"
  exit 0
fi

# Installing recommended packages (apt-transport-https & ...)
sudo apt install software-properties-common apt-transport-https wget -y
if [ $? -ne 0 ]  ; then
  #echo "[INFO] Installing recommended packages is Done!"
  exit 0
fi

# Add i386 packages for wine, Required!
# ToDo: Find a way to detect ARM systems
sudo dpkg --add-architecture i386
if [ $? -ne 0 ]  ; then
  #echo "[INFO] Adding i386 repos is Done!"
  exit 0
fi

# You have two way for downloading and installing wine:
# 1. Using wine in official repos, its default & usually there is a very old version of wine in it.
# 2. Using wine repo on ubuntu/debian. for this, you must uncomment its & commnet #1 installing commands

# ToDo: Using fail detecter
# 2:
#wget -nc https://dl.winehq.org/wine-builds/ubuntu/dists/jammy/winehq-jammy.sources
#sudo mv winehq-jammy.sources /etc/apt/sources.list.d/
#wget -nc https://dl.winehq.org/wine-builds/winehq.key
#sudo mv winehq.key /usr/share/keyrings/winehq-archive.key
#sudo apt update
#sudo apt install winehq-staging --install-recommends

# 1 (default):
sudo apt install --install-recommends wine-stable -y
if [ $? -ne 0 ]  ; then
  #echo "[INFO] Installing wine is Done!"
  exit 0
fi

# Installing Mesa vulkan driver & dxvk for wine
# ToDo: Find a way to detect nouveau for not installing mesa-vulkan-drivers & dxvk (nouveau does not support Vulkan!)
# ToDo: Find a way to detect NVIDIA Proprietary driver. its not using mesa-vulkan-driver!
sudo apt install mesa-vulkan-drivers mesa-vulkan-drivers:i386 libvulkan1 libvulkan1:i386 *vulkan* *dxvk* -y
if [ $? -ne 0 ]  ; then
  #echo "[INFO] Installing vulkan driver & dxvk is Done!"
  exit 0
fi

# Checking wine version
wine --version
