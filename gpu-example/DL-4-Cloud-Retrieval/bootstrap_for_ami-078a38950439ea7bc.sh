#!/bin/bash
#commands to run the programs on top of ami-078a38950439ea7bc: Deep Learning AMI GPU TensorFlow 2.7.0 (Amazon Linux 2) 20220316
#ami-078a38950439ea7bc (64-bit (x86))
#Built with AWS optimized TensorFlow, NVIDIA CUDA, cuDNN, NCCL, GPU Driver, Docker, NVIDIA-Docker and EFA support.

# install open-mpi
wget https://download.open-mpi.org/release/open-mpi/v4.0/openmpi-4.0.0.tar.gz
tar -xzvf openmpi-4.0.0.tar.gz
cd openmpi-4.0.0/ && ./configure --prefix=/usr/local/ && sudo make all install

# install horovod
HOROVOD_WITH_PYTORCH=1 HOROVOD_GPU_OPERATIONS=NCCL HOROVOD_WITH_MPI=1 /usr/bin/python3.8 -m pip install --no-cache-dir horovod[pytorch,tensorflow,keras]

#get and install code for cloud-phase-prediction-main
wget -P /home/ec2-user/ https://ai-4-atmosphere-remote-sensing.s3.amazonaws.com/cloud-phase-prediction-main.zip
unzip /home/ec2-user/cloud-phase-prediction-main.zip -d /home/ec2-user/
cd /home/ec2-user/cloud-phase-prediction-main && /usr/bin/python3.8 -m pip install .

#run horovod version
cd /home/ec2-user/cloud-phase-prediction-main && horovodrun --verbose -np 1 -H localhost:1 /usr/bin/python3.8 train_para.py --training_data_path='./example/training_data/'  --model_saving_path='./saved_model/'

#run commands on EC2 instance
cd /home/ec2-user/cloud-phase-prediction-main && /usr/bin/python3.8 train.py --training_data_path='./example/training_data/'  --model_saving_path='./saved_model/'
aws s3 cp --acl public-read /home/ec2-user/cloud-phase-prediction-main/saved_model s3://ai-4-atmosphere-remote-sensing/cloud-phase-prediction_result --recursive

#get and install code for DL_3d_cloud_retrieval
wget -P /home/ec2-user/ https://ai-4-atmosphere-remote-sensing.s3.amazonaws.com/DL_3d_cloud_retrieval-main.zip
unzip /home/ec2-user/DL_3d_cloud_retrieval-main.zip -d /home/ec2-user/
cd /home/ec2-user/DL_3d_cloud_retrieval-main && /usr/bin/python3.8 -m pip install -r requirements.txt

#run commands on EC2 instance
cd /home/ec2-user/DL_3d_cloud_retrieval-main && mkdir -p outputs && /usr/bin/python3.8 COT_retrieval/test_example.py --cot_file_name=example/training_data/data_cot.h5 --path_1d_retrieval=example/retrieved_COT/ --path_model=saved_model/lstm/model1.h5 --path_predictions=outputs/ --radiance_test=example/testing_data/X_test_1.npy --cot_test=example/testing_data/y_test_1.npy --path_plots=outputs/
aws s3 cp --acl public-read /home/ec2-user/DL_3d_cloud_retrieval-main/outputs/ s3://ai-4-atmosphere-remote-sensing/DL_3d_cloud_retrieval-outputs/ --recursive
#aws s3 cp --acl public-read /home/ec2-user/DL_3d_cloud_retrieval-main/plot s3://ai-4-atmosphere-remote-sensing/DL_3d_cloud_retrieval-outputs/plot --recursive
