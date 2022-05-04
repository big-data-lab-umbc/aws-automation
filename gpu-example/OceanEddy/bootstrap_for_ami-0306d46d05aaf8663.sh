#!/bin/bash
#commands to run the programs on top of ami-0306d46d05aaf8663: Deep Learning AMI (Ubuntu 18.04) Version 59.0
#Built with AWS Anaconda of MXNet-1.8, TensorFlow-2.7, PyTorch-1.10, Neuron, & others. NVIDIA CUDA, cuDNN, NCCL, Intel MKL-DNN, Docker, NVIDIA-Docker & EFA support. For fully managed experience, check: https://aws.amazon.com/sagemaker

# anaconda activate
source activate tensorflow2_p38

# install open-mpi
wget https://download.open-mpi.org/release/open-mpi/v4.0/openmpi-4.0.0.tar.gz
tar -xzvf openmpi-4.0.0.tar.gz
cd openmpi-4.0.0/ && ./configure --prefix=/usr/local/ && sudo make all install

# install horovod
HOROVOD_GPU_OPERATIONS=NCCL HOROVOD_WITH_MPI=1 python3 -m pip install --no-cache-dir horovod[pytorch,tensorflow,keras]

#run horovod version
horovodrun --verbose -np 1 -H localhost:1 python3 eddy_classification_task_vseraj_horovod.py

horovodrun --verbose -np 2 -H localhost:2 python3 eddy_classification_task_vseraj_horovod.py
