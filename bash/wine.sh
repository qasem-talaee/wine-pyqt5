#!/bin/bash

pack=''
which apt
if [ $? -eq 0 ]  ; then
  pack='apt'
fi
which yum
if [ $? -eq 0 ]  ; then
  pack='yum'
fi
which pacman
if [ $? -eq 0 ]  ; then
  pack='pacman'
fi
which zypper
if [ $? -eq 0 ]  ; then
  pack='zypper'
fi
which dnf
if [ $? -eq 0 ]  ; then
  pack='dnf'
fi

sudo $pack update
sudo $pack install software-properties-common apt-transport-https wget dpkg -y
sudo dpkg --add-architecture i386
sudo $pack install --install-recommends wine-stable -y
sudo $pack install mesa-vulkan-drivers mesa-vulkan-drivers:i386 libvulkan1 libvulkan1:i386 *vulkan* *dxvk* -y
wine --version