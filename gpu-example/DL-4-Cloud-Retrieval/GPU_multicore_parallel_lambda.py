import json
import boto3
import time
import sys
import os

credentials = ["","",""]   #insert region,access_key,secret_key
InstanceId = '' #insert your EC2 instance ID

def get_ec2_instances_id(region,access_key,secret_key):
    ec2_conn = boto3.resource('ec2',region_name=region,aws_access_key_id=access_key,aws_secret_access_key=secret_key)
    
    if ec2_conn:
        for instance in ec2_conn.instances.all():
            if instance.state['Name'] == 'running' and instance.security_groups[0]['GroupName'] == '': #insert your security group (i.e. 'default')
                masterInstanceId = instance.instance_id
                print("Master Instance Id is ",masterInstanceId)
        return masterInstanceId
    else:
        print('Region failed', region)
        return None

def send_command_to_master(InstanceId,command,ssm_client):
    print("Ssm run command: ",command)
    response = ssm_client.send_command(InstanceIds=[InstanceId],DocumentName="AWS-RunShellScript",Parameters={'commands': [command]})

def lambda_handler(event, context):
    #event is PAYLOAD
    # masterInstanceId = get_ec2_instances_id(credentials[0],credentials[1],credentials[2])
    masterInstanceId = InstanceId 
    ssm_client = boto3.client('ssm',region_name=credentials[0],aws_access_key_id=credentials[1],aws_secret_access_key=credentials[2])
    
    send_command_to_master(masterInstanceId,\
        "cd /home/ec2-user/DL_3d_cloud_retrieval && mkdir -p plot/lstm && /usr/bin/python3.8 COT_retrieval/test_example.py --cot_file_name=example/training_data/data_cot.h5 --path_1d_retrieval=example/retrieved_COT/ --path_model=saved_model/lstm/model1.h5 --path_predictions=saved_model/lstm/ --radiance_test=example/testing_data/X_test_1.npy --cot_test=example/testing_data/y_test_1.npy --path_plots=plots/lstm/",\
        ssm_client)
    
    send_command_to_master(masterInstanceId,\
        "aws s3 cp --acl public-read /home/ec2-user/DL_3d_cloud_retrieval-main/outputs/ s3://ai-4-atmosphere-remote-sensing/DL_3d_cloud_retrieval-outputs/ --recursive",\
        ssm_client)
    
    # send_command_to_master(masterInstanceId,\
    #     "aws s3 cp --acl public-read /home/ec2-user/DL_3d_cloud_retrieval-main/plot s3://ai-4-atmosphere-remote-sensing/DL_3d_cloud_retrieval-outputs/plot --recursive",\
    #     ssm_client)


    return {
        'statusCode': 200,
        'body': json.dumps('Action Completed!  Please check your S3 Bucket ai-4-atmosphere-remote-sensing/DL_3d_cloud_retrieval-outputs for the resutls')
    }