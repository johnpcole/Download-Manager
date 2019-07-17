#!/bin/sh

cd /mnt/Torrents-Disk/Download-Manager

cp /mnt/Torrents-Disk/Download-Manager/data/application_logs/manager_8.log /mnt/Torrents-Disk/Download-Manager/data/application_logs/manager_9.log
cp /mnt/Torrents-Disk/Download-Manager/data/application_logs/manager_7.log /mnt/Torrents-Disk/Download-Manager/data/application_logs/manager_8.log
cp /mnt/Torrents-Disk/Download-Manager/data/application_logs/manager_6.log /mnt/Torrents-Disk/Download-Manager/data/application_logs/manager_7.log
cp /mnt/Torrents-Disk/Download-Manager/data/application_logs/manager_5.log /mnt/Torrents-Disk/Download-Manager/data/application_logs/manager_6.log
cp /mnt/Torrents-Disk/Download-Manager/data/application_logs/manager_4.log /mnt/Torrents-Disk/Download-Manager/data/application_logs/manager_5.log
cp /mnt/Torrents-Disk/Download-Manager/data/application_logs/manager_3.log /mnt/Torrents-Disk/Download-Manager/data/application_logs/manager_4.log
cp /mnt/Torrents-Disk/Download-Manager/data/application_logs/manager_2.log /mnt/Torrents-Disk/Download-Manager/data/application_logs/manager_3.log
cp /mnt/Torrents-Disk/Download-Manager/data/application_logs/manager_1.log /mnt/Torrents-Disk/Download-Manager/data/application_logs/manager_2.log
cp /mnt/Torrents-Disk/Download-Manager/data/application_logs/manager_0.log /mnt/Torrents-Disk/Download-Manager/data/application_logs/manager_1.log

python3 Download_Manager.py >/mnt/Torrents-Disk/Download-Manager/data/application_logs/manager_0.log 2>&1


