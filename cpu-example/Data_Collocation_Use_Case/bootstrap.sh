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
wget -P /home/ubuntu/ https://kddworkshop.s3.us-west-2.amazonaws.com/ML_based_Cloud_Retrieval_Use_Case.zip
unzip /home/ubuntu/ML_based_Cloud_Retrieval_Use_Case.zip -d /home/ubuntu/