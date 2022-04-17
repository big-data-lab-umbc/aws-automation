#!/bin/bash

sudo apt-get update
sudo apt-get install -y software-properties-
sudo apt install awscli

sudo apt-get install -y python3-pip
sudo apt-get install -y git wget zip unzip vim curl

pip3 install pandas sklearn numpy h5py

#commands for ml_based_cloud_retrieval_with_data_preprocessing only (line 1-20)
pip3 install matplotlib seaborn tables datetimerange pyhdf netCDF4 pvlib

#for dask
python3 -m pip install "dask[complete]"
pip3 uninstall -y click
pip3 install dask-ml click==7

#get and install code
wget -P /home/ubuntu/ https://ai-4-atmosphere-remote-sensing.s3.amazonaws.com/satellite_collocation-main.zip
unzip /home/ubuntu/satellite_collocation-main.zip -d /home/ubuntu/
cd /home/ubuntu/satellite_collocation-main
sudo python3 setup.py install

#get data
#aws s3 cp --recursive s3://ai-4-atmosphere-remote-sensing/ ./
wget -P /home/ubuntu/ https://ai-4-atmosphere-remote-sensing.s3.amazonaws.com/satellite_collocation_sample_data.zip
unzip /home/ubuntu/satellite_collocation_sample_data.zip -d /home/ubuntu/

#run python command
#python3 examples/collocate_viirs_calipso_dask_cluster/collocation_dask_local.py -tp ../satellite_collocation_sample_data/CALIPSO-L2-01km-CLayer/ -sgp ../satellite_collocation_sample_data/VNP03MOD-VIIRS-Coordinates/ -sdp ../satellite_collocation_sample_data/VNP02MOD-VIIRS-Attributes/ -sp ../satellite_collocation_sample_data/collocation-output/
