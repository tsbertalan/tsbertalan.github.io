#!/bin/bash
set -e

wget -qO - https://typora.io/linux/public-key.asc | sudo apt-key add -
wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
curl -sSL https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -

mkdir -p ~/usr
mkdir -p ~/bin

sudo apt-get install apt-transport-https curl vim screen python python3 python3.8 openssh-server net-tools git python3-pip

sudo add-apt-repository 'deb https://typora.io/linux ./'
sudo add-apt-repository ppa:deadsnakes/ppa
echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"

# Zotero: https://github.com/retorquere/zotero-deb
wget -qO- https://github.com/retorquere/zotero-deb/releases/download/apt-get/install.sh | sudo bash

# Signal
# NOTE: These instructions only work for 64 bit Debian-based
# Linux distributions such as Ubuntu, Mint etc.

# 1. Install our official public software signing key
wget -O- https://updates.signal.org/desktop/apt/keys.asc | gpg --dearmor > signal-desktop-keyring.gpg
sudo mv signal-desktop-keyring.gpg /usr/share/keyrings/

# 2. Add our repository to your list of repositories
echo 'deb [arch=amd64 signed-by=/usr/share/keyrings/signal-desktop-keyring.gpg] https://updates.signal.org/desktop/apt xenial main' |\
  sudo tee -a /etc/apt/sources.list.d/signal-xenial.list

# 3. Update your package database and install signal
sudo apt update && sudo apt install signal-desktop

sudo apt update

sudo apt install gnome-tweak-tool typora sublime-text sublime-merge code variety p7zip-full wmctrl htop mlocate trash-cli  steam-installer \
	gimp okular zotero signal-desktop lynx \
	sendmail mailutils sendmail-bin \
	python3.6 python3.7 python-tk python3-tk python3.6-tk python3.7-tk python3-dev\
    nvidia-cuda-toolkit

sudo snap install slack --classic

printf "\n\n\n\n================= Go to https://developer.nvidia.com/cudnn and manually install cudnn because nvidia is a butt ================\n\n\n\n"



ln -s /opt/sublime_merge/sublime_merge "$HOME/bin/sublime_merge"

cp ~/Dropbox/Projects/Next\ Task\ Decider/bin/variety.conf ~/.config/variety/variety.conf

# curl https://code.visualstudio.com/sha/download?build=stable\&os=linux-deb-x64 --output ~/Downloads/vscode_x64.deb
# sudo dpkg -i ~/Downloads/vscode_x64.deb

# https://gist.github.com/steinwaywhw/a4cd19cda655b8249d908261a62687f8
dl_url=$( curl -s https://api.github.com/repos/obsidianmd/obsidian-releases/releases/latest  \
	| grep "browser_download_url.*AppImage" | tail -n 1 | cut -d '"' -f 4 )
bash ~/Dropbox/Projects/Computers/install_obsidian.sh $dl_url

# Increase number of file watches to max.
echo "fs.inotify.max_user_watches=524288" | sudo tee -a /etc/sysctl.conf 

wget https://zoom.us/client/latest/zoom_amd64.deb -O ~/Downloads/zoom_amd64.deb && sudo apt install ~/Downloads/zoom_amd64.deb



dl_url=$( curl -s https://api.github.com/repos/prusa3d/PrusaSlicer/releases/latest  \
	| grep "browser_download_url.*AppImage" | tail -n 1 | cut -d '"' -f 4 )
wget "${dl_url}" -P ~/usr/
latest_ps=$( ls ~/usr | grep -i prusaslicer | tail -n 1 )
chmod +x ~/usr/"${latest_ps}"
ln -s ~/usr/"${latest_ps}" ~/bin/PrusaSlicer

sudo pip3 install virtualenvwrapper
