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
        "cd /home/ec2-user/cloud-phase-prediction-main && /usr/bin/python3.8 train.py --training_data_path='./example/training_data/'  --model_saving_path='./saved_model/'",\
        ssm_client)

    send_command_to_master(masterInstanceId,\
        "aws s3 cp --acl public-read /home/ec2-user/DL_3d_cloud_retrieval-main/outputs/ s3://ai-4-atmosphere-remote-sensing/DL_3d_cloud_retrieval-outputs/ --recursive",\
        ssm_client)

    return {
        'statusCode': 200,
        'body': json.dumps('Action Completed!  Please check your S3 Bucket ai-4-atmosphere-remote-sensing/cloud-phase-prediction_result for the resutls')
    }
