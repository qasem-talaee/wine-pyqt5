#!/bin/bash

sudo apt update
sudo apt install software-properties-common apt-transport-https wget -y
sudo dpkg --add-architecture i386
#wget -nc https://dl.winehq.org/wine-builds/ubuntu/dists/jammy/winehq-jammy.sources
#sudo mv winehq-jammy.sources /etc/apt/sources.list.d/
#wget -nc https://dl.winehq.org/wine-builds/winehq.key
#sudo mv winehq.key /usr/share/keyrings/winehq-archive.key
#sudo apt update
#sudo apt install winehq-staging --install-recommends
sudo apt install --install-recommends wine-stable
sudo apt install mesa-vulkan-drivers mesa-vulkan-drivers:i386 libvulkan1 libvulkan1:i386 *vulkan* *dxvk* -y
wine --version