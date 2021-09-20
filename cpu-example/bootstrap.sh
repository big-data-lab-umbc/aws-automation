#!/bin/bash

sudo apt-get update 
sudo apt-get install -y software-properties-common 
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt-get update

sudo apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-gdbm python3-setuptools
sudo apt-get install -y git wget zip unzip vim curl

python3.6 -m pip install pip --upgrade
python3.6 -m pip install wheel

python3.6 -m pip install --upgrade pip setuptools
python3.6 -m pip install configargparse
pip3 install pandas sklearn numpy h5py

#commands for ml_based_cloud_retrieval_with_data_preprocessing only (line 1-20)
pip3 install matplotlib seaborn tables datetimerange pyhdf netCDF4 pvlib

#for dask
python3.6 -m pip install "dask[complete]"
pip3 uninstall -y click
pip3 install dask-ml click==7

#get code and data
wget -P /home/ubuntu/ https://kddworkshop.s3.us-west-2.amazonaws.com/ML_based_Cloud_Retrieval_Use_Case.zip
unzip /home/ubuntu/ML_based_Cloud_Retrieval_Use_Case.zip -d /home/ubuntu/