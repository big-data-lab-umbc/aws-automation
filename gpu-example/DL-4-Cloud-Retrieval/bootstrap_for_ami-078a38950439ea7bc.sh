#!/bin/bash

HOROVOD_WITH_PYTORCH=1 HOROVOD_GPU_OPERATIONS=NCCL HOROVOD_WITH_MPI=1 /usr/bin/python3.8 -m pip install --no-cache-dir horovod[pytorch,tensorflow,keras]

#get and install code for cloud-phase-prediction-main
wget -P /home/ec2-user/ https://ai-4-atmosphere-remote-sensing.s3.amazonaws.com/cloud-phase-prediction-main.zip
unzip /home/ec2-user/cloud-phase-prediction-main.zip -d /home/ec2-user/
cd /home/ec2-user/cloud-phase-prediction-main && /usr/bin/python3.8 -m pip install .

#run commands on EC2 instance 
cd /home/ec2-user/cloud-phase-prediction-main && /usr/bin/python3.8 train.py --training_data_path='./example/training_data/'  --model_saving_path='./saved_model/'
aws s3 cp --acl public-read /home/ec2-user/cloud-phase-prediction-main/saved_model s3://ai-4-atmosphere-remote-sensing/cloud-phase-prediction_result --recursive

#get and install code for DL_3d_cloud_retrieval
wget -P /home/ec2-user/ https://ai-4-atmosphere-remote-sensing.s3.amazonaws.com/DL_3d_cloud_retrieval-main.zip
unzip /home/ec2-user/DL_3d_cloud_retrieval-main.zip -d /home/ec2-user/
cd /home/ec2-user/DL_3d_cloud_retrieval-main && /usr/bin/python3.8 -m pip install -r requirements.txt

#run commands on EC2 instance
cd /home/ec2-user/DL_3d_cloud_retrieval && mkdir -p plot/lstm && /usr/bin/python3.8 COT_retrieval/test_example.py --cot_file_name=example/training_data/data_cot.h5 --path_1d_retrieval=example/retrieved_COT/ --path_model=saved_model/lstm/model1.h5 --path_predictions=saved_model/lstm/ --radiance_test=example/testing_data/X_test_1.npy --cot_test=example/testing_data/y_test_1.npy --path_plots=plots/lstm/
