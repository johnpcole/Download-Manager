#!/bin/sh
echo "============================================================================================"
echo "===   Getting Download-Manager, version $1, and placing in local folder $2   ==="
echo "============================================================================================"
echo " =========================================================================================="
echo "  ========================================================================================"
echo "   Setting up Application folder $2"
echo "  ========================================================================================"
echo " =========================================================================================="
echo "============================================================================================"
mkdir --verbose /home/pi/$2
echo "============================================================================================"
mkdir --verbose /home/pi/$2/data
echo "============================================================================================"
mkdir --verbose /home/pi/$2/data/application_logs
echo "============================================================================================"
mkdir --verbose /home/pi/$2/data/monitor_history
echo "============================================================================================"
mkdir --verbose /home/pi/$2/data/application_config
echo "============================================================================================"
rm --verbose -r /home/pi/GETGITDOWNLOADTEMP
echo "============================================================================================"
rm --verbose -r /home/pi/$2/codebase
echo "============================================================================================"
rm --verbose -r /home/pi/$2/webassets
echo "============================================================================================"
rm --verbose -r /home/pi/$2/other
echo "============================================================================================"
rm --verbose /home/pi/$2/*.py
echo "============================================================================================"
rm --verbose /home/pi/$2/*.sh
echo "============================================================================================"
echo " =========================================================================================="
echo "  ========================================================================================"
echo "   Setting up temporary unzipping folder and getting package"
echo "  ========================================================================================"
echo " =========================================================================================="
echo "============================================================================================"
mkdir --verbose /home/pi/GETGITDOWNLOADTEMP
echo "============================================================================================"
echo "cd /home/pi/GETGITDOWNLOADTEMP"
cd /home/pi/GETGITDOWNLOADTEMP
echo "============================================================================================"
wget https://github.com/johnpcole/Download-Manager/archive/$1.zip
echo "============================================================================================"
unzip $1.zip
echo "============================================================================================"
echo "rewriting launch-manager.sh"
sed -i "s+/mnt/Torrents-Disk/Download-Manager+/home/pi/$2+g" /home/pi/GETGITDOWNLOADTEMP/Download-Manager-$1/launch_manager.sh
echo "============================================================================================"
echo "rewriting launch-monitor.sh"
sed -i "s+/mnt/Torrents-Disk/Download-Manager+/home/pi/$2+g" /home/pi/GETGITDOWNLOADTEMP/Download-Manager-$1/launch_monitor.sh
echo "============================================================================================"
echo "rewriting launch-copier.sh"
sed -i "s+/mnt/Torrents-Disk/Download-Manager+/home/pi/$2+g" /home/pi/GETGITDOWNLOADTEMP/Download-Manager-$1/launch_copier.sh
echo "============================================================================================"
echo "turning .sh files into executables"
chmod --verbose 744 /home/pi/GETGITDOWNLOADTEMP/Download-Manager-$1/*.sh
echo "============================================================================================"
echo " =========================================================================================="
echo "  ========================================================================================"
echo "   Copying Application to Application folder $2"
echo "  ========================================================================================"
echo " =========================================================================================="
echo "============================================================================================"
cp --verbose -r /home/pi/GETGITDOWNLOADTEMP/Download-Manager-$1/* /home/pi/$2/
echo "============================================================================================"
echo " =========================================================================================="
echo "  ========================================================================================"
echo "   Removing temporary unzipping folder"
echo "  ========================================================================================"
echo " =========================================================================================="
echo "============================================================================================"
rm --verbose -r /home/pi/GETGITDOWNLOADTEMP
echo "============================================================================================"
echo "===   Finished!                                                                          ==="
echo "============================================================================================"
