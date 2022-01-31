#!/bin/bash

apt-get update 
apt-get install -y sudo 
sudo apt-get install -y software-properties-common 
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update

sudo apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-gdbm
sudo apt-get install -y git wget curl zip unzip vim apt-utils gcc make libc-dev musl-dev g++

python3.6 -m pip install pip --upgrade
python3.6 -m pip install wheel

python3.6 -m pip install --upgrade pip setuptools
python3.6 -m pip install configargparse
pip3 install tensorflow==2.2.0
pip3 install cmake keras pandas sklearn numpy Cython

# Install OpenSSH to communicate between containers
sudo apt-get install -y --no-install-recommends openssh-client openssh-server
mkdir -p /var/run/sshd

# Setup SSH Daemon
sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config

# Allow OpenSSH to talk to containers without asking for confirmation
cat /etc/ssh/ssh_config | grep -v StrictHostKeyChecking > /etc/ssh/ssh_config.new
echo "    StrictHostKeyChecking no" >> /etc/ssh/ssh_config.new 
mv /etc/ssh/ssh_config.new /etc/ssh/ssh_config

sudo apt-get update
sudo apt-get clean -y && sudo rm -rf /var/lib/apt/lists/*

#for DeepCoral (MultiGpus-Domain-Adaptation-main)
wget https://download.open-mpi.org/release/open-mpi/v4.0/openmpi-4.0.0.tar.gz
tar -xzvf openmpi-4.0.0.tar.gz
cd openmpi-4.0.0/ && ./configure --prefix=/usr/local/ && sudo make all install

sudo apt update
wget https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64/libnccl-dev_2.4.7-1+cuda10.1_amd64.deb
wget https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64/libnccl2_2.4.7-1+cuda10.1_amd64.deb
sudo dpkg -i libnccl2_2.4.7-1+cuda10.1_amd64.deb
sudo dpkg -i libnccl-dev_2.4.7-1+cuda10.1_amd64.deb

pip3 install torch torchvision
HOROVOD_WITH_PYTORCH=1 HOROVOD_GPU_OPERATIONS=NCCL HOROVOD_WITH_MPI=1 pip install --no-cache-dir horovod[pytorch]

sudo cp /usr/local/cuda-10.1/compat/* /usr/local/cuda/lib64/
