import json
import boto3
import time, sys, os
from datetime import datetime
from botocore.vendored import requests

credentials = ["us-west-2","",""]   #region,access_key,secret_key
InstanceId = 'i-0e78c73fb187d54ed'

def get_ec2_instances_id(region,access_key,secret_key):
    ec2_conn = boto3.resource('ec2',region_name=region,aws_access_key_id=access_key,aws_secret_access_key=secret_key)
    
    if ec2_conn:
        for instance in ec2_conn.instances.all():
            if instance.state['Name'] == 'running' and instance.security_groups[0]['GroupName'] == 'default':
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
    masterInstanceId = InstanceId 
    ssm_client = boto3.client('ssm',region_name=credentials[0],aws_access_key_id=credentials[1],aws_secret_access_key=credentials[2])
    
    send_command_to_master(masterInstanceId,\
        "aws s3 cp /home/ubuntu/satellite_collocation_sample_data/collocation-output s3://ai-4-atmosphere-remote-sensing/collocation-output' '$(date +'%d-%m-%y_%H:%M:%S')/ --recursive",\
        ssm_client) 
        
    time.sleep(2)
    
    html = '''<!DOCTYPE html>
            <html>
                <head>
                    <meta http-equiv="refresh" content="0; url='https://s3.amazonaws.com/ai-4-atmosphere-remote-sensing/index.html'" />
                </head>
                    <body>
                        <p>Please follow <a href="https://www.sampleurl.com">this link</a>.</p>
                    </body>
            </html>'''
    
    return {
        'statusCode': 200,
        'body': html,
            'headers': { 'Content-Type': 'text/html', #'text/html', 
        },   
    }