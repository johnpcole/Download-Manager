#!/bin/sh

cd /mnt/Torrents-Disk/Download-Manager

cp /mnt/Torrents-Disk/Download-Manager/data/logging-8.log /mnt/Torrents-Disk/Download-Manager/data/logging-9.log
cp /mnt/Torrents-Disk/Download-Manager/data/logging-7.log /mnt/Torrents-Disk/Download-Manager/data/logging-8.log
cp /mnt/Torrents-Disk/Download-Manager/data/logging-6.log /mnt/Torrents-Disk/Download-Manager/data/logging-7.log
cp /mnt/Torrents-Disk/Download-Manager/data/logging-5.log /mnt/Torrents-Disk/Download-Manager/data/logging-6.log
cp /mnt/Torrents-Disk/Download-Manager/data/logging-4.log /mnt/Torrents-Disk/Download-Manager/data/logging-5.log
cp /mnt/Torrents-Disk/Download-Manager/data/logging-3.log /mnt/Torrents-Disk/Download-Manager/data/logging-4.log
cp /mnt/Torrents-Disk/Download-Manager/data/logging-2.log /mnt/Torrents-Disk/Download-Manager/data/logging-3.log
cp /mnt/Torrents-Disk/Download-Manager/data/logging-1.log /mnt/Torrents-Disk/Download-Manager/data/logging-2.log
cp /mnt/Torrents-Disk/Download-Manager/data/logging-0.log /mnt/Torrents-Disk/Download-Manager/data/logging-1.log

python3 Download_Manager.py >/mnt/Torrents-Disk/Download-Manager/data/logging-0.log 2>%1


