#!/bin/sh

echo "============================================================================================"
echo Download-Manager Copier
sudo systemctl is-active download-manager-copier
echo "============================================================================================"
echo Download-Manager Operator
sudo systemctl is-active download-manager-operator
echo "============================================================================================"
echo Download-Manager Interface
sudo systemctl is-active download-manager-interface
echo "============================================================================================"



