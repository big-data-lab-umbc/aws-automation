#!/bin/bash

apt-get update
apt-get install -y sudo
sudo apt-get install -y software-properties-common
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev

sudo apt-get install -y python3-pip
sudo apt-get install -y awscli git wget curl zip unzip vim apt-utils gcc make libc-dev musl-dev g++

python3 -m pip install pip --upgrade
python3 -m pip install wheel

python3 -m pip install --upgrade pip setuptools
python3 -m pip install configargparse
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

#install openmpi, torch and horovod
wget https://download.open-mpi.org/release/open-mpi/v4.0/openmpi-4.0.0.tar.gz
tar -xzvf openmpi-4.0.0.tar.gz
cd openmpi-4.0.0/ && ./configure --prefix=/usr/local/ && sudo make all install

sudo apt update
wget https://developer.nvidia.com/compute/machine-learning/cudnn/secure/8.2.1.32/10.2_06072021/Ubuntu18_04-x64/libcudnn8_8.2.1.32-1+cuda10.2_amd64.deb


wget https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64/libnccl-dev_2.4.7-1+cuda10.1_amd64.deb
wget https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64/libnccl2_2.4.7-1+cuda10.1_amd64.deb
sudo dpkg -i libnccl2_2.4.7-1+cuda10.1_amd64.deb
sudo dpkg -i libnccl-dev_2.4.7-1+cuda10.1_amd64.deb

pip3 install torch torchvision
HOROVOD_WITH_PYTORCH=1 HOROVOD_GPU_OPERATIONS=NCCL HOROVOD_WITH_MPI=1 pip3 install --no-cache-dir horovod[pytorch,tensorflow,keras]

pip3 install --upgrade tensorflow

sudo cp /usr/local/cuda-10.1/compat/* /usr/local/cuda/lib64/

#get and install code for cloud-phase-prediction-main
wget -P /home/ubuntu/ https://ai-4-atmosphere-remote-sensing.s3.amazonaws.com/cloud-phase-prediction-main.zip
unzip /home/ubuntu/cloud-phase-prediction-main.zip -d /home/ubuntu/
cd /home/ubuntu/cloud-phase-prediction-main
sudo pip3 install .

#run commands on EC2 instance i-0e3e1b3ee379e5346
cd /home/ubuntu/cloud-phase-prediction-main && /usr/bin/python3 train.py --training_data_path='./example/training_data/'  --model_saving_path='./saved_model/'
aws s3 cp --acl public-read /home/ubuntu/cloud-phase-prediction-main/saved_model s3://ai-4-atmosphere-remote-sensing/cloud-phase-prediction_result --recursive

#get and install code for DL_3d_cloud_retrieval
wget -P /home/ubuntu/ https://ai-4-atmosphere-remote-sensing.s3.amazonaws.com/DL_3d_cloud_retrieval-main.zip
unzip /home/ubuntu/DL_3d_cloud_retrieval-main.zip -d /home/ubuntu/
cd /home/ubuntu/DL_3d_cloud_retrieval-main
sudo pip3 install -r requirements.txt

#run commands on EC2 instance i-0e3e1b3ee379e5346
cd /home/ubuntu/DL_3d_cloud_retrieval-main && python3 COT_retrieval/test.py --cot_file_name=example/training_data/data_cot.h5 --path_1d_retrieval=retrieved_COT/ --path_model=saved_model/lstm/model-1.h5 --path_predictions=saved_model/bilstm_transformer_embedding/ --radiance_test=example/testing_data/X_test_1.npy --cot_test=example/testing_data/y_test_1.npy --path_plots=plots/bilstm_with_transformer_embedding/

python3 COT_retrieval/test.py --cot_file_name=example/training_data/data_cot.h5 --path_1d_retrieval=retrieved_COT/ --path_model=saved_model/lstm/model-1.h5 --path_predictions=saved_model/bilstm_transformer_embedding/ --radiance_test=example/testing_data/X_test_1.npy --cot_test=example/testing_data/y_test_1.npy --path_plots=plots/bilstm_with_transformer_embedding/
