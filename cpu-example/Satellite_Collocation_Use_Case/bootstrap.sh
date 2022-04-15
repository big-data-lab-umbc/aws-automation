#!/bin/bash

sudo apt-get update
sudo apt-get install -y software-properties-common

sudo apt-get install -y python3-pip
sudo apt-get install -y git wget zip unzip vim curl

pip3 install pandas sklearn numpy h5py

#commands for ml_based_cloud_retrieval_with_data_preprocessing only (line 1-20)
pip3 install matplotlib seaborn tables datetimerange pyhdf netCDF4 pvlib

#for dask
python3 -m pip install "dask[complete]"
pip3 uninstall -y click
pip3 install dask-ml click==7

#get code and data
wget -P /home/ubuntu/ https://ai-4-atmosphere-remote-sensing.s3.amazonaws.com/satellite_collocation-1.0.zip
unzip /home/ubuntu/satellite_collocation-1.0.zip -d /home/ubuntu/
cd /home/ubuntu/satellite_collocation
python setup.py install
