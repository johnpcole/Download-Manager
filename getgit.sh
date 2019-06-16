#!/bin/sh
echo "Getting Download-Manager, version $1, and placing in $2"

echo "============================================================================================"
mkdir /home/pi/$2
mkdir /home/pi/$2/data
rm -r /home/pi/GETGITDOWNLOADTEMP
rm -r /home/pi/$2/codebase
rm -r /home/pi/$2/webassets
rm Download-Manager.py

echo "============================================================================================"
mkdir /home/pi/GETGITDOWNLOADTEMP

echo "============================================================================================"
cd /home/pi/GETGITDOWNLOADTEMP

echo "============================================================================================"
wget https://github.com/johnpcole/Download-Manager/archive/$1.zip

echo "============================================================================================"
unzip $1.zip

echo "============================================================================================"
rm /home/pi/GETGITDOWNLOADTEMP/Download-Manager-$1/*.sh
cp -r /home/pi/GETGITDOWNLOADTEMP/Download-Manager-$1/* /home/pi/$2/

echo "============================================================================================"
rm -r /home/pi/GETGITDOWNLOADTEMP

echo "============================================================================================"
echo "Finished!"
